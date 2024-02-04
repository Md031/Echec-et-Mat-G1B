import pygame as Pg
import Data as Dt
import views.Canvas as Cnvs
import views.GameDisplayer as Gd
import controllers.Controller as Ctrl
import controllers.GameController as GCtrl

class Window() :
    """
    Représente la fenêtre de l'application où seront affichées toutes les différentes vues

    Attributes 
    ----------
    screen : pygame.Surface
        surface sur laquelle on va afficher toutes les pages de l'application
    canvas : list[Canvas]  
        liste contenant toutes les pages de l'application
    controllers : list[Controller]  
        liste contenant toutes controlleurs de pages de l'application
    active_canvas : Canvas
        la page affichée sur la fenêtre
    active_controller : Controller
        le controller de la page active
    clock : Clock
        contrôle le framerate de la fenêtre
    """

    def __init__(self, size : tuple[int], game_type : bool) -> None :
        """
        Initialise une instance de Window

        Parameters
        ----------
        size : tuple[int]
            la taille de la fenêtre
        """
        self.__screen : Pg.Surface = Pg.display.set_mode(size)
        self.__screen.fill((60,25,60))
        self.__canvas : list[Cnvs.Canvas] = [None, Gd.GameDisplayer()]
        self.__controllers : list[Ctrl.Controller] = [None, GCtrl.GameController(self, game_type = game_type), game_type]
        self.__active_canvas : Cnvs.Canvas = self.canvas(Dt.CanvasType.GAME)
        self.__active_controller : Ctrl.Controller = self.controllers(Dt.CanvasType.GAME)
        self.__clock : Pg.time.Clock = Pg.time.Clock() 
        Pg.display.set_caption("FAILS")

    ###########
    # GETTERS #
    ###########
    @property
    def size(self) -> tuple[int] : 
        """Renvoie les dimensions de la fenêtre"""
        return self.screen.get_size()

    @property
    def screen(self) -> Pg.Surface :
        """Renvoie la surface"""
        return self.__screen

    def canvas(self, position : int | None = None) -> list[Cnvs.Canvas] | Cnvs.Canvas :
        """
        Renvoie une/plusieurs page(s) de l'application

        Parameters
        ----------
        position : int | None
            la numéro de la page à récupérer

        Returns
        -------
        list[Canvas] | Canvas 
            la page demandée si un nombre est passé en paramètre sinon toutes les pages de l'application
        """
        return self.__canvas[position] if position else self.__canvas

    @property
    def active_canvas(self) -> Cnvs.Canvas :
        """Renvoie la page affiche sur la fenêtre"""
        return self.__active_canvas

    @property
    def active_canvas_type(self) -> int :
        """Renvoie le type de la page active"""
        return self.__active_canvas.canvas_type

    def controllers(self, position : int | None = None) -> list[Ctrl.Controller] | Ctrl.Controller :
        """
        Renvoie une/plusieurs controlleur(s) de l'application

        Parameters
        ----------
        position : int | None
            la numéro du controlleur à récupérer

        Returns
        -------
        list[Controller] | Controller 
            le controlleur si un nombre est passé en paramètre sinon tout les controlleurs de l'application
        """
        return self.__controllers[position] if position else self.__controllers

    @property
    def active_controller(self) -> Ctrl.Controller :
        """Renvoie le controlleur de la page active"""
        return self.__active_controller

    def active_controller_type(self) -> int :
        """Renvoie le type du conttrolleur de la page active"""
        return self.__active_controller.type

    ###########
    # SETTERS #
    ###########
    def set_canvas(self, type : int) -> None :
        """
        Modifie la page à afficher sur la fenêtre
        
        Parameters
        ----------
        canvas_type : int
            le type de la page qu'il faut afficher
        """
        self.__active_canvas = self.canvas(type)
        self.__active_controller = self.controllers(type)

    ###################
    # OTHER FUNCTIONS #
    ###################
    def display(self) -> None :
        """Affiche la page sur la fenêtre"""
        self.__active_canvas.display(self)
        self.__clock.tick(60)

    def main_loop(self) -> None :
        """lance la fenêtre"""
        Pg.init()
        running = True
        while running :
            Pg.display.update()
            self.display()
            if self.active_controller.is_in_animation :
                print("in animation")
                self.active_controller.update()
            else :
                for event in Pg.event.get() :
                    if event.type == Pg.QUIT :
                        Pg.quit()
                        exit()
                    self.active_controller.handle(event)
