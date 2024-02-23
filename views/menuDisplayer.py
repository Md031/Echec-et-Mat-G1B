import views.resetButtonDisplayer as resetBD
import views.takeBackMove as tkb
import data as dt
import views.text as txt
import pygame as pg

class MenuDisplayer :
    def __init__(self) -> None:
        self.reset_button_displayer = resetBD.ResetButtonDisplayer((810, 560), "REPLAY" , pg.font.Font("font/sh-pinscher/SHPinscher-Regular.otf", 50), dt.Colors.WHITE, dt.Colors.BROWN)
        self.take_back_move = tkb.TakeBackMove((660, 20))
        self.move_history = txt.Text((660, 100), "a" , pg.font.Font("font/sh-pinscher/SHPinscher-Regular.otf", 18))
        self.timer_displayer = TextDisplayer("")
        self.moves_displayer = TextDisplayer("Moves played : ", (660, 50))

    def display(self, window) -> None : 
        self.reset_button_displayer.display(window)
        self.take_back_move.display(window)
        self.move_history = txt.Text((660, 100), "a" , pg.font.Font("font/sh-pinscher/SHPinscher-Regular.otf", 18))
        self.timer_displayer.display(window)
        self.moves_displayer.display(window)
        
    
class TextDisplayer(MenuDisplayer):
    def __init__(self, text=None, position=(660, 20)) -> None:
        self.position = position
        self.l_texts = [txt.Text(position, text , pg.font.Font("font/sh-pinscher/SHPinscher-Regular.otf", 18), dt.Colors.BLACK, dt.Colors.BG_COLOR)]

    def change_text(self, new_text : str) -> None :
        self.l_texts[0].set_txt(new_text)
    
    def add_text(self, text) -> None :
        self.set_position((self.position[0], self.position[1] + 20))  # add txt beneath the previous one
        new_text = txt.Text(self.position, text, pg.font.Font("font/sh-pinscher/SHPinscher-Regular.otf", 18), dt.Colors.BLACK, dt.Colors.BG_COLOR)
        self.l_texts.append(new_text)
    
    def set_position(self, position) -> None :
        self.position = position

    def get_position(self) -> tuple[int] :
        return self.position

    def display(self, window) -> None :
        for text in self.l_texts :
            text.display(window)
