from abc import abstractmethod, ABC

class Widget(ABC) :

    def __init__(self, position : tuple[int], name : str) :
        self._position : tuple[int] = position
        self._name : str = name

    @property
    def position(self) -> tuple[int] : return self._position

    @property
    def x(self) -> int : return self.position[0]

    @property
    def y(self) -> int : return self.position[1]

    @property
    def name(self) -> str : return self._name

    def set_position(self, position : tuple[int]) -> None : self._position = position

    @abstractmethod
    def display(self, window) -> None :
        ...

    @abstractmethod
    def reset(self) -> None :
        ...

    @abstractmethod
    def __str__(self) -> str :
        ...

    @abstractmethod
    def __contains__(self, coords : tuple[int]) -> bool :
        ...

    def __repr__(self) -> str : return str(self)
