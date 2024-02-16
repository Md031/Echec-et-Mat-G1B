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
        if self.piece.color : filename += "W"
        else : filename += "B"
        filename += f"{ch.PIECE_NAMES[self.piece.piece_type]}.png"
        self.__image : pg.Surface = pg.image.load(filename).convert_alpha()

    @property
    def piece(self) -> ch.Piece : return self.__piece

    @property
    def image(self) -> pg.Surface : return self.__image

    def display(self, window) -> None : window.screen.blit(self.image, self.position)

    def reset(self) -> None : return super().reset()

    def __contains__(self, coords: tuple[int]) -> bool : return super().__contains__(coords)

    def __str__(self) -> str : return f"{self.piece.symbol()}"
