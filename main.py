import chess
from ai import *
from human import Human
import torch
from chessboard import display



class Game:
    def __init__(self, board, white_player, black_player) -> None:
        self.board = board
        self.__white_player = white_player
        self.__black_player = black_player
        self.__white_player.set_color(chess.WHITE)
        self.__black_player.set_color(chess.BLACK)

    def who(self, player):
        return "White" if player == chess.WHITE else "Black"

    def play(self):
        disp = display.start(board.fen())
        try:
            while not board.is_game_over(claim_draw=True):
                print()
                print(board)
                if board.turn == chess.WHITE:
                    uci = self.__white_player.move(board)
                else:
                    uci = self.__black_player.move(board)
                board.push_uci(uci)
                display.update(board.fen(),disp)  
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

game = Game(board, white_player = Human(), black_player = NeuronalNetworkModel("ChessModel.pt"))

game.play()
