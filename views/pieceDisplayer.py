import pygame as pg
import chess as ch
import views.widget as wdgt

class PieceDisplayer(wdgt.Widget) :

    def __init__(self, piece : ch.Piece, position : tuple[int] = None) -> None :
        super().__init__(position, "PieceDisplayer")
        self.__piece : ch.Piece = piece
        self.init_image()

    def init_image(self) -> None :
        filename : str = "images/classic/"
        if self.piece.color == ch.WHITE : filename += "W"
        else : filename += "B"
        match self.piece.symbol().upper() :
            case "P" : filename += "pawn"
            case "Q" : filename += "queen"
            case "K" : filename += "king"
            case "N" : filename += "knight"
            case "B" : filename += "bishop"
            case "R" : filename += "rook"
        filename += ".png"
        self.__image : pg.Surface = pg.image.load(filename).convert_alpha()

    @property
    def piece(self) -> ch.Piece : return self.__piece

    @property
    def image(self) -> pg.Surface : return self.__image

    def display(self, window) -> None : window.screen.blit(self.image, self.position)

    def reset(self) -> None : return super().reset()

    def __contains__(self, coords: tuple[int]) -> bool : return super().__contains__(coords)

    def __str__(self) -> str : return f"{self.piece.symbol()}"
