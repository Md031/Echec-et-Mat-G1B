# import pygame as Pg
import views.Tile as Tl
import views.PieceDisplayer as PieceD
import models.Board as Brd
import Data as Dt

class BoardDisplayer() :
    def __init__(self, board : Brd.Board = None, position : Dt.Point = Dt.Point(0, 0)) -> None :
        self.__position : Dt.Point = position
        self.__board : Brd.Board = board
        self.__grid : list[list[Tl.Tile]] = []
        if self.__board :
            self._init_grid()

    @property
    def grid(self) -> list[list[Tl.Tile]] :
        return self.__grid

    @property
    def position(self) -> Dt.Point : return self.__position

    def set_board(self, board : Brd.Board = None) -> None :
        self.__board = board
        self._init_grid()

    def _init_grid(self) -> None :
        cmpt_tile : int = 0
        tile : Tl.Tile = None
        for i in range(Dt.Utils.DEFAULT_GRID_DIMENSIONS) :
            row = []
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
        for row in self.grid :
            for tile in row :
                tile.display(window)

    def __iter__(self) :
        self.__i : int = 0
        self.__j : int = 0
        return self

    def __next__(self) -> Tl.Tile :
        tile : Tl.Tile = self[Dt.Point(self.__i, self.__j)]
        self.__j += 1
        if self.__j == len(self.grid[0]) :
            self.__j = 0
            self.__i += 1
        if self.__i == len(self.grid) :
            raise StopIteration
        return tile
