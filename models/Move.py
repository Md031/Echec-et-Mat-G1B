import Data as Dt
import models.Board as Brd
import models.Pieces as Pcs

class Move :
    def __init__(self, start_pos : Dt.Point, dest_pos : Dt.Point, board : Brd.Board) -> None :
        self.__start_pos : Dt.Point = start_pos
        self.__dest_pos : Dt.Point = dest_pos
        self.__piece_moved : Pcs.Piece = board[self.start_pos]
        self.__piece_captured : Pcs.Piece = board[self.dest_pos]
        self.__type : int = Dt.MoveType.DEFAULT
        self.__promote_to : str = None
        self.__castling_rook : Pcs.Piece = None

    @property
    def start_pos(self) -> Dt.Point : return self.__start_pos

    @property
    def dest_pos(self) -> Dt.Point : return self.__dest_pos

    @property
    def piece_moved(self) -> Pcs.Piece : return self.__piece_moved

    @property
    def piece_captured(self) -> Pcs.Piece | None : return self.__piece_captured

    @property
    def uci(self) -> str : 
        return Dt.convert_coordinates(self.start_pos) + Dt.convert_coordinates(self.dest_pos) 

    @property
    def move_type(self) -> int :
        return self.__type

    @property
    def promote_to(self) -> str | None :
        return self.__promote_to

    @property
    def castling_rook(self) -> Pcs.Rook | None :
        return self.__castling_rook

    def set_type(self, value : int) -> None :
        self.__type = value

    def set_dest_pos(self, position : Dt.Point) -> None :
        if self.move_type == Dt.MoveType.EN_PASSANT :
            self.__dest_pos = position

    def set_promotion(self, value : str) -> None :
        if self.move_type == Dt.MoveType.PROMOTION :
            self.__promote_to = value

    def set_castling_rook(self, piece : Pcs.Rook) -> None :
        if self.move_type == Dt.MoveType.CASTLING :
            self.__castling_rook = piece