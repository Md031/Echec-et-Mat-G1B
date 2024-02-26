import pygame as pg
import data as dt
import views.widget as wdgt

class Text(wdgt.Widget) :
    def __init__(self, position : tuple[int], text : str, font : pg.font.Font, 
    color : pg.Color = dt.Colors.BLACK, bg_color : pg.Color = None) :
        super().__init__(position, "Text")
        self.__color : pg.Color = [color, None]
        self.__bg_color : pg.Color = [bg_color, None]
        self.__text : str = text
        self.__font : pg.font.Font = font
        self.__text_renderer : pg.Surface = font.render(text, True, self.__color[0], self.__bg_color[0])

    @property
    def text(self) -> str : return self.__text

    @property
    def color(self) -> pg.Color : return self.__color[0]

    @property
    def bg_color(self) -> pg.Color : return self.__bg_color[0]

    @property
    def font(self) -> pg.font.Font : return self.__font

    @property
    def text_renderer(self) -> pg.Surface : return self.__text_renderer

    def set_color(self, value : pg.Color) -> None :
        self.__color[1] = value
        self.__text_renderer = self.font.render(self.text, True, self.__color[1], self.__bg_color[0])

    def set_bg_color(self, value : pg.Color) -> None :
        self.__bg_color[1] = value
        self.__text_renderer = self.font.render(self.text, True, self.color[0], self.__bg_color[1])

    def reset(self) -> None :
        self.__color = [self.__color[0], None]  
        self.__bg_color = [dt.Colors.BG_COLOR, None]
        self.__text_renderer = self.font.render(self.text, True, self.color[0], self.bg_color[0])

    def set_txt(self, new_txt : str) -> None:
        self.__text = new_txt
        self.__text_renderer = self.font.render(self.__text, True, self.__color[0], self.__bg_color[0])

    def set_coord(self, new_coord: tuple[int]) -> None:
        self.set_position(new_coord)
        self.__text_renderer = self.font.render(self.text, True, self.color, self.bg_color)

    def display(self, window) -> None : window.screen.blit(self.__text_renderer, self.position)

    def __str__(self) -> str : return f"{self.name}({self.text}, {self.position})"

    def __contains__(self, coords : tuple[int]) -> bool : super().__contains__(coords)
