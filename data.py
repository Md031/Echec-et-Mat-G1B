import pygame as pg
import chess as ch

def convert_coordinates(pos : tuple[int] | str) -> tuple[int] | str :
    if isinstance(pos, tuple) :
        row, col = pos
        return chr(ord("a") + col) + str(Utils.DEFAULT_GRID_DIMENSIONS - row)
    else :
        return (Utils.DEFAULT_GRID_DIMENSIONS - int(pos[1]), ord(pos[0]) - ord("a"))

class Colors :
    RED : pg.Color = pg.Color(255, 0, 0)
    BLUE : pg.Color = pg.Color(0, 0, 255)
    GREEN : pg.Color = pg.Color(0, 255, 0)
    BROWN : pg.Color = pg.Color(88, 41, 0)
    BEIGE : pg.Color = pg.Color(245, 245, 220)
    WHITE : pg.Color = pg.Color(255, 255, 255)
    BLACK : pg.Color = pg.Color(0, 0, 0)
    YELLOW : pg.Color = pg.Color(241, 196, 15)
    PURPLE : pg.Color = pg.Color(125, 60, 152)

class Utils :
    DEFAULT_WINDOW_WIDTH : int = 800
    DEFAULT_WINDOW_HEIGHT : int = 640
    DEFAULT_BOARD_DIMENSIONS : int = 640
    DEFAULT_GRID_DIMENSIONS : int = 8
    DEFAULT_PIECE_DIMENSIONS : int = 60
    DEFAULT_TILE_DIMENSIONS : int = DEFAULT_BOARD_DIMENSIONS // DEFAULT_GRID_DIMENSIONS
    DEFAULT_TILE_OFFSET : int = (DEFAULT_TILE_DIMENSIONS - DEFAULT_PIECE_DIMENSIONS) / 2

class State :
    ONGOING : int = 0
    CHECK : int = 1
    CHECKMATE : int = 2
    STALEMATE : int = 3
    DRAW : int = 4

class ButtonType :
    UP_ANIMATION : int = 0
    DOWN_ANIMATION : int = 1
    NO_ANIMATION : int  = 2

class MoveType :
    DEFAULT : int = 0
    DROP : int = 1
    PROMOTION : int = 2
    CASTLING : int = 3
    EN_PASSANT : int = 4

class Move :
    movement : ch.Move = None
    direction : tuple[int]
    move_type : int = MoveType.DEFAULT 

##################################### Ia Data ########################################################

# This section is inspired by the work of famous polish chess player Tomasz Michniewski
# The idea is to create tables that represent the value of a type of piece in the board given its position



PIECE_VALUES = [100, 300, 300, 500, 900, 0]   #maps out the values of the pieces.
                                                    # by default in the chess library these are the values chess.PAWN = 0, chess.KNIGHT= 1, chess.BISHOP= 2, chess.ROOK= 3, chess.QUEEN= 4, chess.KING= 5
                                                    #this is why the index 0 is None
                                                    #We can get then simply get the value of a piece with PIECE_VALUES[piece.piece_type]

PIECE_TABLES_WHITE = [[0,  0,  0,  0,  0,  0,  0,  0,    #PAWN
                50, 50, 50, 50, 50, 50, 50, 50,    #a pawn is basically a lot stronger in the middle since chess is about controlling the center and the board
                10, 10, 20, 30, 30, 20, 10, 10,    #and the closer it gets to promotion the higher the value
                5,  5, 10, 25, 25, 10,  5,  5,
                0,  0,  0, 20, 20,  0,  0,  0,
                5, -5,-10,  0,  0,-10, -5,  5,
                5, 10, 10,-20,-20, 10, 10,  5,
                0,  0,  0,  0,  0,  0,  0,  0],

                [-50,-40,-30,-30,-30,-30,-40,-50,   #KNIGHT
                -40,-20,  0,  0,  0,  0,-20,-40,
                -30,  0, 10, 15, 15, 10,  0,-30,
                -30,  5, 15, 20, 20, 15,  5,-30,
                -30,  0, 15, 20, 20, 15,  0,-30,
                -30,  5, 10, 15, 15, 10,  5,-30,
                -40,-20,  0,  5,  5,  0,-20,-40,
                -50,-40,-30,-30,-30,-30,-40,-50],

                [-20,-10,-10,-10,-10,-10,-10,-20,   #BISHOP
                -10,  0,  0,  0,  0,  0,  0,-10,
                -10,  0,  5, 10, 10,  5,  0,-10,
                -10,  5,  5, 10, 10,  5,  5,-10,
                -10,  0, 10, 10, 10, 10,  0,-10,
                -10, 10, 10, 10, 10, 10, 10,-10,
                -10,  5,  0,  0,  0,  0,  5,-10,
                -20,-10,-10,-10,-10,-10,-10,-20],


                [0,  0,  0,  0,  0,  0,  0,  0,     #ROOK
                5, 10, 10, 10, 10, 10, 10,  5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                0,  0,  0,  5,  5,  0,  0,  0],


                [-20,-10,-10, -5, -5,-10,-10,-20,   #QUEEN
                -10,  0,  0,  0,  0,  0,  0,-10,
                -10,  0,  5,  5,  5,  5,  0,-10,
                -5,  0,  5,  5,  5,  5,  0, -5,
                0,  0,  5,  5,  5,  5,  0, -5,
                -10,  5,  5,  5,  5,  5,  0,-10,
                -10,  0,  5,  0,  0,  0,  0,-10,
                -20,-10,-10, -5, -5,-10,-10,-20],


                [-30,-40,-40,-50,-50,-40,-40,-30,   #KING MIDDLE GAME
                -30,-40,-40,-50,-50,-40,-40,-30,    # A king is safer when in castled in the middle game but we want to activate it in the end game since there is no more piece that can threaten it so we create
                -30,-40,-40,-50,-50,-40,-40,-30,    # two different tables. In the end game the kin is stronger when controlling the center.
                -30,-40,-40,-50,-50,-40,-40,-30,
                -20,-30,-30,-40,-40,-30,-30,-20,
                -10,-20,-20,-20,-20,-20,-20,-10,
                20, 20,  0,  0,  0,  0, 20, 20,
                20, 30, 10,  0,  0, 10, 30, 20],

                [-50,-40,-30,-20,-20,-30,-40,-50,   #KING END GAME
                -30,-20,-10,  0,  0,-10,-20,-30,
                -30,-10, 20, 30, 30, 20,-10,-30,
                -30,-10, 30, 40, 40, 30,-10,-30,
                -30,-10, 30, 40, 40, 30,-10,-30,
                -30,-10, 20, 30, 30, 20,-10,-30,
                -30,-30,  0,  0,  0,  0,-30,-30,
                -50,-30,-30,-30,-30,-30,-30,-50]]

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