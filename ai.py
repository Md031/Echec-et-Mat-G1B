import random 
import chess 

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
        #code a method that evaluates the board state, an idea is to count the number of pieces * their values

        # pion : 1 point
        # cavalier : 3 points
        # fou : 3 points
        # tour : 5 points
        # dame : 9 points
        # roi : je pense float(+inf)
        pass