import pygame as pg
import data as dt
import views.widget as wdgt

class Popup(wdgt.Widget) :

    def __init__(self, size : tuple[int], content : list[wdgt.Widget] = [], 
    frame : tuple[int] = (dt.Utils.DEFAULT_BOARD_DIMENSIONS, dt.Utils.DEFAULT_BOARD_DIMENSIONS)) :
        self.__size : tuple[int] = size
        position : tuple[int] = ((frame[0] - self.size[0]) // 2, (frame[1] - self.size[1]) // 2)
        super().__init__(position, "Pop-up")
        self.__content : list[wdgt.Widget] = content
        self.__active : bool = False
        self.__bg_color : pg.Surface = pg.Surface(self.size)
        self.__bg_color.fill(dt.Colors.WHITE)

    @property
    def is_active(self) -> bool : return self.__active

    @property
    def content(self) -> list[wdgt.Widget] : return self.__content

    @property
    def size(self) -> tuple[int] : return self.__size

    def set_active(self, value : bool) -> None : self.__active = value

    def add_widget(self, widget : wdgt.Widget) -> None : self.__content.append(widget)

    def __contains__(self, coords : tuple[int]) -> bool : 
        if not isinstance(coords, tuple[int]) :
            coords : tuple[int] = tuple[int](coords[0], coords[1])
        return  (self.x < coords.x < self.x + self.size[0] 
        and self.y < coords.y < self.y + self.size[1])

    def display(self, window) -> None :
        window.screen.blit(self.__bg_color, self.position)
        for widget in self.content :
            widget.display(window)

    def reset(self) -> None :
        self.set_active(False)
        for widget in self.content :
            widget.reset()

    def __str__(self) -> str :
        popup_str : str = f"{self.name} :\n"
        for widget in self.content :
            popup_str += str(widget) + "\n\n"
        return popup_str
