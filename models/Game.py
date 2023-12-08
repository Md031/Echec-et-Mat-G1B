import chess
import models.Board as Bd
import models.Pieces as Pcs
import Data as Dt

class Game :
    """
    """

    def __init__(self, fen : str = None, ai = None) -> None :
        """
        """
        self.__round : int = 0
        self.__state : int = Dt.State.ONGOING
        self.__moves : list = []
        self.__activer_player_actions : list[str] = []

        fen_tokens = self._parse_fen(fen)
        self.__board : Bd.Board = Bd.Board(fen_tokens[0] if fen_tokens else \
            Dt.Utils.DEFAULT_BOARD_FEN)
        self.__active_player : int = fen_tokens[0] if fen_tokens else Dt.Utils.DEFAULT_FIRST_PLAYER
        self.__castling_rights : list[str] = fen_tokens[0] if fen_tokens \
            else Dt.Utils.DEFAULT_CASTLING_RIGHTS.split("|")

    def _parse_fen(self, fen : str) -> list[str] :
        fen_tokens : list[str] = fen.strip().split(" ") if fen else None
        return fen_tokens

    ###########
    # GETTERS #
    ###########
    @property
    def board(self) -> Bd.Board : return self.__board

    @property
    def active_player(self) -> int : return self.__active_player

    @property
    def round(self) -> int : return self.__round

    @property
    def state(self) -> int : return self.__state

    @property
    def moves(self) -> list : return self.__moves

    @property
    def pop_move(self) -> str : return self.__moves.pop()

    @property
    def activer_player_actions(self) -> list[str] : return self._available_actions()

    @property
    def activer_player_castling_rights(self) -> str : self.__castling_rights[self.active_player]

    ###########
    # SETTERS #
    ###########
    def set_board(self, board : str = Dt.Utils.DEFAULT_BOARD_FEN) -> None :
        self.__board.set_board(board)

    def set_active_player(self, active_player : int) -> None :
        self.__active_player = active_player

    def set_casling_rights(self, castling_rights : str) -> None : 
        self.__castling_rights = castling_rights

    def _next_round(self) -> None :
        self.__round += 1
        self.set_active_player(self.round % 2)

    def set_state(self, state : int) -> None : self.__state = state

    def _add_move(self, move : str) -> None : self.__moves.append(move)

    def _add_action(self, action : str) -> None : self.__activer_player_actions.append(action)

    ###################
    # OTHER FUNCTIONS #
    ################### 
    def _available_actions(self) -> list[str] :
        actions : list[str] = []
        for piece in self.board.get_player_pieces(self.active_player) :
            actions.extend(piece.available_actions(self))
        return actions

    def _is_check(self) -> bool :
        ...

    def capture(self, piece : Pcs.Piece) -> None :
        self.__board.capture(piece)

    def update_board(self, move : chess.Move) -> tuple[str, int] :
        # str_move : str = self.chess_board.san(move)
        # move_type : int = MoveType.NORMAL
        # if self.chess_board.is_capture(move) :
        #     move_type = MoveType.CAPTURE
        # elif self.chess_board.is_castling(move) :
        #     move_type = MoveType.CASTLING
        # self.chess_board.push(move)
        # self._update_state()
        # return str_move, move_type
        ...

    def _update_state(self) -> None :
        # if self.chess_board.is_check() :
        #     self.__state = State.CHECK
        # elif self.chess_board.is_checkmate() :
        #     self.__state = State.CHECKMATE
        # elif self.chess_board.is_stalemate() :
        #     self.__state = State.STALEMATE
        # else :
        #     self.__state = State.ONGOING
        ...

    def __str__(self) -> str :
        str_game : str = f"{self.__repr__()}\n\n{str(self.board)}"
        return str_game

    def __repr__(self) -> str :
        str_game : str = "Game\n"
        str_game += f"board : {self.board.fen}\n"
        str_game += f"player 1 : {self.board.get_player_pieces(0)}\n"
        str_game += f"player 2 : {self.board.get_player_pieces(1)}"
        return str_game