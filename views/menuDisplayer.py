import views.boardDisplayer as boardD
import data as dt
import views.tile as tl
import models.game as gm
import views.popup as pup
import views.text as txt
import views.button as btn
import pygame as pg

class MenuDisplayer :
    def __init__(self) -> None:
        self.ai_move_timer = txt.Text((660, 20), "Minimax played move in 2.00ms" , pg.font.Font("font/sh-pinscher/SHPinscher-Regular.otf", 18))

    def display(self, window) -> None : 
        self.ai_move_timer.display(window)