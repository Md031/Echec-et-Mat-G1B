import Data as Dt
import copy
from abc import abstractmethod, ABC

class Piece(ABC) :
    """
    Représente une pièce dans le jeu d'échecs

    Attributes
    ----------
    name : str
        nom de la pièce
    symbole : str
        symbole représentant la pièce dans la notation san (Standard Algebric Notation)
    position : Dt.Point
        position de la pièce sur le plateau de jeu
    owner : int
        numéro du joueur a qui appartient la pièce
    image_filename : str
        chemin vers le fichier .png représentant la pièce
    icon : str
        icône de la pièce 
    """

    def __init__(self, position : Dt.Point, owner : int, image_type : str, name : str,
    symbol : str, icon : str) -> None :
        """
        Initialise une instance de Piece

        Parameters
        ----------
        position : Dt.Point
            la position de la pièce sur le plateau
        owner : int
            le numéro du joueur a qui appartient la pièce
        image_type : str
            le style de l'image représentant la pièce
        name : str
            le nom de la pièce
        symbol : str
            le symbole représentant la pièce dans la notation san
        icon : str
            l'icône de la pièce
        """
        self._name  : str = name
        self._symbol : str = symbol
        self._position : Dt.Point = position
        self._owner  : int = owner
        self._image_filename : str = f"images/{image_type}/W{self.name}.png" if self.owner == 0 \
            else f"images/{image_type}/B{self.name}.png"
        self._icon : str = icon

    ###########
    # GETTERS #
    ###########
    @property
    def name(self) -> str :
        """Renvoie le nom de la pièce"""
        return self._name

    @property
    def symbol(self) -> str :
        """Renvoie le symbole de la pièce"""
        return self._symbol

    @property
    def position(self) -> Dt.Point :
        """Renvoie la position de la pièce sur le plateau de jeu"""
        return self._position

    @property
    def chess_positon(self) -> Dt.Point :
        """Renvoie la position de la pièce sur le plateau en notation d'échecs (ex : f5)"""
        return Dt.convert_coordinates(self.position)

    @property
    def owner(self) -> int :
        """Renvoie le joueur à qui appartient la pièce"""
        return self._owner

    @property
    def image_filename(self) -> str :
        """Renvoie le chemin vers le fichier .png représentant la pièce"""
        return self._image_filename

    @property
    def icon(self) -> str :
        """Renvoie l'icône de la pièce"""
        return self._icon

    ###########
    # SETTERS #
    ###########
    def set_position(self, position : Dt.Point) -> None :
        """
        Modifie la position de la pièce sur le plateau de jeu

        Parameters
        ----------
        position : Dt.Point
            la nouvelle positon de la pièce
        """
        self._position = position

    ###################
    # OTHER FUNCTIONS #
    ###################
    @abstractmethod
    def available_actions(self, game) -> list[str] :
        """Renvoie une liste de toutes les actions possibles d'une pièce sur le plateau de jeu"""

    @abstractmethod
    def is_possible_move(self, dest : Dt.Point | list[Dt.Point], 
    direction : tuple[int], game) -> bool :
        ...

    def __str__(self) -> str : 
        return f"{self.icon} ({self.name}) | pos : {self.chess_positon} {self.position} | owner : {self.owner}"

    def __repr__(self) -> str : return str(self)

    def __eq__(self, __value: object) -> bool :
        if isinstance(__value, Piece) :
            return (__value.name == self.name and __value.position == self.position
                and __value.owner == self.owner)
        else :
            return False

