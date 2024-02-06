import pygame as Pg
import Data as Dt
import views.Widget as Wdgt

class Popup(Wdgt.Widget) :
    """"""

    def __init__(self , size : Dt.Point, content : list[Wdgt.Widget] = []) :
        self.__size = size
        position : Dt.Point = Dt.Point((Dt.Utils.DEFAULT_BOARD_DIMENSIONS - size.x) // 2, 
            (Dt.Utils.DEFAULT_BOARD_DIMENSIONS - size.y) // 2)
        super().__init__(position, "pop-up")
        self.__content : list[Wdgt.Widget] = content
        self.__active : bool = True
        self.__bg_color : Pg.Surface = Pg.Surface((size.x, size.y))
        self.__bg_color.fill(Dt.Colors.WHITE)

    @property
    def is_active(self) -> bool :
        return self.__active

    @property
    def content(self) -> list[Wdgt.Widget] :
        return self.__content

    @property
    def size(self) -> Dt.Point :
        return self.__size

    def set_active(self, value : bool) -> None :
        self.__active = value

    def add_widget(self, widget : Wdgt.Widget) -> None :
        self.__content.append(widget)

    def __contains__(self, coords : Dt.Point | tuple[int]) -> bool : 
        if not isinstance(coords, Dt.Point) :
            coords : Dt.Point = Dt.Point(coords[0], coords[1])
        return  self.position.x <= coords.x <= self.position.x + self.size.x and \
            self.position.y <= coords.y <= self.position.y + self.size.y

    def display(self, window) -> None :
        window.screen.blit(self.__bg_color, (self.position.x, self.position.y))
        for widget in self.content :
            widget.display(window)

    def __str__(self) -> str :
        popup_str : str = "popup :\n"
        for widget in self.content :
            popup_str += str(widget) + "\n\n"
        return popup_str
