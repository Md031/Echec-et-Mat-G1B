import pygame as pg
import views.gameDisplayer as gd
import controllers.gameController as ctrl
import data as dt
import threading

class Window() :
    def __init__(self, size : tuple[int], playerWhite, playerBlack) -> None :
        self.__screen : pg.Surface = pg.display.set_mode(size)
        icon = pg.image.load('images/classic/WKnight.png') 
        pg.display.set_icon(icon)
        self.__font : pg.font.Font = pg.font.Font("font/sh-pinscher/SHPinscher-Regular.otf", 18)
        self.__screen.fill((dt.Colors.BG_COLOR))
        self.__game_dislayer : gd.GameDisplayer = gd.GameDisplayer(self.font)
        self.__game_controller : ctrl.GameController = ctrl.GameController(self, playerWhite, playerBlack)
        self.__clock : pg.time.Clock = pg.time.Clock()
        pg.display.set_caption("pyChess")
        self.__threads_ai = [None, None]
        self.__threads_ai[0] = threading.Thread(target=self.main_loop)
        self.__threads_ai[1] = threading.Thread(target=self.main_loop)
        self.__mutex_move = threading.Lock()

    ###########
    # GETTERS #
    ###########
    @property
    def size(self) -> tuple[int] : return self.screen.get_size()

    @property
    def screen(self) -> pg.Surface : return self.__screen

    @property
    def game_displayer(self) -> gd.GameDisplayer : return self.__game_dislayer

    @property
    def game_controller(self) -> ctrl.GameController : return self.__game_controller

    @property
    def font(self) -> pg.font.Font : return self.__font

    ###################
    # OTHER FUNCTIONS #
    ###################
    def display(self) -> None :
        self.game_displayer.display(self)
        self.__clock.tick(60)

    def handle_event(self) -> None :
        event = pg.event.get()
        self.game_controller.handle(event)
        if len(event) != 0:
            for e in event:
                if e.type == pg.QUIT:
                    pg.quit()
                    exit()

    def main_loop(self) -> None :
        running = True
        # self.__threads_ai[0] = threading.Thread(target=self.handle_move, args=(color, event))
        # self.__threads_ai[1] = threading.Thread(target=self.handle_move, args=(color, event))
        while running :
            self.__mutex_move.acquire()
            try:  # to synchronise the threads
                pg.display.update()
                self.display()
                self.handle_event()
            finally:
                self.__mutex_move.release()

                
            # pg.display.update()
            # self.display()
            # # if self.game_controller.is_in_animation :
            # #     self.game_controller.update()
            # # else :
            # self.handle_event()