class Pawn(Piece) :
    """Représente un pion dans le jeu d'échecs"""

    def __init__(self, position : Dt.Point, owner : int, image_type : str = "classic", name : str = "pawn",
    symbol : str = "", icon : str = "♙") -> None :
        """
        Initialise une instance de Pawn 
        (voir contstructeur de la classe "Piece")
        """
        super().__init__(position, owner, image_type, name, symbol, icon)
        self.__double_start : bool = True

    @property
    def can_double_start(self) -> bool :
        """Permet de savoir si le pion a encore le droit d'avancer de deux cases"""
        return self.__double_start

    def set_double_start(self, value : bool) -> None :
        """
        Donne ou retire au pion le droit d'avancer de deux cases

        Parameters
        ----------
        value : bool 
            la valeur booléenne à attribuer
        """
        self.__double_start = value 

    def available_actions(self, game) -> list[str] :
        """Renvoie les positions atteignables par le pion sur le plateau de jeu"""
        actions : list[str] = []
        dest : Dt.Point = None
        directions : list[tuple[int]] = Dt.Utils.DEFAULT_PIECES_DIRECTIONS[self.name][self.owner]
        for direction in directions :
            dest = self.position + direction
            if self.is_possible_move(dest, direction, game) :
                actions.append(self.chess_positon + Dt.convert_coordinates(dest))
        return actions

    def is_possible_move(self, dest : Dt.Point | list[Dt.Point], 
    direction : tuple[int], game) -> bool :
        if dest in game.board :
            dest_owner : int | None = game.board[dest].owner if game.board[dest] else None
            if direction in [(-2, 0), (2, 0)] : 
                return self._check_double_start(dest_owner, game)
            elif direction in [(-1, 1), (1, 1), (-1, -1), (1, -1)] : 
                return self._check_capture(dest_owner, direction, game)
            else : 
                return dest_owner is None
        return False

    def _check_double_start(self, dest_owner : int, game) -> bool :
        tmp = [game.board[self.position + (-1, 0)], 
            game.board[self.position + (1, 0)]]
        return (self.can_double_start and dest_owner is None and 
        ((tmp[0] is None and self.owner == 0) or (tmp[1] is None and self.owner == 1)))

    def _check_capture(self, dest_owner : int, direction : tuple[int], game) -> bool :
        if dest_owner is None :
            dest : Dt.Point = self.position + (0, direction[1])
            piece : Piece = game.board[dest]
            move = game.get_last_move(piece)
            if move is not None :
                return (isinstance(piece, Pawn) and piece.owner != self.owner
                and not move.piece_moved.can_double_start 
                and move.dest_pos - move.start_pos in [(-2, 0), (2, 0)])
        else :
            return dest_owner != self.owner
        return False

class Knight(Piece) :
    """Représente un cavalier dans le jeu d'échecs"""

    def __init__(self, position : Dt.Point, owner : int, image_type : str = "classic", name : str = "knight",
    symbol : str = "N", icon : str = "♘") -> None :
        """
        Initialise une instance de Knight 
        (voir contstructeur de la classe "Piece")
        """
        super().__init__(position, owner, image_type, name, symbol, icon)

    def available_actions(self, game) -> list[str] :
        """Renvoie les positions atteignables par le cavalier sur le plateau de jeu"""
        actions : list[str] = []
        dest : Dt.Point = None
        directions : list[tuple[int]] = Dt.Utils.DEFAULT_PIECES_DIRECTIONS[self.name]
        for direction in directions :
            dest = self.position + direction
            if self.is_possible_move(dest, None, game) :
                actions.append(self.chess_positon + Dt.convert_coordinates(dest))
        return actions

    def is_possible_move(self, dest : Dt.Point | list[Dt.Point], 
    direction : tuple[int], game) -> bool :
        return (dest in game.board and (not game.board[dest] 
        or game.board[dest].owner != self.owner))

class Bishop(Piece) :
    """Représente un fou dans le jeu d'échecs"""

    def __init__(self, position : Dt.Point, owner : int, image_type : str = "classic", name : str = "bishop",
    symbol : str = "B", icon : str = "♗") -> None :
        """
        Initialise une instance de Bishop 
        (voir contstructeur de la classe "Piece")
        """
        super().__init__(position, owner, image_type, name, symbol, icon)

    def available_actions(self, game) -> list[str] :
        """Renvoie les positions atteignables par le fou sur le plateau de jeu"""
        actions : list[str] = []
        directions : list[tuple[int]] = Dt.Utils.DEFAULT_PIECES_DIRECTIONS[self.name]
        available_directions : list[bool] = [True] * len(directions)
        dests : list[Dt.Point] = [copy.copy(self.position) for i in range(len(directions))]
        while available_directions.count(False) != len(directions) :
            for i in range(len(directions)) :
                dest, direction, available = dests[i], directions[i], available_directions[i]
                if available and self.is_possible_move(dest, direction, game) :
                    actions.append(self.chess_positon + Dt.convert_coordinates(dests[i]))
                    dest_owner : int = game.board[dest].owner if game.board[dest] else None
                    if dest_owner is not None :
                        available_directions[i] = False
                else :
                    available_directions[i] = False
        return actions

    def is_possible_move(self, dest : Dt.Point | list[Dt.Point], 
    direction : tuple[int], game) -> bool :
        dest += direction
        return (dest in game.board and (game.board[dest] is None 
        or game.board[dest].owner != self.owner))

