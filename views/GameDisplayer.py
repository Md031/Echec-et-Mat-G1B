import views.Canvas as Cnvs
import views.BoardDisplayer as BoardD
import models.Game as Gm
import Data as Dt 

class GameDisplayer(Cnvs.Canvas) :
    def __init__(self, type: int = Dt.CanvasType.GAME) -> None :
        super().__init__(type)
        self.__boardDisplayer : BoardD.BoardDisplayer = BoardD.BoardDisplayer()
        self.__game : Gm.Game = None

    @property
    def game(self) -> Gm.Game : return self.__game

    @property
    def baordDisplayer(self) -> BoardD.BoardDisplayer : return self.__boardDisplayer

    def get_tile(self, position : str | Dt.Point) :
        if isinstance(position, str) :
            position = Dt.convert_coordinates(position)
        return self.__boardDisplayer[position]

    def set_game(self, game : Gm.Game) :
        self.__game = game
        self.__boardDisplayer.set_board(self.__game.board)

    def display(self, window) -> None: self.__boardDisplayer.display(window)
