# src/main.py

from flask import Flask, render_template, request, jsonify
import asyncio
import os
import traceback

# To allow the Flask app to find the analysis_core module
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from analysis_core import ChessAnalyzer

app = Flask(__name__, template_folder='templates')

# --- Configuration ---
STOCKFISH_PATH = "stockfish/stockfish-ubuntu-x86-64-avx2"

@app.route('/')
def index():
    """Renders the main page with the PGN submission form."""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Handles the analysis request from the form.
    Runs the async analysis and returns the results as JSON.
    """
    pgn_data = request.form.get('pgn')
    depth = int(request.form.get('depth', 14))

    if not pgn_data:
        return jsonify({'error': 'No PGN data provided.'}), 400

    try:
        # Run the async analysis function from our sync Flask route
        results = asyncio.run(run_analysis(pgn_data, depth))
        # Also pass the original PGN back to the client for the chessboard
        results['pgn'] = pgn_data
        return jsonify(results)
    except Exception as e:
        # Log the full error to the console for debugging
        print("An error occurred during analysis:")
        print(traceback.format_exc())
        # Return a more specific error to the user
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

async def run_analysis(pgn_string, depth):
    """
    A helper async function to initialize and run the ChessAnalyzer.
    """
    analyzer = None
    try:
        analyzer = await ChessAnalyzer.create(STOCKFISH_PATH)
        w_acpl, b_acpl, w_acc, b_acc, evals, moves = await analyzer.analyze_pgn_incrementally(
            pgn_string,
            depth
        )
        return {
            'white_acpl': f"{w_acpl:.2f}",
            'white_accuracy': f"{w_acc:.2f}",
            'black_acpl': f"{b_acpl:.2f}",
            'black_accuracy': f"{b_acc:.2f}",
            'evaluations': evals,
            'moves_data': moves
        }
    finally:
        if analyzer:
            await analyzer.quit()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
