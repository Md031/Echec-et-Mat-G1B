import torch
from chess import Board
from NeuralNetworkUtils import board_2_rep, letter_2_num
import numpy as np
import chess

def check_mate_single(board: Board):
    board = board.copy()
    legal_moves = list(board.legal_moves)
    for move in legal_moves:
        board.push_uci(str(move))
        if board.is_checkmate():
            move = board.pop()
            return move
        _ = board.pop()

def distribution_over_moves(vals):
    probs = np.array(vals)
    probs = np.exp(probs)
    probs = probs / probs.sum()
    probs = probs ** 3
    probs = probs / probs.sum()
    return probs

def predict(x, model):
    out = model.forward(x)
    return out

def choose_move(board: Board, color, model):
    legal_moves = list(board.legal_moves)

    move = check_mate_single(board)
    if move is not None:
        return move
    
    if torch.cuda.is_available():
        device = "cuda"
        x = torch.Tensor(board_2_rep(board)).float().to(device)
    else: # for CPU-only machines
        device = "cpu"
        x = torch.Tensor(board_2_rep(board)).float().to(device)
    
    if color == chess.BLACK:
        x *= -1
    x = x.unsqueeze(0)
    move = predict(x, model)

    vals = []
    froms = [str(legal_move)[:2] for legal_move in legal_moves]
    froms = list(set(froms))
    for from_ in froms:
        val = move[0, 0, :, :][8 - int(from_[1]), letter_2_num[from_[0]]] 
        vals.append(val.detach().to('cpu'))
    probs = distribution_over_moves(vals)
    chosen_from = str(np.random.choice(froms, size=1, p=probs)[0])[:2]

    
    vals = []
    for legal_move in legal_moves:
        from_ = str(legal_move)[:2]
        if from_ == chosen_from:
            to = str(legal_move)[2:]
            val = move[0, 1, :, :][8 - int(to[1]), letter_2_num[to[0]]]
            vals.append(val.detach().to('cpu'))
            #vals.append(val)
        else:
            vals.append(0)

    chosen_move = legal_moves[np.argmax(vals)]

    return chosen_move
    