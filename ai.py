import random 
import chess 
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
    
class Minimax(Ai):
    def __init__(self):
        super().__init__()

    # not complete
    def move(self, board, depth):
        bestMove = float('-inf')
        for move in board.legal_moves:
            board.push_uci(move.uci())

            value = max(bestMove, self.max_value( board, depth -1))
            board.pop()     #undo the last move

            if(value > bestMove):
                bestMove = value
                bestMoveFinal = move
                
        return bestMoveFinal.uci()
    
    def max_value(self, board, depth):
        if depth <= 0 or board.is_game_over :
            return self.evaluation(board)

        best_move = float('-inf')
        for move in board.legal_moves:
            board.push_uci(move.uci)()

            best_move = max(best_move,  self.min_value(board, depth - 1))
            board.pop()

        return best_move
                
    def min_value(self, board, depth):
        if depth <= 0 or board.is_game_over :
            return self.evaluation(board)

        best_move = float('inf')
        for move in board.legal_moves:
            board.push_uci(move.uci())

            best_move = max(best_move, self.max_value(board, depth - 1))
            board.pop()

        return best_move
                
    def evaluation(self, board):
        total_evaluation = 0
        
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:

                if piece.color == chess.WHITE:  #Counts value of the piece using the white player table
                    if piece.piece_type == chess.KING:  #if the current piece is a king we need to check accordingly if its the end game or not
                            if self.is_end_game(board) :
                                total_evaluation += PIECE_VALUES[piece.piece_type] + PIECE_TABLES_WHITE[KING_END_GAME][square]
                            else :
                                total_evaluation += PIECE_VALUES[piece.piece_type] + PIECE_TABLES_WHITE[KING_MIDDLE_GAME][square]
                                
                    else:   #its not a king
                            total_evaluation += PIECE_TABLES_WHITE[piece.piece_type - 1][square] # PIECE_TABLES[piece.piece_type - 1] because piece.piece_type starts at index 1 while our list starts at index 0 (to match the type in the table basically)

                else:    #Counts value of the piece for the black player using the other table
                    if piece.piece_type == chess.KING:
                            if self.is_end_game(board) :
                                total_evaluation -= PIECE_VALUES[piece.piece_type] + PIECE_TABLES_BLACK[KING_END_GAME][square]
                            else :
                                total_evaluation -= PIECE_VALUES[piece.piece_type] + PIECE_TABLES_BLACK[KING_MIDDLE_GAME][square]
                                
                    else:
                            total_evaluation -= PIECE_VALUES[piece.piece_type] * PIECE_TABLES_BLACK[piece.piece_type - 1][square] # PIECE_TABLES[piece.piece_type - 1] because piece.piece_type starts at index 1 while our list starts at index 0 (to match the type in the table basically)

        
        if(self.color == chess.BLACK):  #if we evaluate for the black player we need to invert this value this is easier than creating more conditions in the loop up there
            total_evaluation = -total_evaluation

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