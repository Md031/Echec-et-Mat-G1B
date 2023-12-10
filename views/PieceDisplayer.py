import pygame as Pg
import models.Pieces as Pcs
import Data as Dt

class PieceDisplayer(Pg.sprite.Sprite) :
    """
    Représente l'affichage d'une pièce du jeu d'échecs sur la fenêtre de l'application

    Attributes
    ----------
    position : Dt.Point
        la position de la pièce sur la fenêtre
    piece : Pcs.Piece
        la pièce à afficher
    """

    def __init__(self, position : Dt.Point, piece : Pcs.Piece) -> None :
        """
        Initialise une instance de PieceDisplayer

        Parameters
        ----------
        position : Dt.Point
        la position de la pièce sur la fenêtre
        piece : Pcs.Piece
            la pièce à afficher
        """
        Pg.sprite.Sprite.__init__(self)
        self.__piece : Pcs.Piece = piece
        self.__image : Pg.Surface = Pg.image.load(self.__piece.image_filename).convert_alpha()
        self.__rect : Pg.Rect = Pg.rect.Rect(position.x, position.y, \
            self.__image.get_size()[0], self.__image.get_size()[1])
        self.__rect.topleft = position.x, position.y

    @property
    def position(self) -> Dt.Point :
        """Renvoie la position (coin suprérieur gauche) de la pièce sur la fenêtre"""
        return Dt.Point(self.__rect.topleft[0], self.__rect.topleft[1])

    @property
    def center(self) -> Dt.Point :
        """Renvoie la position (centre) de la pièce sur la fenêtre"""
        return Dt.Point(self.__rect.center[0], self.__rect.center[1])

    @property
    def grid_position(self) -> Dt.Point : 
        """Renvoie la position de la pièce sur le plateau de jeu"""
        return self.__piece.position

    @property
    def image_filename(self) -> str :
        """Renvoie le chemin vers le fichier .png qui représente la pièce""" 
        return self.__piece.image_filename

    @property
    def piece(self) -> Pcs.Piece :
        """Renvoie la pièce à afficher"""
        return self.__piece

    def set_position(self, position : Dt.Point) -> None :
        """Change la position de la pièce sur la fenêtre"""
        self.__rect.center = position.x, position.y 

    def display(self, window) -> None :
        """
        Affiche la pièce sur la fenêtre

        Parameters
        ----------
        window : Window
            la fenêtre sur laquelle la pièce va être affichées
        """
        window.screen.blit(self.__image, (self.position.x, self.position.y))
