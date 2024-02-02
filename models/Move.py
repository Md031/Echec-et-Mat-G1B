import Data as Dt
import models.Board as Brd
import models.Pieces as Pcs

class Move :
    def __init__(self, start_pos : Dt.Point, dest_pos : Dt.Point, board : Brd.Board) -> None :
        self.__start_pos : Dt.Point = start_pos
        self.__dest_pos : Dt.Point = dest_pos
        self.__piece_moved : Pcs.Piece = board[self.start_pos]
        self.__piece_captured : Pcs.Piece = board[self.dest_pos]

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
    def san(self) -> str : 
        ...