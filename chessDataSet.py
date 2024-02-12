from NeuralNetwork import *
import chess
from torch.utils.data import Dataset, DataLoader

import numpy as np

class ChessDataset(Dataset):
    def __init__(self, games):
        super(ChessDataset, self).__init__()
        self.games = games
    
    def __len__(self):
        return 40_000
    
    def __getitem__(self, index):
        game_i = np.random.randint(self.games.shape[0])
        random_game = chess_data['AN'].values[game_i]
        moves = create_move_list(random_game)
        game_state_i = np.random.randint(len(moves)-1)
        next_move = moves[game_state_i]
        moves = moves[:game_state_i]
        board = chess.Board()
        for move in moves:
            board.push_san(move)
        x = board_2_rep(board)
        y = move_2_rep(next_move, board)
        if game_state_i %2 == 1: #if its an odd number, meaning it is black's turn
            x *= -1              #we multiply the board metrics by -1
        return x, y
    
data_train = ChessDataset(chess_data['AN'])
data_train_loader = DataLoader(data_train, batch_size=32, shuffle=True, drop_last=True) # Shuffle not necessary because games are selected randomly