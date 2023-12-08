from abc import abstractmethod, ABC

class Canvas(ABC) :
    def __init__(self, type : int) -> None: self._type : int = type

    @property
    def canvas_type(self) -> int : return self._type

    @abstractmethod
    def display(self, window) -> None :
        """méthode qui permet d'afficher ce que contient la vue"""