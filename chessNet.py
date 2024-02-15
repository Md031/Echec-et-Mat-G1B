import torch.nn as nn
import torch
import torch.nn.functional as F
from chess import Board
from NeuralNetworkUtils import *
import numpy as np
import chess


class module(nn.Module):
    def __init__(self, hidden_size):
        super(module, self).__init__()
        self.conv1 = nn.Conv2d(hidden_size, hidden_size, 3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(hidden_size, hidden_size, 3, stride=1, padding=1)
        self.bn1 = nn.BatchNorm2d(hidden_size)
        self.bn2 = nn.BatchNorm2d(hidden_size)
        self.activation1 = nn.SELU()
        self.activation2 = nn.SELU()

    def forward(self, x):
        x_input = torch.clone(x)
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.activation1(x)
        x = self.conv2(x)
        x = self.bn2(x)
        x = x + x_input
        x = self.activation2(x)
        return x

        
class ChessNet(nn.Module):
    def __init__(self, hidden_layers=4, hidden_size=200):
        super(ChessNet, self).__init__()
        self.hidden_layers = hidden_layers
        self.input_layer = nn.Conv2d(6, hidden_size, 3, stride=1, padding=1)
        self.module_list = nn.ModuleList([module(hidden_size) for i in range(hidden_layers)])
        self.output_layer = nn.Conv2d(hidden_size, 2, 3, stride=1, padding=1)
        
    def forward(self, x):
        x = self.input_layer(x)
        x = F.relu(x)
        
        for i in range(self.hidden_layers):
            x = self.module_list[i](x)
            
        x = self.output_layer(x)
        
        return x
    
# model = ChessNet()
# # model = torch.load("ChessModel.pt")
# # model.eval()
# model = model.to('cuda') # Uses GPU



# # Picking Moves

# def check_mate_single(board: Board):
#     board = board.copy()
#     legal_moves = list(board.legal_moves)
#     for move in legal_moves:
#         board.push_uci(str(move))
#         if board.is_checkmate():
#             move = board.pop()
#             return move
#         _ = board.pop()

# def distribution_over_moves(vals):
#     probs = np.array(vals)
#     probs = np.exp(probs)
#     probs = probs / probs.sum()
#     probs = probs ** 3
#     probs = probs / probs.sum()
#     return probs

# def predict(x):
#     out = model.forward(x)
#     return out

# def choose_move(board: Board, player, color):
#     legal_moves = list(board.legal_moves)

#     move = check_mate_single(board)
#     if move is not None:
#         return move
    
#     x = torch.Tensor(board_2_rep(board)).float().to('cuda')
#     if color == chess.BLACK:
#         x *= -1
#     x = x.unsqueeze(0)
#     move = predict(x)

#     vals = []
#     froms = [str(legal_move)[:2] for legal_move in legal_moves]
#     froms = list(set(froms))
#     for from_ in froms:
#         val = move[0, :, :][8 - int(from_[1]), letter_2_num[from_[0]]] 
#         vals.append(val)
    
#     probs = distribution_over_moves(vals)

#     chosen_from = str(np.random.choice(froms, size=1, p=probs)[0])[:2]
#     vals = []
#     for legal_move in legal_moves:
#         from_ = str(legal_move)[:2]
#         if from_ == chosen_from:
#             to = str(legal_move)[2:]
#             val = move[1, :, :][8 - int(to[1]), letter_2_num[to[0]]]
#             vals.append(val)
#         else:
#             vals.append(0)

#     chosen_move = legal_moves[np.argmax(vals)]

#     return chosen_move
    