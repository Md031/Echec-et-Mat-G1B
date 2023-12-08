import pygame as Pg
import Data as Dt
import views.PieceDisplayer as PieceD
import models.Pieces as Pcs
import views.Widget as Wdgt

class Tile(Wdgt.Widget) :
    def __init__(self, position : Dt.Point, grid_position : Dt.Point, color : Pg.Color | str) -> None :
        super().__init__(position, "tile")
        self.__background : Pg.Surface = Pg.Surface((Dt.Utils.DEFAULT_TILE_DIMENSIONS, Dt.Utils.DEFAULT_TILE_DIMENSIONS))
        self.__background.fill(color)
        self.__rect = Pg.rect.Rect(super().position.x, super().position.y, \
            Dt.Utils.DEFAULT_TILE_DIMENSIONS, Dt.Utils.DEFAULT_TILE_DIMENSIONS)
        print(self.__rect)
        self.__grid_position : Dt.Point = grid_position
        self.__color : str | Dt.Point = color
        self.__pieceDisplayer : PieceD.PieceDisplayer = None
        self.__visited : bool = False
        self.__clicked : bool = False
        self.__choice : bool = False

    @property
    def position(self) -> Dt.Point : return Dt.Point(self.__rect.center[0], self.__rect.center[1])

    @property
    def grid_position(self) -> Dt.Point : return self.__grid_position

    @property
    def chess_position(self) -> str :
        return Dt.convert_coordinates(self.grid_position)

    @property
    def color(self) -> Pg.color : return self.__color

    @property
    def pieceDisplayer(self) -> PieceD.PieceDisplayer : return self.__pieceDisplayer

    @property
    def piece(self) -> Pcs.Piece : 
        return self.__pieceDisplayer.piece if self.__pieceDisplayer else None

    @property
    def is_visited(self) -> bool : return self.__visited

    @property
    def is_clicked(self) -> bool : return self.__clicked

    @property
    def is_choice(self) -> bool : return self.__choice

    def set_piece(self, piece : PieceD.PieceDisplayer = None) -> None : self.__pieceDisplayer = piece

    def set_visited(self, value : bool) -> None : self.__visited = value

    def set_clicked(self, value : bool = None) -> None : 
        self.__clicked = not self.__clicked if value is None else value

    def set_choice(self, value : bool) -> None : self.__choice = value

    def __contains__(self, point : Dt.Point | tuple[int]) -> bool : 
        if isinstance(point, Dt.Point) :
            return  super().position.x <= point.x <= super().position.x + Dt.Utils.DEFAULT_TILE_DIMENSIONS and \
                super().position.y <= point.x <= super().position.y + Dt.Utils.DEFAULT_TILE_DIMENSIONS
        else :
            return  super().position.x <= point[0] <= super().position.x + Dt.Utils.DEFAULT_TILE_DIMENSIONS and \
                super().position.y <= point[1] <= super().position.y + Dt.Utils.DEFAULT_TILE_DIMENSIONS

    def display(self, window) -> None :
        window.screen.blit(self.__background, (super().position.x, super().position.y))
        if self.is_clicked :
            Pg.draw.rect(window.screen, Dt.Colors.RED, [super().position.x, super().position.y, \
                Dt.Utils.DEFAULT_TILE_DIMENSIONS, Dt.Utils.DEFAULT_TILE_DIMENSIONS], 2)
        elif self.is_visited :
            Pg.draw.rect(window.screen, Dt.Colors.GREEN, [super().position.x, super().position.y, \
                Dt.Utils.DEFAULT_TILE_DIMENSIONS, Dt.Utils.DEFAULT_TILE_DIMENSIONS], 1)
        if self.__pieceDisplayer :
            self.__pieceDisplayer.display(window)
        if self.is_choice :
            Pg.draw.circle(window.screen, Dt.Colors.YELLOW, (self.center.x, self.center.y), 10)

    def __str__(self) -> str :
        if self.__pieceDisplayer :
            return f"{self.chess_position} : {self.piece}"
        else :
            return f"{self.chess_position} : empty"
