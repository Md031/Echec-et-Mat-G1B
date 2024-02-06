# import pygame as Pg
import views.Tile as Tl
import views.PieceDisplayer as PieceD
import models.Board as Brd
import Data as Dt
import views.Widget as Wdgt

class BoardDisplayer(Wdgt.Widget) :
    """
    Représente l'affichage du plateau de jeu sur la fenêtre de l'application

    Attributes
    ----------
    board : Board
        le plateau de jeu à afficher
    grid : list[list[Tile]]
        l'affichae du plateau de jeu
    """

    def __init__(self, board : Brd.Board = None, position : Dt.Point = Dt.Point(0, 0)) -> None :
        """
        Initialise une instance de BoardDisplayer
        (voir constructeur de "Widget")
        """
        super().__init__(position, "board_displayer")
        self.__board : Brd.Board = board
        self.__grid : list[list[Tl.Tile]] = []
        if self.__board :
            self._init_grid()

    @property
    def grid(self) -> list[list[Tl.Tile]] :
        """Renvoie les cases affichées sur la fenêtres"""
        return self.__grid

    @property
    def position(self) -> Dt.Point :
        """Renvoie la position du plateau de jeu sur la fenêtre"""
        return self.__position

    def set_board(self, board : Brd.Board = None) -> None :
        """
        Change le plateau à afficher

        Parameters
        ----------
        board : Board
            le nouveau plateau à afficher
        """
        self.__board = board
        self.grid.clear()
        self._init_grid()

    def _init_grid(self) -> None :
        """Initialise l'affichage du plateu de jeu"""
        cmpt_tile : int = 0
        tile : Tl.Tile = None
        for i in range(Dt.Utils.DEFAULT_GRID_DIMENSIONS) :
            row : list[Tl.Tile] = []
            for j in range(Dt.Utils.DEFAULT_GRID_DIMENSIONS) :
                grid_position = Dt.Point(i, j)
                window_position = Dt.Point(j * Dt.Utils.DEFAULT_TILE_DIMENSIONS, i * Dt.Utils.DEFAULT_TILE_DIMENSIONS)
                piece = self.__board[i, j]
                if (i % 2 == 0 and j % 2 == 0) or (i % 2 != 0 and j % 2 != 0) :
                    tile = Tl.Tile(window_position, grid_position, Dt.Colors.BEIGE)
                else :
                    tile = Tl.Tile(window_position, grid_position, Dt.Colors.BROWN)

                if piece :
                    piece_position = Dt.Point(window_position.x + Dt.Utils.DEFAULT_TILE_OFFSET, \
                        window_position.y + Dt.Utils.DEFAULT_TILE_OFFSET)
                    tile.set_piece(PieceD.PieceDisplayer(piece_position, piece))
                row.append(tile)
                cmpt_tile += 1
            self.__grid.append(row)

    def __getitem__(self, pos : Dt.Point) -> Tl.Tile :
        return self.grid[pos.x][pos.y]

    def display(self, window) -> None :
        for tile in self :
            tile.display(window)

    def __contains__(self, point : Dt.Point | tuple[int]) -> bool : 
        if isinstance(point, Dt.Point) :
            return  super().position.x <= point.x <= super().position.x + Dt.Utils.DEFAULT_TILE_DIMENSIONS and \
                super().position.y <= point.x <= super().position.y + Dt.Utils.DEFAULT_TILE_DIMENSIONS
        else :
            return  super().position.x <= point[0] <= super().position.x + Dt.Utils.DEFAULT_TILE_DIMENSIONS and \
                super().position.y <= point[1] <= super().position.y + Dt.Utils.DEFAULT_TILE_DIMENSIONS

    def __str__(self) -> str :
        return str(self.__board)

    def __repr__(self) -> str :
        return str(self.__board)

    def __iter__(self) :
        self.__i : int = 0
        self.__j : int = -1
        return self

    def __next__(self) -> Tl.Tile :
        self.__j += 1
        if self.__j == len(self.grid[0]) :
            self.__j = 0
            self.__i += 1
        if self.__i == len(self.grid) :
            raise StopIteration
        tile : Tl.Tile = self[Dt.Point(self.__i, self.__j)]
        return tile