import Data as Dt
import copy
from abc import ABC

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

    def __init__(self, position : Dt.Point, owner : int, image_type : str, name : str, \
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
    def available_actions(self, game) -> list[str] :
        """"""
        actions : list[str] = []
        directions : list[tuple[int]] = Dt.Utils.DEFAULT_PIECES_DIRECTIONS[self.name]
        dest : Dt.Point | list[Dt.Point] = None
        if self.name == "pawn" :
            for direction in directions[self.owner] :
                dest = copy.copy(self.position)
                dest += direction
                if dest in game.game :
                    if (direction == (-2, 0) or direction == (2, 0)) and self.can_double_start \
                    and game.game[dest] is None :
                        actions.append(self.chess_positon + Dt.convert_coordinates(dest))
                    elif direction != (1, 0) and direction != (-1, 0) and \
                    (direction[0] == -1 and self.owner == 0 or direction[0] == 1 and self.owner == 1) :
                        if game.game[dest] and game.game[dest].owner != self.owner :
                            actions.append(self.chess_positon + Dt.convert_coordinates(dest))
                    elif game.game[dest] is None :
                        actions.append(self.chess_positon + Dt.convert_coordinates(dest))
        elif self.name == "knight" or self.name == "king" :
            for direction in directions :
                dest : Dt.Point = copy.copy(self.position)
                dest += direction
                if dest in game.game and (game.game[dest] is None or game.game[dest].owner != self.owner) :
                    actions.append(self.chess_positon + Dt.convert_coordinates(dest))
        else :
            available_directions = [True] * len(directions)
            dest = [copy.copy(self.position) for i in range(len(directions))]
            while available_directions.count(False) != len(directions) :
                for i in range(len(dest)) :
                    available, direction = available_directions[i], directions[i]
                    if available :
                        dest[i] += direction
                        if dest[i] in game.game and (game.game[dest[i]] is None or \
                        game.game[dest[i]].owner != self.owner) :
                            actions.append(self.chess_positon + Dt.convert_coordinates(dest[i]))
                        else :
                            available_directions[i] = False
        return actions

    def __str__(self) -> str : 
        return f"{self.icon} ({self.name}) | pos : {self.chess_positon} {self.position} | owner : {self.owner}"

    def __repr__(self) -> str : return str(self)

    def __eq__(self, __value: object) -> bool :
        if isinstance(__value, Piece) :
            return (__value.name == self.name and __value.chess_positon == self.chess_positon \
                and __value.player == self.player)
        else :
            return False

class Pawn(Piece) :
    """Représente un pion dans le jeu d'échecs"""

    def __init__(self, position : Dt.Point, owner : int, image_type : str = "classic", name : str = "pawn", \
    symbol : str = "", icon : str = "♙") -> None :
        """
        Initialise une instance de Pawn 
        (voir contstructeur de la classe "Piece")
        """
        super().__init__(position, owner, image_type, name, symbol, icon)
        self.__double_start : bool = True

    ###########
    # GETTERS #
    ###########
    @property
    def can_double_start(self) -> bool :
        """Permet de savoir si le pion a encore le droit d'avancer de deux cases"""
        return self.__double_start

    ###########
    # SETTERS #
    ###########
    def give_up_double_start(self) -> None :
        """Retire au pion le droit d'avancer de deux cases"""
        self.__double_start = False

    ###################
    # OTHER FUNCTIONS #
    ###################
    def available_actions(self, game) -> list[str] :
        """Renvoie les positions atteignables par le pion sur le plateau de jeu"""
        return super().available_actions(game)

class Knight(Piece) :
    """Représente un cavalier dans le jeu d'échecs"""

    def __init__(self, position : Dt.Point, owner : int, image_type : str = "classic", name : str = "knight", \
    symbol : str = "N", icon : str = "♘") -> None :
        """
        Initialise une instance de Knight 
        (voir contstructeur de la classe "Piece")
        """
        super().__init__(position, owner, image_type, name, symbol, icon)

    def available_actions(self, game) -> list[str] :
        """Renvoie les positions atteignables par le cavalier sur le plateau de jeu"""
        return super().available_actions(game)

class Bishop(Piece) :
    """Représente un fou dans le jeu d'échecs"""

    def __init__(self, position : Dt.Point, owner : int, image_type : str = "classic", name : str = "bishop", \
    symbol : str = "B", icon : str = "♗") -> None :
        """
        Initialise une instance de Bishop 
        (voir contstructeur de la classe "Piece")
        """
        super().__init__(position, owner, image_type, name, symbol, icon)

    def available_actions(self, game) -> list[str] :
        """Renvoie les positions atteignables par le fou sur le plateau de jeu"""
        return super().available_actions(game)

class Rook(Piece) :
    """Représente une tour dans le jeu d'échecs"""

    def __init__(self, position : Dt.Point, owner : int, image_type : str = "classic", name : str = "rook", \
    symbol : str = "R", icon : str = "♖") -> None :
        """
        Initialise une instance de Rook 
        (voir contstructeur de la classe "Piece")
        """
        super().__init__(position, owner, image_type, name, symbol, icon)

    def available_actions(self, game) -> list[str] :
        """Renvoie les positions atteignables par la tour sur le plateau de jeu"""
        return super().available_actions(game)

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
        return super().available_actions(game)

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
        return super().available_actions(game)
