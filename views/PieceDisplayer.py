import pygame as Pg
import models.Pieces as Pcs
import Data as Dt

class PieceDisplayer(Pg.sprite.Sprite) :
    def __init__(self, position : Dt.Point, piece : Pcs.Piece) -> None :
        Pg.sprite.Sprite.__init__(self)
        self.__piece : Pcs.Piece = piece
        self.__image : Pg.Surface = Pg.image.load(self.__piece.image_filename).convert_alpha()
        self.__rect : Pg.Rect = Pg.rect.Rect(position.x, position.y, \
            self.__image.get_size()[0], self.__image.get_size()[1])
        self.__rect.topleft = position.x, position.y

    @property
    def position(self) -> Dt.Point : return Dt.Point(self.__rect.topleft[0], self.__rect.topleft[1])

    @property
    def center(self) -> Dt.Point : return Dt.Point(self.__rect.center[0], self.__rect.center[1])

    @property
    def grid_position(self) -> Dt.Point : return self.__piece.position

    @property
    def image_filename(self) -> str : return self.__piece.image_filename

    @property
    def piece(self) -> Pcs.Piece : return self.__piece

    def set_position(self, position : Dt.Point) -> None : self.__rect.center = position.x, position.y 

    def display(self, window) -> None : window.screen.blit(self.__image, (self.position.x, self.position.y))
