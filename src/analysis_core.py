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
        """
        Creates and initializes a ChessAnalyzer instance, starting Stockfish
        and enabling WDL statistics.
        """
        try:
            _, engine = await chess.engine.popen_uci(stockfish_path)
            await engine.configure({"UCI_ShowWDL": "true"})
            return cls(engine)
        except Exception as e:
            print(f"Error initializing Stockfish engine: {e}")
            raise

    def _wdl_to_win_chance(self, wdl_score, turn):
        """
        Converts a WDL score object into a single win chance percentage (from 0 to 1).
        The score is from the engine's perspective (usually White's).
        """
        # The wdl_score object behaves like a tuple (wins, draws, losses)
        win_prob = wdl_score[0] / 1000.0
        draw_prob = wdl_score[1] / 1000.0
        
        # Win chance is the chance of winning plus half the chance of drawing.
        win_chance = win_prob + (draw_prob / 2.0)

        # If it's Black's turn, we need the inverse perspective for their win chance.
        if turn == chess.BLACK:
            return 1.0 - win_chance
        return win_chance

    def _calculate_accuracy_from_acpl(self, acpl):
        """
        Calculates Lichess-like accuracy percentage from average centipawn loss.
        """
        # This is the formula provided by Lichess in their documentation.
        return 103.1668 * math.exp(-0.04354 * acpl) if acpl > 0 else 100.0


    async def analyze_pgn_incrementally(self, pgn_string, depth):
        """
        Analyzes a PGN game incrementally to calculate ACPL and Accuracy for both players.
        """
        game = chess.pgn.read_game(StringIO(pgn_string))
        if game is None:
            raise ValueError("Could not parse PGN.")

        board = game.board()
        white_acpls = []
        black_acpls = []

        print(f"Starting incremental PGN analysis with depth {depth}...")

        # Get evaluation of the initial position
        info_before = await self.engine.analyse(board, chess.engine.Limit(depth=depth))
        
        for i, move in enumerate(game.mainline_moves()):
            if board.is_game_over():
                break

            turn = board.turn
            player_name = "White" if turn == chess.WHITE else "Black"
            
            # Make the move and analyze the position *after*
            board.push(move)
            info_after = await self.engine.analyse(board, chess.engine.Limit(depth=depth))

            eval_before_cp = info_before['score'].white().score(mate_score=32000)
            eval_after_cp = info_after['score'].white().score(mate_score=32000)

            # --- Centipawn Loss Calculation ---
            if turn == chess.WHITE:
                cp_loss = max(0, eval_before_cp - eval_after_cp)
                white_acpls.append(cp_loss)
            else:
                cp_loss = max(0, eval_after_cp - eval_before_cp)
                black_acpls.append(cp_loss)

            print(f"Move {i//2 + 1} ({move.uci()}) by {player_name}: ACPL={cp_loss:.0f}")

            # The "after" info becomes the "before" for the next move
            info_before = info_after

        print("nAnalysis complete.")

        avg_white_acpl = sum(white_acpls) / len(white_acpls) if white_acpls else 0
        avg_black_acpl = sum(black_acpls) / len(black_acpls) if black_acpls else 0
        
        # Calculate final accuracy from the total average ACPL for each player
        white_final_accuracy = self._calculate_accuracy_from_acpl(avg_white_acpl)
        black_final_accuracy = self._calculate_accuracy_from_acpl(avg_black_acpl)

        return avg_white_acpl, avg_black_acpl, white_final_accuracy, black_final_accuracy

    async def quit(self):
        if self.engine:
            await self.engine.quit()

async def main():
    parser = argparse.ArgumentParser(description="Analyze a chess game PGN to calculate ACPL and Accuracy for each player.")
    parser.add_argument("--pgn_file", required=True, help="Path to the PGN file to analyze.")
    parser.add_argument("--depth", type=int, default=14, help="Stockfish analysis depth. Default is 14.")
    
    args = parser.parse_args()

    stockfish_path = "stockfish/stockfish-ubuntu-x86-64-avx2"
    
    if not os.path.exists(args.pgn_file):
        print(f"Error: PGN file not found at: {args.pgn_file}")
        return

    with open(args.pgn_file, 'r') as f:
        pgn_string = f.read()

    analyzer = None
    try:
        analyzer = await ChessAnalyzer.create(stockfish_path)
        
        w_acpl, b_acpl, w_acc, b_acc = await analyzer.analyze_pgn_incrementally(pgn_string, args.depth)

        print("n--- Analysis Report ---")
        print(f"White: ACPL = {w_acpl:.2f}, Accuracy = {w_acc:.2f}%")
        print(f"Black: ACPL = {b_acpl:.2f}, Accuracy = {b_acc:.2f}%")

    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if analyzer:
            await analyzer.quit()

if __name__ == '__main__':
    asyncio.run(main())
