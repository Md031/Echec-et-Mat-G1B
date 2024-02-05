import pygame as Pg
import Data as Dt
from Data import Point
import views.Widget as Wdgt

class Text(Wdgt.Widget) :
    """"""

    def __init__(self, position : Dt.Point, text : str, font : Pg.font.Font, color : Pg.Color = Dt.Colors.BLACK, 
    bg_color : Pg.Color = None) :
        super().__init__(position, "text")
        self.__color : Pg.Color = color
        self.__bg_color : Pg.Color = bg_color
        self.__text : str = text
        self.__font : Pg.font.Font = font
        self.__text_renderer : Pg.Surface = font.render(text, True, self.color, self.bg_color)

    @property
    def text(self) -> str :
        return self.__text

    @property
    def color(self) -> Pg.Color :
        return self.__color

    @property
    def bg_color(self) -> Pg.Color :
        return self.__bg_color

    @property
    def font(self) -> Pg.font.Font :
        return self.__font

    def set_color(self, value : Pg.Color) -> None :
        self.__color = value
        self.__text_renderer = self.font.render(self.text, True, self.color, self.bg_color)

    def set_bg_color(self, value : Pg.Color) -> None :
        self.__bg_color = value
        self.__text_renderer = self.font.render(self.text, True, self.color, self.bg_color)

    def display(self, window) -> None:
        window.screen.blit(self.__text_renderer, (self.position.x, self.position.y))

    def __str__(self) -> str:
        return f"Text({self.text},{self.position})"

    def __contains__(self, coords : Point | tuple[int]) -> bool:
        if not isinstance(coords, Dt.Point) :
            coords = Dt.Point(coords[0], coords[1])
        text_rect : Pg.Rect = self.__text_renderer.get_rect()
        return  text_rect.topleft[0] <= coords.x <= text_rect.topleft[0] + text_rect.size[0] and \
            text_rect.topleft[1] <= coords.y <= text_rect.topleft[1] + text_rect.size[1]
