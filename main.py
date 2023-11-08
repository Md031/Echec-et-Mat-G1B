import chess
from ai import *
from human import Human


class Game:
    def __init__(self, board, player_1, player_2) -> None:
        self.board = board
        self.player_1 = player_1
        self.player_2 = player_2


    def who(self, player):
        return "White" if player == chess.WHITE else "Black"

    def play(self):
        try:
            while not board.is_game_over(claim_draw=True):
                if board.turn == chess.WHITE:
                    uci = self.player_1.move(board)
                else:
                    uci = self.player_2.move(board)
                board.push_uci(uci)

                print(board)
        except KeyboardInterrupt:
            msg = "Game interrupted!"

        if board.is_checkmate():
            msg = "checkmate: " + self.who(not board.turn) + " wins!"
        elif board.is_stalemate():
            msg = "draw: stalemate"
        elif board.is_fivefold_repetition():
            msg = "draw: 5-fold repetition"
        elif board.is_insufficient_material():
            msg = "draw: insufficient material"
        elif board.can_claim_draw():
            msg = "draw: claim"
        
        print(msg)



board = chess.Board()

game = Game(board, player_1 = Random(), player_2 = Human())

game.play()
