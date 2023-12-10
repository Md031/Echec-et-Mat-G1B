import views.Canvas as Cnvs
import views.BoardDisplayer as BoardD
import models.Game as Gm
import Data as Dt 

class GameDisplayer(Cnvs.Canvas) :
    """
    Représente la page du où se déroulera la partie d'échecs

    Attributes
    ----------
    boardDiplayer : BoardDisplayer
        l'affichage du plateau dee jeu
    game : Game
        la partie d'échecs à afficher
    """

    def __init__(self, type: int = Dt.CanvasType.GAME) -> None :
        """
        Initalise une instance de GameDisplayer
        (voir constructeur de la classe "Canvas")
        """
        super().__init__(type)
        self.__boardDisplayer : BoardD.BoardDisplayer = BoardD.BoardDisplayer()
        self.__game : Gm.Game = None

    @property
    def game(self) -> Gm.Game :
        """Renvoie la partie en cours"""
        return self.__game

    @property
    def baordDisplayer(self) -> BoardD.BoardDisplayer :
        """Renvoie l'affichage du plateau de jeu"""
        return self.__boardDisplayer

    def get_tile(self, position : str | Dt.Point) :
        """Permert de récupérer une dans cases dans l'affichage du plateau de jeu"""
        if isinstance(position, str) :
            position = Dt.convert_coordinates(position)
        return self.__boardDisplayer[position]

    def set_game(self, game : Gm.Game) :
        """Change la partie d'échecs à afficher"""
        self.__game = game
        self.__boardDisplayer.set_board(self.__game.board)

    def display(self, window) -> None : self.__boardDisplayer.display(window)