class Rook(Piece) :
    """Représente une tour dans le jeu d'échecs"""

    def __init__(self, position : Dt.Point, owner : int, image_type : str = "classic", name : str = "rook",
    symbol : str = "R", icon : str = "♖") -> None :
        """
        Initialise une instance de Rook 
        (voir contstructeur de la classe "Piece")
        """
        super().__init__(position, owner, image_type, name, symbol, icon)

    def available_actions(self, game) -> list[str] :
        """Renvoie les positions atteignables par la tour sur le plateau de jeu"""
        return Bishop.available_actions(self, game)

    def is_possible_move(self, dest: Dt.Point | list[Dt.Point], 
    direction: tuple[int], game) -> bool:
        return Bishop.is_possible_move(self, dest, direction, game)

class Queen(Piece) :
    """Représente une reine dans le jeu d'échecs"""

    def __init__(self, position : Dt.Point, owner : int, image_type : str = "classic", name : str = "queen", \
    symbol : str = "Q", icon : str = "♕") -> None :
        """
        Initialise une instance de Queen 
        (voir contstructeur de la classe "Piece")
        """
        super().__init__(position, owner, image_type, name, symbol, icon)

    def available_actions(self, game) -> list[str] :
        """Renvoie les positions atteignables par la reine sur le plateau de jeu"""
        return Bishop.available_actions(self, game)

    def is_possible_move(self, dest: Dt.Point | list[Dt.Point], 
    direction: tuple[int], game) -> bool:
        return Bishop.is_possible_move(self, dest, direction, game)

class King(Piece) :
    """Représente une reine dans le jeu d'échecs"""

    def __init__(self, position : Dt.Point, owner : int, image_type : str = "classic", name : str = "king", \
    symbol : str = "K", icon : str = "♔") -> None :
        """
        Initialise une instance de King
        (voir contstructeur de la classe "Piece")
        """
        super().__init__(position, owner, image_type, name, symbol, icon)

    def available_actions(self, game) -> list[str] :
        """Renvoie les positions atteignables par le roi sur le plateau de jeu"""
        available_moves : list[str] = Knight.available_actions(self, game)
        castling_rights : str = game.activer_player_castling_rights
        if castling_rights is not None :
            king_side  : list[Dt.Point] = self.get_castling_pos(king_side = True)
            queen_side : list[Dt.Point] = self.get_castling_pos(king_side = False)
            moves : list[str] = [
                self.check_castling(movements, side if self.owner == 1 else side.upper(), 
                    castling_rights, game) 
                for movements, side in zip([king_side, queen_side], ["k", "q"]) 
            ]
            for move in moves :
                if move is not None :
                    available_moves.append(move)
        return available_moves

    def get_castling_pos(self, king_side : bool) -> list[Dt.Point] :
        start, end, step = (1, 3, 1) if king_side else  (-1, -4, -1)
        return [self.position + (0, i) for i in range(start, end, step)]

    def is_possible_move(self, dest : Dt.Point | list[Dt.Point], 
    direction : tuple[int], game) -> bool :
        if direction not in [(0, 2), (0, -2)] :
            return Knight.is_possible_move(self, dest, direction, game)
        else :
            return dest in game.board and game.board[dest] is None

    def check_castling(self, movements : list[Dt.Point], side : bool, castling_rights : str, game) -> str :
        can_castle : bool = True
        for pos in movements :
                if not self.is_possible_move(pos, None, game) :
                    can_castle = False
                    break
        if can_castle and side in castling_rights :
            dest : str = Dt.convert_coordinates(Dt.Point(self.position.x, movements[-1].y))
            return self.chess_positon + dest
