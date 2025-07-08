# src/analysis_core.py

import chess
import chess.engine
import chess.pgn
import os
import math
from io import StringIO
import asyncio
import argparse

class ChessAnalyzer:
    """
    A class to handle chess analysis using Stockfish with the chess.engine API.
    Calculates Average Centipawn Loss (ACPL) and Lichess-like Accuracy.
    """

    def __init__(self, engine):
        self.engine = engine

    @classmethod
    async def create(cls, stockfish_path):
        try:
            _, engine = await chess.engine.popen_uci(stockfish_path)
            return cls(engine)
        except Exception as e:
            print(f"Error initializing Stockfish engine: {e}")
            raise

    def _centipawns_to_win_percent(self, cp):
        return 50 + 50 * (2 / (1 + math.exp(-0.00368208 * cp)) - 1)

    def _calculate_move_accuracy(self, win_chance_drop):
        win_chance_drop = max(0, win_chance_drop)
        return 103.1668 * math.exp(-0.04354 * win_chance_drop) - 3.1669

    async def analyze_pgn_incrementally(self, pgn_string, depth):
        game = chess.pgn.read_game(StringIO(pgn_string))
        if game is None:
            raise ValueError("Could not parse PGN.")

        board = game.board()
        moves_data = []
        evaluations = []

        print(f"Starting incremental PGN analysis with depth {depth}...")

        info_before = await self.engine.analyse(board, chess.engine.Limit(depth=depth))
        evaluations.append(info_before['score'].white().score(mate_score=32000))
        
        for move in game.mainline_moves():
            if board.is_game_over():
                break

            turn = board.turn
            # Get the Standard Algebraic Notation *before* making the move.
            san = board.san(move)
            
            board.push(move)
            info_after = await self.engine.analyse(board, chess.engine.Limit(depth=depth))

            eval_before_cp = info_before['score'].white().score(mate_score=32000)
            eval_after_cp = info_after['score'].white().score(mate_score=32000)
            evaluations.append(eval_after_cp)

            if turn == chess.WHITE:
                cp_loss = max(0, eval_before_cp - eval_after_cp)
            else:
                cp_loss = max(0, eval_after_cp - eval_before_cp)

            win_percent_before_white = self._centipawns_to_win_percent(eval_before_cp)
            win_percent_after_white = self._centipawns_to_win_percent(eval_after_cp)

            if turn == chess.WHITE:
                win_chance_drop = win_percent_before_white - win_percent_after_white
            else:
                win_chance_drop = win_percent_after_white - win_percent_before_white

            move_accuracy = self._calculate_move_accuracy(win_chance_drop)
            
            moves_data.append({
                "move_number": board.fullmove_number if turn == chess.BLACK else board.fullmove_number,
                "turn": "White" if turn == chess.WHITE else "Black",
                "san": san,
                "acpl": f"{cp_loss:.0f}",
                "accuracy": f"{move_accuracy:.1f}%"
            })

            info_before = info_after

        print("nAnalysis complete.")

        white_acpls = [float(m['acpl']) for m in moves_data if m['turn'] == 'White']
        black_acpls = [float(m['acpl']) for m in moves_data if m['turn'] == 'Black']
        white_accuracies = [float(m['accuracy'][:-1]) for m in moves_data if m['turn'] == 'White']
        black_accuracies = [float(m['accuracy'][:-1]) for m in moves_data if m['turn'] == 'Black']

        avg_white_acpl = sum(white_acpls) / len(white_acpls) if white_acpls else 0
        avg_black_acpl = sum(black_acpls) / len(black_acpls) if black_acpls else 0
        
        avg_white_accuracy = sum(white_accuracies) / len(white_accuracies) if white_accuracies else 0
        avg_black_accuracy = sum(black_accuracies) / len(black_accuracies) if black_accuracies else 0
        
        return avg_white_acpl, avg_black_acpl, avg_white_accuracy, avg_black_accuracy, evaluations, moves_data

    async def quit(self):
        if self.engine:
            await self.engine.quit()
