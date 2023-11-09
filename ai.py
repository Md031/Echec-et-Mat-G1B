import random 
import chess 
import pieceValues

class Ai:   #Interface class
    def move(board):
        raise Exception("NotImplementedException")

class Random(Ai):
    def move(self, board):
        move = random.choice(list(board.legal_moves))
        return move.uci()
    
class Minimax(Ai):
    # not complete
    def move(self, board, depth):
        bestMove = float('-inf')
        for move in board.legal_moves:
            move = chess.push_uci(move)

            value = max(bestMove, self.max_value( board, depth -1))
            board.pop()     #undo the last move

            if(value > bestMove):
                bestMove = value
                bestMoveFinal = move
        return bestMoveFinal
    
    def max_value(self, board, depth):
        if depth <= 0 or board.is_game_over :
            return self.evaluation(board)

        best_move = float('-inf')
        for legal_move in board.legal_moves:
            move = chess.Move.from_uci(str(legal_move))
            board.push(move)

            best_move = max(best_move,  self.min_value(board, depth - 1))
            board.pop()

        return best_move
                
    def min_value(self, board, depth):
        if depth <= 0 or board.is_game_over :
            return self.evaluation(board)

        best_move = None
        best_move = float('inf')
        for legal_move in board.legal_moves:
            move = chess.Move.from_uci(str(legal_move))
            board.push(move)

            best_move = max(best_move, self.max_value(board, depth - 1))
            board.pop()

        return best_move
                
    def evaluation(self):
        #code a method that evaluates the board state using pieceValues tables. 

        # to complete
        pass

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
                if piece.piece_type != chess.QUEEN: 
                    side_piece_count[piece.color] += pieceValues.PIECE_VALUES[piece.piece_type]     # this adds the value of the piece to the counter

        # Check the conditions for each side
        for side in [chess.WHITE, chess.BLACK]:
            if any(piece.piece_type == chess.QUEEN and piece.color == side for piece in board.piece_map().values()):    #checks if there is a queen of the given color
                if side_piece_count[side] > 300:    #checks if there is more than one minor piece or three pawns    
                    has_more_pieces = True #side has more than one minor piece or other pieces along with a queen.")
                else:
                    has_more_pieces = False #side has at most one minor piece along with a queen.")

        if not has_more_pieces:
            return True
        return False