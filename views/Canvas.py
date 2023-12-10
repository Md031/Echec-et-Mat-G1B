from abc import abstractmethod, ABC

class Canvas(ABC) :
    """
    Représente une page de l'application

    Attributes
    ----------
    type : int
        le type de la page
    """

    def __init__(self, type : int) -> None :
        """
        Initialise une instance de Canvas

        Parameters
        ----------
        type : int
            le type de la page
        """
        self._type : int = type

    @property
    def canvas_type(self) -> int :
        """Renvoie le type de la page"""
        return self._type

    @abstractmethod
    def display(self, window) -> None :
        """
        Affiche le contenu de la page

        Parameters
        ----------
        window : Window
            la fenêtre sur laquelle sera affiché la page
        """