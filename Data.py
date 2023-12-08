import pygame as Pg
import copy

class Point :
    def __init__(self, x : int | float, y : int | float) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, __value : object) -> bool :
        if isinstance(__value, Point) :
            return self.x == __value.x and self.y == __value.y
        elif isinstance(__value, tuple) or isinstance(__value, list) :
            return self.x == __value[0] and self.x == __value[1]

    def __copy__(self) :
        return Point(self.x, self.y)

    def __add__(self, __value : object) :
        res : Point = copy.copy(self)
        res += __value
        return res

    def __iadd__(self, __value : object) :
        if isinstance(__value, Point) :
            self.x += __value.x
            self.y += __value.y
        elif isinstance(__value, tuple) or isinstance(__value, list) :
            self.x += __value[0]
            self.y += __value[1]
        return self

    def __sub__(self, __value : object) :
        res : Point = copy.copy(self)
        res -= __value
        return res

    def __isub__(self, __value : object) :
        if isinstance(__value, Point) :
            self.x -= __value.x
            self.y -= __value.y
        elif isinstance(__value, tuple) or isinstance(__value, list) :
            self.x -= __value[0]
            self.y -= __value[1]
        return self

def convert_coordinates(pos : Point | tuple[int] | str ) -> Point :
    if isinstance(pos, tuple) :
        row, col = pos
        return chr(ord("a") + col) + str(Utils.DEFAULT_GRID_DIMENSIONS - row)
    elif isinstance(pos, Point) :
        return chr(ord("a") + pos.y) + str(Utils.DEFAULT_GRID_DIMENSIONS - pos.x)
    else :
        # print(pos, Point(Utils.DEFAULT_GRID_DIMENSIONS - int(pos[1]), ord(pos[0]) - ord("a")))
        return Point(Utils.DEFAULT_GRID_DIMENSIONS - int(pos[1]), ord(pos[0]) - ord("a"))

class CanvasType :
    HOME : int = 0
    GAME : int = 1

class Colors :
    RED : Pg.Color = Pg.Color(255, 0, 0)
    BLUE : Pg.Color = Pg.Color(0, 0, 255)
    GREEN : Pg.Color = Pg.Color(0, 255, 0)
    BROWN : Pg.Color = Pg.Color(88, 41, 0)
    BEIGE : Pg.Color = Pg.Color(245, 245, 220)
    WHITE : Pg.Color = Pg.Color(255, 255, 255)
    BLACK : Pg.Color = Pg.Color(0, 0, 0)
    YELLOW : Pg.Color = Pg.Color(241, 196, 15)
    PURPLE : Pg.Color = Pg.Color(125, 60, 152)

class Utils :
    DEFAULT_WINDOW_WIDTH : int = 800
    DEFAULT_WINDOW_HEIGHT : int = 700
    DEFAULT_BOARD_DIMENSIONS : int = 640
    DEFAULT_GRID_DIMENSIONS : int = 8
    DEFAULT_PIECE_DIMENSIONS : int = 60
    DEFAULT_TILE_DIMENSIONS : int = DEFAULT_BOARD_DIMENSIONS // DEFAULT_GRID_DIMENSIONS
    DEFAULT_TILE_OFFSET : int = (DEFAULT_TILE_DIMENSIONS - DEFAULT_PIECE_DIMENSIONS) / 2
    DEFAULT_BOARD_FEN : str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
    DEFAULT_CASTLING_RIGHTS : str = "KQ|kq"
    DEFAULT_FIRST_PLAYER : int = 0
    DEFAULT_FEN : str = f"{DEFAULT_BOARD_FEN} {str(DEFAULT_FIRST_PLAYER)} {DEFAULT_CASTLING_RIGHTS}"
    DEFAULT_PIECES_DIRECTIONS : dict[str : list[tuple[int]]] = {\
        "pawn" : [[(-1, 0), (-2, 0), (-1, 1), (-1, -1)], [(1, 0), (2, 0), (1, 1), (1, -1)]], \
        "knight" : [(-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1)], \
        "bishop" : [(-1, 1), (1, 1), (1, -1), (-1, -1)], \
        "rook" : [(-1, 0), (0, 1), (1, 0), (0, -1)], \
        "queen" : [(-1, 0), (0, 1), (1, 0), (0, -1), (-1, 1), (1, 1), (1, -1), (-1, -1)], \
        "king" : [(-1, 0), (0, 1), (1, 0), (0, -1), (-1, 1), (1, 1), (1, -1), (-1, -1)]
    }

class State :
    ONGOING : int = 0
    CHECK : int = 1
    CHECKMATE : int = 2
    STALEMATE : int = 3
    RESIGNATION : int = 4

class MoveType :
    NORMAL : int = 0
    CAPTURE : int = 1
    CASTLING : int = 2
