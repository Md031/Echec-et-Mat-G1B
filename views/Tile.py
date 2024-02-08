import pygame as Pg
import Data as Dt
import views.PieceDisplayer as PieceD
import models.Pieces as Pcs
import views.Widget as Wdgt

class Tile(Wdgt.Widget) :
    """
    Représente l'affichage d'une case du plateau de jeu sur la fenêtre de l'application

    Attributes
    ----------
    bg_color : Surface
        surface sur laqulle il y aura la couleur de fond de la case
    rect : Rect
        rectangle qui représentes les limites de la case sur la fenêtre
    grid_position : Dt.Point
        la position de la case sur le plateau de jeu
    color : Color
        la couleur de fond de la case
    pieceDisplayer : PieceDisplayer
        la pièce à afficher
    visited : bool
        booléen permettant de savoir si le curseur de la souris est passé sur la case
    clicked : bool
        booléen permettant de savoir si l'utilisateur a cliqué sur la case
    choice : bool
        booléen permettant de savoir si la case est une des destination possibles pour la pièce
        choisie par l'utilisateur
    """

    def __init__(self, position : Dt.Point, grid_position : Dt.Point, color : Pg.Color | str) -> None :
        """
        Initialise une instance de Tile
        (voir constructeur de "Widget")

        Parameters
        ----------
        position : Dt.Point
            position de la case sur la fenêtre
        grid_position : Dt.Point
            position de la case dans le plateau de jeu
        color : Color | str
            la couleur de fond de la case
        """
        super().__init__(position, "tile")
        self.__bg_color : Pg.Surface = Pg.Surface((Dt.Utils.DEFAULT_TILE_DIMENSIONS, Dt.Utils.DEFAULT_TILE_DIMENSIONS))
        self.__bg_color.fill(color)
        self.__rect = Pg.rect.Rect(super().position.x, super().position.y, \
            Dt.Utils.DEFAULT_TILE_DIMENSIONS, Dt.Utils.DEFAULT_TILE_DIMENSIONS)
        self.__grid_position : Dt.Point = grid_position
        self.__color : str | Dt.Point = color
        self.__pieceDisplayer : PieceD.PieceDisplayer = None
        self.__visited : bool = False
        self.__clicked : bool = False
        self.__choice : bool = False

    @property
    def position(self) -> Dt.Point :
        """Renvoie la position de la case sur la fenêtre"""
        return Dt.Point(self.__rect.center[0], self.__rect.center[1])

    @property
    def grid_position(self) -> Dt.Point :
        """Renvoie la position de la case dans le plateu de jeu"""
        return self.__grid_position

    @property
    def chess_position(self) -> str :
        """Renvoie la position de la case dans le plateu de jeu en notation d'échecs (ex : f5)"""
        return Dt.convert_coordinates(self.grid_position)

    @property
    def color(self) -> Pg.color :
        """Renvoie la couleur de fond de la case"""
        return self.__color

    @property
    def pieceDisplayer(self) -> PieceD.PieceDisplayer :
        """Renvoie l'affichage de la pièce'"""
        return self.__pieceDisplayer

    @property
    def piece(self) -> Pcs.Piece : 
        """Renvoie la pièce à afficher"""
        return self.__pieceDisplayer.piece if self.__pieceDisplayer else None

    @property
    def is_visited(self) -> bool :
        """Renvoie vrai si si le curseur de la souris est passé sur la case"""
        return self.__visited

    @property
    def is_clicked(self) -> bool :
        """Renvoie vrai si l'utilisateur a cliqué sur la case"""
        return self.__clicked

    @property
    def is_choice(self) -> bool :
        """
        Renvoie vrai si la case est une des destination possibles pour la pièce
        choisie par l'utilisateur
        """
        return self.__choice

    def set_piece(self, piece : PieceD.PieceDisplayer = None) -> None :
        """
        Change la pièce à afficher

        Parameters
        ----------
        piece : PieceDisplayer
            la nouvelle pi§ce à afficher
        """
        self.__pieceDisplayer = piece
        if self.pieceDisplayer :
            self.pieceDisplayer.set_position(self.position)

    def set_visited(self, value : bool) -> None :
        """Change la valeur du booléen gérant la présence du curseur de la souris sur la case"""
        self.__visited = value

    def set_clicked(self, value : bool = None) -> None : 
        """Change la valeur du booléen gérant le clique de la souris sur la case"""
        self.__clicked = not self.__clicked if value is None else value

    def set_choice(self, value : bool) -> None :
        """
        Change la valeur du booléen gérant la possibilité que la case soit une destination de la
        pièce choisie par l'utilisateur
        """
        self.__choice = value

    def __contains__(self, coords : Dt.Point | tuple[int]) -> bool : 
        if not isinstance(coords, Dt.Point) :
            coords = Dt.Point(coords[0], coords[1])
        return  super().position.x <= coords.x <= super().position.x + Dt.Utils.DEFAULT_TILE_DIMENSIONS and \
            super().position.y <= coords.y <= super().position.y + Dt.Utils.DEFAULT_TILE_DIMENSIONS

    def display(self, window) -> None :
        window.screen.blit(self.__bg_color, (super().position.x, super().position.y))
        if self.is_clicked :
            Pg.draw.rect(window.screen, Dt.Colors.RED, [super().position.x, super().position.y, \
                Dt.Utils.DEFAULT_TILE_DIMENSIONS, Dt.Utils.DEFAULT_TILE_DIMENSIONS], 2)
        elif self.is_visited :
            Pg.draw.rect(window.screen, Dt.Colors.GREEN, [super().position.x, super().position.y, \
                Dt.Utils.DEFAULT_TILE_DIMENSIONS, Dt.Utils.DEFAULT_TILE_DIMENSIONS], 1)
        if self.pieceDisplayer :
            self.pieceDisplayer.display(window)
        if self.is_choice : # the move possible for the selected pawn
            if self.pieceDisplayer is None : color : Pg.Color = Dt.Colors.YELLOW
            else : color : Pg.Color = Dt.Colors.PURPLE
            Pg.draw.circle(window.screen, color, (self.position.x, self.position.y), 10)


    def __str__(self) -> str :
        if self.__pieceDisplayer :
            return f"{self.chess_position} : {self.piece}"
        else :
            return f"{self.chess_position} : empty"
