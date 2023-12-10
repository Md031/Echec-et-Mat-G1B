import Data as Dt
import models.Pieces as Pcs

class Board :
    """
    Représente le plateau du jeu d'échecs

    Attributes
    ----------
    pieces : list[list[Pcs.Pieces]]
        les pièces possédées par les joueurs présents sur le plateau de jeu
    grid : list[list[Pcs.Pieces | None]]
        matrice représentant le plateu de jeu
    """

    def __init__(self, board_fen : str = Dt.Utils.DEFAULT_BOARD_FEN) -> None :
        """
        Initialise une instance de Board

        Parameters
        ----------
        board_fen : str
            le plateau de jeu en notation fen (Forsyth-Edwards Notation)
        """
        self.__pieces : list[list[Pcs.Piece]] = [[], []]
        self.__grid : list[list[Pcs.Piece | None]] = []
        self._init(board_fen)

    ###########
    # GETTERS #
    ###########
    @property
    def fen(self) -> str :
        """Renvoie le plateu de jeu en notation fen"""
        fen : str = ""
        for row in self.grid :
            space : int = 0
            for piece in row :
                if piece :
                    space = 0
                    fen += piece.name[0].upper() if piece.owner == 0 else piece.name[0]
                else : 
                    space += 1
            fen += str(space) if space > 0 else ""
            fen += "/"
        return fen.strip("/")

    @property
    def grid(self) -> list[list[Pcs.Piece | None]] :
        """Renvoie la matrice représentant le plateau de jeu"""
        return self.__grid

    @property
    def size(self) -> tuple[int] : 
        """Renvoie les dimensions du plateau de jeu"""
        return len(self.grid), len(self.grid[0]) 

    def get_player_pieces(self, player : int) -> list[Pcs.Piece] : 
        """
        Renvoie une liste des pièces appartenant à un joueur

        Parameters
        ----------
        player : int
            le numéro du joueur
        """
        return self.__pieces[player]

    def __getitem__(self, pos : tuple[int] | Dt.Point | str) -> Pcs.Piece | None :
        if isinstance(pos, tuple) :
            return self.grid[pos[0]][pos[1]]
        elif isinstance(pos, str) :
            pos = Dt.convert_coordinates(pos)
        return self.grid[pos.x][pos.y]

    ###########
    # SETTERS #
    ###########
    def set_board(self, board_fen : str) -> None :
        """
        Modifie le plateau le plateau de jeu

        Parameters
        ----------
        board_fen : str
            le nouveau plateau de jeu en notation fen
        """
        self._init(board_fen)

    def _init(self, board_fen : str = Dt.Utils.DEFAULT_BOARD_FEN) -> None :
        """Initialise le plateau de jeu"""
        self.__pieces.clear()
        self.__grid.clear()
        self.__pieces = [[], []]
        self.__grid = []
        board_fen_list : list[str] = board_fen.split("/")

        row : int = 0 
        for a_list in board_fen_list :
            col : int = 0
            board_row : list[Pcs.Piece | None] = []
            for data in a_list :
                if data.isalpha() :
                    owner = 0 if data.isupper() else 1
                    piece : Pcs.Piece = None
                    position : Dt.Point = Dt.Point(row, col)

                    match data.upper() :
                        case "P" : piece = Pcs.Pawn(position, owner)
                        case "N" : piece = Pcs.Knight(position, owner)
                        case "B" : piece = Pcs.Bishop(position, owner)
                        case "R" : piece = Pcs.Rook(position, owner)
                        case "Q" : piece = Pcs.Queen(position, owner)
                        case "K" : piece = Pcs.King(position, owner)

                    self.__pieces[owner].append(piece)
                    board_row.append(piece)
                    col += 1
                elif data.isdigit() :
                    for i in range(int(data)) :
                        board_row.append(None)
                        col += 1
                
            self.__grid.append(board_row)
            row += 1

    ###################
    # OTHER FUNCTIONS #
    ###################
    def __contains__(self, coords : Dt.Point | str | tuple) -> bool :
        if isinstance(coords, Dt.Point) :
            return 0 <= coords.x < self.size[0] and 0 <= coords.y < self.size[1]
        elif isinstance(coords, tuple) :
            return 0 <= coords[0] < self.size[0] and 0 <= coords[1] < self.size[1]
        elif isinstance(coords, str) :
            coords = Dt.convert_coordinates(coords)
            return 0 <= coords[0] < self.size[0] and 0 <= coords[0] < self.size[1]

    def capture(self, piece : Pcs.Piece) -> None :
        """"""
        player_piece : list[Pcs.Piece] = self.player_pieces(piece.player)
        player_piece.pop(player_piece.index(piece))

    def __str__(self) -> str :
        str_board : str = ""
        for row in range(len(self.grid)) :
            for col in range(len(self.grid[0])) :
                position : Dt.Point = Dt.Point(row, col) 
                piece : Pcs.Piece | None = self[position]
                str_board += piece.icon + " " if piece else ". "
            str_board += "\n"
        return str_board.strip("\n")

    def __repr__(self) -> str : return str(self.__pieces)

    def __iter__(self) :
        self.__i : int = 0
        self.__j : int = 0
        return self

    def __next__(self) -> Pcs.Piece | None :
        piece : Pcs.Piece | None = self[self.__i, self.__j]
        self.__j += 1
        if self.__j == len(self.grid[0]) :
            self.__j = 0
            self.__i += 1
        if self.__i == len(self.grid) :
            raise StopIteration
        return piece
