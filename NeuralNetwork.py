import numpy as np
import re
import pandas as pd
import gc


letter_2_num = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
num_2_letter = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}


def board_2_rep(board):
    """Transform the board into a matrix that can be interpreted by the neural network"""
    pieces = ["p", "r", "n", "b", "q", "k"]
    layers = []
    for piece in pieces:
        layers.append(create_rep_layer(board, piece))
    
    board_matrix = np.stack(layers)
    return board_matrix


def create_rep_layer(board, piece: str):
    """Creates a layer in the matrix for the piece type"""
    s = str(board)
    s = re.sub(f"[^{piece}{piece.upper()} \n]", ".", s)
    s = re.sub(f"{piece}", "-1", s)
    s = re.sub(f"{piece.upper()}", "1", s)
    s = re.sub(f"\.", "0", s)

    board_mat = []
    for row in s.split("\n"):
        row = row.split(" ")
        row = [int(x) for x in row]
        board_mat.append(row)
    
    return np.array(board_mat)


def move_2_rep(move, board):
    board.push_san(move).uci()  
    move = str(board.pop())     #Converts a move into its uci format (e2e4) 
    
    from_output_layer = np.zeros((8,8))
    from_row = 8 - int(move[1])
    from_column = letter_2_num[move[0]]
    from_output_layer[from_row, from_column] = 1

    to_output_layer = np.zeros((8,8))
    to_row = 8 - int(move[3])
    tow_column = letter_2_num[move[2]]
    to_output_layer[to_row, tow_column] = 1

    return np.stack([from_output_layer, to_output_layer])


def create_move_list(s):
    return re.sub('\d*\. ','',s).split(' ')[:-1]

chess_data_raw = pd.read_csv('chess_games.csv', usecols = ['AN','WhiteElo'])
chess_data = chess_data_raw[chess_data_raw['WhiteElo'] > 2000]


del chess_data_raw
gc.collect()

chess_data = chess_data[['AN']]
chess_data = chess_data[~chess_data['AN'].str.contains('{')]
chess_data = chess_data[chess_data['AN'].str.len()>20]

print(chess_data.shape[0])