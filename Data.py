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
            return self.x == __value[0] and self.y == __value[1]

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
    DEFAULT_WINDOW_HEIGHT : int = 640
    DEFAULT_BOARD_DIMENSIONS : int = 640
    DEFAULT_GRID_DIMENSIONS : int = 5
    # DEFAULT_GRID_DIMENSIONS : int = 8
    DEFAULT_PIECE_DIMENSIONS : int = 60
    DEFAULT_TILE_DIMENSIONS : int = DEFAULT_BOARD_DIMENSIONS // DEFAULT_GRID_DIMENSIONS
    DEFAULT_TILE_OFFSET : int = (DEFAULT_TILE_DIMENSIONS - DEFAULT_PIECE_DIMENSIONS) / 2
    DEFAULT_BOARD_FEN : str = "rnbqk/ppppp/5/PPPPP/RNBQK"
    # DEFAULT_BOARD_FEN : str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/R3K2R"
    DEFAULT_CASTLING_RIGHTS : str = "KQ|kq"
    DEFAULT_FIRST_PLAYER : int = 0
    DEFAULT_FEN : str = f"{DEFAULT_BOARD_FEN} {str(DEFAULT_FIRST_PLAYER)} {DEFAULT_CASTLING_RIGHTS}"
    DEFAULT_PIECES_DIRECTIONS : dict[str : list[tuple[int]]] = {\
        "pawn" : [[(-2, 0), (-1, 0), (-1, 1), (-1, -1)], [(2, 0), (1, 0), (1, 1), (1, -1)]], \
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

class ButtonType :
    UP_ANIMATION : int = 0
    DOWN_ANIMATION : int = 1
    NO_ANIMATION : int  = 2

class MoveType :
    DEFAULT : int = 0
    PROMOTION : int = 1
    CASTLING : int = 2
    EN_PASSANT : int = 3

##################################### Ia Data ########################################################

# This section is inspired by the work of famous polish chess player Tomasz Michniewski
# The idea is to create tables that represent the value of a type of piece in the board given its position



PIECE_VALUES = [None, 100, 300, 300, 500, 900, 0]   #maps out the values of the pieces.
                                                    # by default in the chess library these are the values chess.PAWN = 1, chess.KNIGHT= 2, chess.BISHOP= 3, chess.ROOK= 4, chess.QUEEN= 5, chess.KING= 6
                                                    #this is why the index 0 is None
                                                    #We can get then simply get the value of a piece with PIECE_VALUES[piece.piece_type]

PIECE_TABLES_WHITE = [[  0,  0,  0,  0,  0,         #PAWN
                        50, 50, 50, 50, 50,         #a pawn is basically a lot stronger in the middle since chess is about controlling the center and the board
                        10, 15, 20, 15, 10,         #and the closer it gets to promotion the higher the value
                         5, 10,-10, 10,  5,
                         0,  0,  0,  0,  0],

                      [-50, -40, -30, -40, -50,     #KNIGHT
                       -15,   0,   5,   0, -15,
                         0,  15,  20,  15,   0,
                       -15,   0,   5,   0, -15,
                       -50, -40, -30, -40, -50],

                       [-20, -10, -10, -10, -20,     #BISHOP
                        -10,   0,   5,   0, -10,
                          0,   5,  15,   5,   0,
                        -10,   0,   5,   0, -10,
                        -20, -10, -10, -10, -20],

                        [ 0,   0,   0,   0,   0,     #ROOK
                         -5,  10,  10,  10,  -5,
                         -5,   0,   0,   0,  -5,
                         -5,   0,   0,   0,  -5,
                          0,   0,   5,   0,   0],

                       [-20, -10,  -5, -10, -20,     #QUEEN
                         -5,   5,   5,   5,  -5,
                          0,  10,  10,  10,   0,
                         -5,   5,   5,   5,  -5,
                        -20, -10,  -5, -10, -20],

                       [-30, -40,  -50, -40, -30,   #KING MIDDLE GAME
                        -15, -10,   -5, -10, -15,   # A king is safer when in castled in the middle game but we want to activate it in the end game since there is no more piece that can threaten it so we create
                          5,   0,    0,   0,   5,   # two different tables. In the end game the kin is stronger when controlling the center.
                         15,  10,    5,  10,  15,
                         20,  30,   10,  30,  20],

                       [-30, -40,  -50, -40, -30,   #KING END GAME
                        -15, -10,    5, -10, -15,
                          5,  10,   20,  10,   5,
                        -15, -10,    5, -10, -15,
                        -30, -40,  -50, -40, -30]]
# PIECE_TABLES_WHITE = [[0,  0,  0,  0,  0,  0,  0,  0,    #PAWN
#                 50, 50, 50, 50, 50, 50, 50, 50,    #a pawn is basically a lot stronger in the middle since chess is about controlling the center and the board
#                 10, 10, 20, 30, 30, 20, 10, 10,    #and the closer it gets to promotion the higher the value
#                 5,  5, 10, 25, 25, 10,  5,  5,
#                 0,  0,  0, 20, 20,  0,  0,  0,
#                 5, -5,-10,  0,  0,-10, -5,  5,
#                 5, 10, 10,-20,-20, 10, 10,  5,
#                 0,  0,  0,  0,  0,  0,  0,  0],

#                 [-50,-40,-30,-30,-30,-30,-40,-50,   #KNIGHT
#                 -40,-20,  0,  0,  0,  0,-20,-40,
#                 -30,  0, 10, 15, 15, 10,  0,-30,
#                 -30,  5, 15, 20, 20, 15,  5,-30,
#                 -30,  0, 15, 20, 20, 15,  0,-30,
#                 -30,  5, 10, 15, 15, 10,  5,-30,
#                 -40,-20,  0,  5,  5,  0,-20,-40,
#                 -50,-40,-30,-30,-30,-30,-40,-50],

#                 [-20,-10,-10,-10,-10,-10,-10,-20,   #BISHOP
#                 -10,  0,  0,  0,  0,  0,  0,-10,
#                 -10,  0,  5, 10, 10,  5,  0,-10,
#                 -10,  5,  5, 10, 10,  5,  5,-10,
#                 -10,  0, 10, 10, 10, 10,  0,-10,
#                 -10, 10, 10, 10, 10, 10, 10,-10,
#                 -10,  5,  0,  0,  0,  0,  5,-10,
#                 -20,-10,-10,-10,-10,-10,-10,-20],


#                 [0,  0,  0,  0,  0,  0,  0,  0,     #ROOK
#                 5, 10, 10, 10, 10, 10, 10,  5,
#                 -5,  0,  0,  0,  0,  0,  0, -5,
#                 -5,  0,  0,  0,  0,  0,  0, -5,
#                 -5,  0,  0,  0,  0,  0,  0, -5,
#                 -5,  0,  0,  0,  0,  0,  0, -5,
#                 -5,  0,  0,  0,  0,  0,  0, -5,
#                 0,  0,  0,  5,  5,  0,  0,  0],


#                 [-20,-10,-10, -5, -5,-10,-10,-20,   #QUEEN
#                 -10,  0,  0,  0,  0,  0,  0,-10,
#                 -10,  0,  5,  5,  5,  5,  0,-10,
#                 -5,  0,  5,  5,  5,  5,  0, -5,
#                 0,  0,  5,  5,  5,  5,  0, -5,
#                 -10,  5,  5,  5,  5,  5,  0,-10,
#                 -10,  0,  5,  0,  0,  0,  0,-10,
#                 -20,-10,-10, -5, -5,-10,-10,-20],


#                 [-30,-40,-40,-50,-50,-40,-40,-30,   #KING MIDDLE GAME
#                 -30,-40,-40,-50,-50,-40,-40,-30,    # A king is safer when in castled in the middle game but we want to activate it in the end game since there is no more piece that can threaten it so we create
#                 -30,-40,-40,-50,-50,-40,-40,-30,    # two different tables. In the end game the kin is stronger when controlling the center.
#                 -30,-40,-40,-50,-50,-40,-40,-30,
#                 -20,-30,-30,-40,-40,-30,-30,-20,
#                 -10,-20,-20,-20,-20,-20,-20,-10,
#                 20, 20,  0,  0,  0,  0, 20, 20,
#                 20, 30, 10,  0,  0, 10, 30, 20],

#                 [-50,-40,-30,-20,-20,-30,-40,-50,   #KING END GAME
#                 -30,-20,-10,  0,  0,-10,-20,-30,
#                 -30,-10, 20, 30, 30, 20,-10,-30,
#                 -30,-10, 30, 40, 40, 30,-10,-30,
#                 -30,-10, 30, 40, 40, 30,-10,-30,
#                 -30,-10, 20, 30, 30, 20,-10,-30,
#                 -30,-30,  0,  0,  0,  0,-30,-30,
#                 -50,-30,-30,-30,-30,-30,-30,-50]]

KING_MIDDLE_GAME = 5    #index of the table
KING_END_GAME = 6       #index of the table


# These values are for white, we can get the same values for black by simply mirroring these
def mirror_table(lst, row_size=5):
    """rotates two times the bord by 90 degrees"""
    lst_copy = lst.copy()
    for _ in range(2):
        lst_copy = [lst_copy[j] for i in range(row_size-1, -1, -1) for j in range(i, len(lst_copy), row_size)]
    return lst_copy


PIECE_TABLES_BLACK = [mirror_table(table, 5) for table in PIECE_TABLES_WHITE]