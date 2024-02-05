import Data as Dt
from abc import abstractmethod, ABC

class Widget(ABC) :
    """
    Représente un élément se trouvant sur une des pages de l'application

    Attributes
    ----------
    position : Dt.Point
        la position de l'élément sur la fenêtre
    name : str
        le nom de l'élément
    """

    def __init__(self, position : Dt.Point, name : str) :
        """
        Initialise une instance de Widget

        Parameters
        ----------
        position : Dt.Point
        la position de l'élément sur la fenêtre
        name : str
            le nom de l'élément
        """
        self._position : Dt.Point = position
        self._name : str = name

    @property
    def position(self) -> Dt.Point :
        """Renvoie la position de l'élément sur la fenêtre"""
        return self._position

    @property
    def name(self) -> str :
        """Renvoei le nom de l'élément"""
        return self._name

    def set_position(self, position : Dt.Point) -> None : 
        """Modifie la position de l'élément sur la fenêtre"""
        self._position = position

    @abstractmethod
    def display(self, window) -> None :
        """
        Affiche l'élément sur la fenêtre

        Parameters :
            window : Window
                fenêtre sur laquelle sera affichée l'élément
        """
        ...

    @abstractmethod
    def __str__(self) -> str :
        ...

    @abstractmethod
    def __contains__(self, coords : Dt.Point | tuple) -> bool :
        ...

    def __repr__(self) -> str : return str(self)
