import pygame as pg
import views.widget as wdgt

class TakeBackMove(wdgt.Widget) :

    def __init__(self, position : tuple[int] = None) -> None :
        super().__init__(position, "TakeBackMove")
        self.init_image()

    def init_image(self) -> None :
        filename : str = "images/classic/back.png"
        self.__image : pg.Surface = pg.image.load(filename).convert_alpha()
        self.__image = pg.transform.scale(self.__image, (20,20))

    @property
    def image(self) -> pg.Surface : return self.__image

    def display(self, window) -> None : window.screen.blit(self.image, self.position)

    def reset(self) -> None : return super().reset()

    def __contains__(self, coords: tuple[int]) -> bool :
        x, y = coords
        return (600 < x < 700 and 0 < y < 60)

    def __str__(self) -> str : return f"{self.piece.symbol()}"
