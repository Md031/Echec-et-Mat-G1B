import Data as Dt
from abc import abstractmethod, ABC

class Widget(ABC) :
    def __init__(self, position : Dt.Point, name : str) :
        self._position : Dt.Point = position
        self._name : str = name

    @property
    def position(self) -> Dt.Point : return self._position

    @property
    def name(self) -> str : return self._name

    def set_position(self, position : Dt.Point) -> None : self._position = position

    @abstractmethod
    def display(self, window) -> None :
        ...

    @abstractmethod
    def __str__(self) -> str :
        ...

    @abstractmethod
    def __contains__(self, coords : Dt.Point | str | tuple) -> bool :
        ...

    def __repr__(self) -> str : return str(self)
