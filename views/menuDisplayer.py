import views.resetButtonDisplayer as resetBD
import views.takeBackMove as tkb
import data as dt
import views.text as txt
import pygame as pg

class MenuDisplayer :
    def __init__(self) -> None:
        self.ai_move_timer = txt.Text((660, 20), "" , pg.font.Font("font/sh-pinscher/SHPinscher-Regular.otf", 18))
        self.reset_button_displayer = resetBD.ResetButtonDisplayer((660, 600), "RESET" , pg.font.Font("font/sh-pinscher/SHPinscher-Regular.otf", 30), dt.Colors.WHITE, dt.Colors.BROWN)
        self.take_back_move = tkb.TakeBackMove((660, 80))
        self.move_history = txt.Text((660, 100), "a" , pg.font.Font("font/sh-pinscher/SHPinscher-Regular.otf", 18))

    def display(self, window) -> None : 
        self.ai_move_timer.display(window)
        self.reset_button_displayer.display(window)
        self.take_back_move.display(window)
        self.move_history = txt.Text((660, 100), "a" , pg.font.Font("font/sh-pinscher/SHPinscher-Regular.otf", 18))
        