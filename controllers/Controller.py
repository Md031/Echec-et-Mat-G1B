import pygame as Pg
import Data as Dt
import views.Widget as Wdgt
from abc import abstractmethod, ABC

class Controller(ABC) :
    """
    Classe qui va gérer les intéractions entre l'uilisateur et une des pages de l'application

    Attributes
    ----------
    type : int
        le type du controlleur
    window : Window
        la fenêtre de l'application
    animate : bool
        permet de savoir s'il faut mettre à jour certains éléments de la page controllée
    to_animate : list[tuple[Wdgt.Widget, Dt.Point, tuple[int]]]
        liste contenant les éléments à mettre à jour
    """

    def __init__(self, window, ctrl_type : int, game_type : bool) -> None :
        """
        Initialise une instance de Controller

        Parameters
        ----------
        window : Window
            la fenêtre de l'application
        type : int 
            le type du controlleur
        """
        self._type : int = ctrl_type
        self._game_type : bool = game_type
        self._window = window
        self._animate : bool = False
        self._to_animate : list[tuple[Wdgt.Widget, Dt.Point, tuple[int]]] = []

    @property
    def window(self) :
        """Renvoie la fenêtre de l'application"""
        return self._window

    @property
    def type(self) -> int :
        """Renvoie le type du controlleur"""
        return self._type

    @property
    def is_in_animation(self) -> bool :
        """
        Renvoie vrai si le controlleur est encore en train de mettre à jour
        des éléments de la page controllée
        """
        return self._animate

    def clear_animations(self) -> None :
        """Retire de la liste tous les éléments qui sont mis à jour"""
        self._to_animate.clear()

    @abstractmethod
    def handle_mouse_motion(self, event) -> None :
        """Gère les mouvements de la souris"""
        ...

    @abstractmethod
    def handle_mouse_click(self, event) -> None :
        """Gère les cliques de la souris"""
        ...

    @abstractmethod
    def handle_key_pressed(self, event) -> None :
        """Gère les entrées sur le clavier"""
        ...

    def update(self) -> None :
        """Met à jour les éléments de la liste 'to_animate'"""
        verif = 0
        for widget, dest, direction in self._to_animate :
            widget.set_position(Dt.Point(widget.position.x + direction[0], widget.position.y + direction[1]))
            widget.display(self.window)
            if (abs(dest.x - widget.position.x) <= 10 and abs(dest.y - widget.position.y) <= 10) :
                widget.set_position(dest)
                verif += 1
        self._animate = verif != len(self._to_animate)
        if not self._animate :
            self.clear_animations()

        for widget, dest, direction in self._to_animate :
            if widget.position == dest :
                verif += 1
    
    def handle(self, event) -> None :
        """Gère les événements qui ont lieu dans la fenêtre de l'application"""
        match event.type :
            case Pg.MOUSEMOTION :
                self.handle_mouse_motion(event)
            case Pg.MOUSEBUTTONDOWN :
                self.handle_mouse_click(event)
            case Pg.KEYDOWN :
                self.handle_key_pressed(event)
