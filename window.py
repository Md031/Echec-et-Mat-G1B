import pygame as pg
import views.gameDisplayer as gd
import controllers.gameController as ctrl
import data as dt
import threading

class Window():
    def __init__(self, size: tuple[int], playerWhite, playerBlack) -> None:
        self.__screen: pg.Surface = pg.display.set_mode(size)
        icon = pg.image.load('images/classic/WKnight.png') 
        pg.display.set_icon(icon)
        self.__font: pg.font.Font = pg.font.Font("font/sh-pinscher/SHPinscher-Regular.otf", 18)
        self.__screen.fill((dt.Colors.BG_COLOR))
        self.__game_displayer: gd.GameDisplayer = gd.GameDisplayer(self.font)
        self.__game_controller: ctrl.GameController = ctrl.GameController(self, playerWhite, playerBlack)
        self.__clock: pg.time.Clock = pg.time.Clock()
        pg.display.set_caption("pyChess")
        self.__thread_run = True
        self.__cmpt = 0
        self.__game_running = True
        self.__threads_ai = [threading.Thread(target=self.handle_event_thread, args=[0]), threading.Thread(target=self.handle_event_thread, args=[1])]
        self.__mutex_move = threading.Lock()
        self.__mutex_event = threading.Lock()
        self.__mutex_quit = threading.Lock()
        self.__threads_ai[0].start()
        self.__threads_ai[1].start()
        self.__winner = None

    ###########
    # GETTERS #
    ###########
    @property
    def size(self) -> tuple[int]:
        return self.screen.get_size()

    @property
    def screen(self) -> pg.Surface:
        return self.__screen

    @property
    def game_displayer(self) -> gd.GameDisplayer:
        return self.__game_displayer

    @property
    def game_controller(self) -> ctrl.GameController:
        return self.__game_controller

    @property
    def font(self) -> pg.font.Font:
        return self.__font
    
    @property 
    def game_running(self) -> bool:
        return self.__game_running
    
    @property
    def winner(self) -> str:
        return self.__winner
    
    ###################
    # OTHER FUNCTIONS #
    ###################

    def check_quit(self, event) -> None:
        if len(event) != 0:
            for e in event:
                if e.type == pg.QUIT:
                    self.__game_controller.set_exited_progam()
                    pg.quit()
                    exit()

    def display(self) -> None:
        self.game_displayer.display(self)
        self.__clock.tick(60)

    def handle_event(self) -> None:
        event = pg.event.get()
        self.__mutex_quit.acquire()
        try:
            self.check_quit(event)
        finally:
            self.__mutex_quit.release()
        res = 0
        self.__mutex_event.acquire()
        try:
            res = self.game_controller.handle(event)
        finally:
            self.__mutex_event.release()
        if res == 0 or res == 1:
            self.__thread_run = False

    def handle_event_thread(self, thread_index: int) -> None:
        while not self.__game_controller.player_exited_program:
            self.__mutex_move.acquire()
            try:
                self.handle_event()
            finally:
                self.__mutex_move.release()
        self.__mutex_move.acquire()
        try:
            self.__cmpt += 1
        finally:
            self.__mutex_move.release()
        if self.__cmpt == 1:  # to only show the message once
            self.game_displayer.menu_displayer.moves_displayer.add_text(f'The {self.__winner} won the game.', dt.Colors.RED)

    def main_loop(self) -> None:
        while self.__game_running or not self.__game_controller.player_exited_program:
            pg.display.update()
            self.display()
            pg.event.pump()
            if self.game_controller.game.is_over:
                self.__game_running = False