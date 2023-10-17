from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)

ROWS = 6
COLS = 7

def create_board():
    return np.zeros((ROWS, COLS))

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROWS-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROWS):
        if board[r][col] == 0:
            return r

def winning_move(board, piece):
    # Check horizontal, vertical and diagonal winning conditions
    # ... (this code is omitted for brevity)

def minimax(board, depth, maximizingPlayer, alpha, beta):
    valid_locations = [c for c in range(COLS) if is_valid_location(board, c)]
    is_terminal = len(valid_locations) == 0 or winning_move(board, 1) or winning_move(board, 2)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, 2):
                return (None, float('inf'))
            elif winning_move(board, 1):
                return (None, float('-inf'))
            else:
                return (None, 0)
        else:
            return (None, 0)
    if maximizingPlayer:
        value = float('-inf')
        column = np.random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, 2)
            new_score = minimax(temp_board, depth-1, False, alpha, beta)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:
        value = float('inf')
        column = np.random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, 1)
            new_score = minimax(temp_board, depth-1, True, alpha, beta)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

@app.route('/best-move', methods=['POST'])
def get_best_move():
    data = request.get_json()
    board = np.array(data['board'])
    col, score = minimax(board, 4, True, float('-inf'), float('inf'))
    return jsonify({'column': int(col), 'score': score})

if __name__ == '__main__':
    app.run(debug=True)
