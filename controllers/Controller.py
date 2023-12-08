import pygame as Pg
import Data as Dt
import views.Widget as Wdgt
from abc import abstractmethod, ABC

class Controller(ABC) :
    def __init__(self, window, type : int) -> None :
        self._type : int = type
        self._window = window
        self._animate : bool = False
        self._to_animate : list[tuple[Wdgt.Widget, Dt.Point, tuple[int]]] = []

    @property
    def window(self) : return self._window

    @property
    def type(self) -> int : return self._type

    @property
    def is_in_animation(self) -> bool : return self._animate

    def clear_animations(self) -> None : self._to_animate.clear()

    @abstractmethod
    def handle_mouse_motion(self, event) -> None :
        ...

    @abstractmethod
    def handle_mouse_click(self, event) -> None :
        ...

    @abstractmethod
    def handle_key_pressed(self, event) -> None :
        ...

    def update(self) -> None :
        for widget, dest, direction in self._to_animate :
            widget.set_position(Dt.Point(widget.position.x + direction[0], widget.position.y + direction[1]))
            widget.display(self.window)
            if (abs(dest.x - widget.position.x) <= 10 and abs(dest.y - widget.position.y) <= 10) :
                widget.set_position(dest)

    def handle(self, event) -> None :
        match event.type :
            case Pg.MOUSEMOTION :
                self.handle_mouse_motion(event)
            case Pg.MOUSEBUTTONDOWN :
                self.handle_mouse_click(event)
            case Pg.KEYDOWN :
                self.handle_key_pressed(event)
