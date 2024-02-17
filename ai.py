import random 
import chess 
import chess.polyglot
from NeuralNetworkPickMoves import choose_move
from chessNet import ChessNet
import torch

from pieceValues import *

class Ai:   #Interface class
    def __init__(self):
        self.color = None

    def move(board):
        raise Exception("NotImplementedException")
    
    def set_color(self, color):
        self.color = color

class Random(Ai):
    def __init__(self):
        super().__init__()

    def move(self, board):
        move = random.choice(list(board.legal_moves))
        return move.uci()
    
class NeuronalNetworkModel(Ai):
    def __init__(self, ModelPath):
        super().__init__()
        self.model = ChessNet()
        self.model.load_state_dict(torch.load(ModelPath))
        self.model.eval()
        if torch.cuda.is_available():
            device = "cuda"
        else:
            device = "cpu"
        self.model.to(device)

    
    def move(self, board):
        move = choose_move(board, self.color, self.model)
        move = move.uci()
        return move
    
class Minimax(Ai):
    def __init__(self):
        super().__init__()
        self.__book = chess.polyglot.open_reader("Human.bin")   #opening database


    def move(self, board, depth=4):
        try :
            main_entry = self.__book.find(board)
            if main_entry is not None:
                move = main_entry.move.uci()
        except:
            move = self.minimax(board, depth).uci() 
        return move
    
    def minimax(self, board, depth) :
        if board.turn == chess.WHITE:
            return self.maximize(board, depth)[1]
        else :
            return self.minimize(board, depth)[1]
    
    def maximize(self, board, depth : int, alpha = float('-inf'), beta = float('inf'), move = None) -> float :
        if depth == 0 or board.is_game_over() :
            if board.is_checkmate():
                if board.turn != self.color:    #If the current player has checkmate
                    evaluation = float("INF") if self.color == chess.WHITE else float("-INF")
                else:
                    evaluation = float("-INF") if self.color == chess.WHITE else float("INF")
                        
            else:
                evaluation = self.evaluation(board)
            return evaluation, move

        best_move  = None
        score : float = float("-INF")
        valid_actions = board.legal_moves

        for action in valid_actions :
            board.push(action)
            action_score : float = self.minimize(board, depth - 1, alpha, beta, action)[0]
            if action_score > score :
                score = action_score
                best_move = action
            board.pop()
            
            if score >= beta :
                return score, best_move
            alpha = max(alpha, score)
            
        return score, best_move

    def minimize(self, board, depth : int, alpha = float('-inf'), beta = float('inf'), move = None) -> float:
        if depth == 0 or board.is_game_over() :
            if board.is_checkmate():
                if board.turn != self.color:    #If the current player has checkmate
                    evaluation = float("INF") if self.color == chess.WHITE else float("-INF")
                else:
                    evaluation = float("-INF") if self.color == chess.WHITE else float("INF")
                        
            else:
                evaluation = self.evaluation(board)
            return evaluation, move


        best_move = None
        score : float = float("INF")
        valid_actions = board.legal_moves

        for action in valid_actions :
            board.push(action)
            action_score : float = self.maximize(board, depth - 1, alpha, beta, action)[0]
            if action_score < score :
                score = action_score
                best_move = action
            board.pop()
            
            if score <= alpha :
                return score, best_move
            beta = min(beta, score)
            
        return score, best_move
    
    
                
    def evaluation(self, board):
        total_evaluation = 0
        
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:

                if piece.color == chess.WHITE:  #Counts value of the piece using the white player table
                    if piece.piece_type == chess.KING:  #if the current piece is a king we need to check accordingly if its the end game or not
                            if self.is_end_game(board) :
                                total_evaluation += PIECE_VALUES[piece.piece_type - 1] + PIECE_TABLES_WHITE[KING_END_GAME][square]
                            else :
                                total_evaluation += PIECE_VALUES[piece.piece_type - 1] + PIECE_TABLES_WHITE[KING_MIDDLE_GAME][square]
                                
                    else:   #its not a king
                            total_evaluation += PIECE_VALUES[piece.piece_type -1] + PIECE_TABLES_WHITE[piece.piece_type - 1][square] # PIECE_TABLES[piece.piece_type - 1] because piece.piece_type starts at index 1 while our list starts at index 0 (to match the type in the table basically)

                else:    #Counts value of the piece for the black player using the other table
                    if piece.piece_type == chess.KING:
                            if self.is_end_game(board) :
                                total_evaluation -= PIECE_VALUES[piece.piece_type - 1] + PIECE_TABLES_BLACK[KING_END_GAME][square]
                            else :
                                total_evaluation -= PIECE_VALUES[piece.piece_type - 1] + PIECE_TABLES_BLACK[KING_MIDDLE_GAME][square]
                                
                    else:
                            total_evaluation -= PIECE_VALUES[piece.piece_type - 1] + PIECE_TABLES_BLACK[piece.piece_type - 1][square] # PIECE_TABLES[piece.piece_type - 1] because piece.piece_type starts at index 1 while our list starts at index 0 (to match the type in the table basically)
        return total_evaluation

    def is_end_game(self, board):
        # returns true if the current state of the game is ¨the end game
        # measured by two metrics:
        # 1. there is no queens on the board
        # 2. Every side which has a queen has additionally no other pieces or one minorpiece maximum. A minor piece is either a bishop, knight or three pawns since it has the same value.

        # This function is important for the evaluation of the king's position since the evaluation is different in the endgame

        queens_present = any(piece.piece_type == chess.QUEEN for piece in board.piece_map().values()) #checks if theres is queens on the board

        if not queens_present:
            return True

        # Dictionary to store the count of pieces for each side
        side_piece_count = {chess.WHITE: 0, chess.BLACK: 0}

        # Iterate through all the pieces on the board
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                if piece.piece_type != chess.QUEEN and piece.piece_type != chess.KING: 
                    side_piece_count[piece.color] += PIECE_VALUES[piece.piece_type]     # this adds the value of the piece to the counter

        # Check the conditions for each side
        for side in [chess.WHITE, chess.BLACK]:
            if any(piece.piece_type == chess.QUEEN and piece.color == side for piece in board.piece_map().values()):    #checks if there is a queen of the given color
                if side_piece_count[side] > 300:    #checks if there is more than one minor piece or three pawns    
                    return True     #if one side that has a queen has more than one minor piece we stop and return true.
                else:   #else we check for the other side
                    has_more_pieces = False #side has at most one minor piece along with a queen.")

        return has_more_pieces