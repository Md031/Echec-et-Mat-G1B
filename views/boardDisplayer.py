import chess as ch
import data as dt
import views.pieceDisplayer as pieceD
import views.tile as tl
import views.widget as wdgt

class BoardDisplayer(wdgt.Widget) :

    def __init__(self, board : ch.Board) -> None :
        super().__init__((0, 0), "BoardDisplayer")
        self.__grid : list[list[tl.Tile]] = []
        self.init_board(board)

    def init_board(self, board : ch.Board) -> None :
        for i in range(dt.Utils.DEFAULT_GRID_DIMENSIONS) :
            self.grid.append([])
            for j in range(dt.Utils.DEFAULT_GRID_DIMENSIONS) :
                tile : tl.Tile = self.create_tile(board, i, j)
                self.grid[-1].append(tile)

    def create_tile(self, board : ch.Board, col : int, row : int) -> tl.Tile :
        nb_square = 56 - 8 * col + row
        piece : ch.Piece = board.piece_at(nb_square)
        tile : tl.Tile = None
        tile_position : tuple[int] = (row * dt.Utils.DEFAULT_TILE_DIMENSIONS, 
            col * dt.Utils.DEFAULT_TILE_DIMENSIONS)
        if (col + row) % 2 == 0 :
            tile = tl.Tile(tile_position, (col, row), dt.Colors.BEIGE)
        else :
            tile = tl.Tile(tile_position, (col, row), dt.Colors.BROWN)
        if piece :
            tile.set_piece(pieceD.PieceDisplayer(piece, (col, row)))
        return tile

    @property
    def grid(self) -> list[list[tl.Tile]] : return self.__grid

    def reset(self) -> None : return super().reset()

    def display(self, window) -> None : 
        for tile in self : tile.display(window)

    def __getitem__(self, position : tuple[int]) -> tl.Tile :
        x, y = position
        return self.grid[x][y]

    def __contains__(self, position : tuple[int]) -> bool :
        x, y = position
        return (self.x < x < dt.Utils.DEFAULT_BOARD_DIMENSIONS 
            and self.y < y < dt.Utils.DEFAULT_BOARD_DIMENSIONS)

    def __iter__(self) :
        self.__i : int = 0
        self.__j : int = -1
        return self

    def __next__(self) -> tl.Tile :
        self.__j += 1
        if self.__j == dt.Utils.DEFAULT_GRID_DIMENSIONS :
            self.__j = 0
            self.__i += 1
        if self.__i == dt.Utils.DEFAULT_GRID_DIMENSIONS :
            raise StopIteration
        tile : tl.Tile = self[(self.__i, self.__j)]
        return tile

    def __str__(self) -> str :
        return f"{self.name}"
