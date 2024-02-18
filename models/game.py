import chess as ch
import data as dt

class Game :
    def __init__(self) -> None :
        self.__board : ch.Board = ch.Board()
        self.__round : int = 0
        self.__state : int = dt.State.ONGOING
        self.__active_player_actions : list[ch.Move] = []
        self.update_state()

    # getters 
    @property
    def board(self) -> ch.Board : return self.__board

    @property
    def active_player(self) -> bool : return self.board.turn

    @property
    def round(self) -> int : return self.__round

    @property
    def state(self) -> int : return self.__state

    @property
    def moves(self) -> list[ch.Move] : return self.board.move_stack

    @property
    def active_player_actions(self) -> list[ch.Move] : return self.__active_player_actions

    @property
    def is_over(self) -> bool :
        return self.state == dt.State.CHECKMATE or self.state == dt.State.STALEMATE

    @property
    def fen(self) -> str : self.board.fen

    # other functions 
    def update_state(self) -> None :
        # we check if the state of the game is blocking in any way
        if self.board.is_check() : return dt.State.CHECK
        elif self.board.is_checkmate() : return dt.State.CHECKMATE
        if self.board.is_stalemate() : return dt.State.STALEMATE
        if self.board.is_variant_draw() : return dt.State.DRAW
        # if everything is ok we update the player actions
        self.__active_player_actions = self.board.legal_moves
        
        # print(" player : ", self.active_player, " actions : ")
        # for elem in list(self.__active_player_actions):
            # print(elem, " ", end= " ")
        # print("\n-----------------------")

    def push_move(self, move : ch.Move) -> None :
        self.board.push(move)
        self.update_state()

    def pop_move(self) -> ch.Move :
        move : ch.Move = self.board.pop()
        self.update_state()
        return move

    def reset(self) -> None :
        self.__board.reset()
