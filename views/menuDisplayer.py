import views.resetButtonDisplayer as resetBD
import views.takeBackMove as tkb
import data as dt
import views.text as txt
import pygame as pg

class MenuDisplayer :
    def __init__(self) -> None:
        self.reset_button_displayer = resetBD.ResetButtonDisplayer((810, 560), "REPLAY" , pg.font.Font("font/sh-pinscher/SHPinscher-Regular.otf", 50), dt.Colors.WHITE, dt.Colors.BROWN)
        self.take_back_move = tkb.TakeBackMove((660, 20))
        self.moves_displayer = TextDisplayer("Moves played : ", (660, 50))
        self.background_rect = pg.Rect(660, 60, 430, 500)

    def draw_background(self, screen) -> None:
        pg.draw.rect(screen, dt.Colors.BG_COLOR, self.background_rect)

    def display(self, window) -> None : 
        self.reset_button_displayer.display(window)
        self.take_back_move.display(window)
        self.draw_background(window.screen)
        self.moves_displayer.display(window)


    
class TextDisplayer(MenuDisplayer):
    def __init__(self, text=None, position=(660, 20)) -> None:
        self.position = position
        self.l_texts = [txt.Text(position, text , pg.font.Font("font/sh-pinscher/SHPinscher-Regular.otf", 18), dt.Colors.BLACK, dt.Colors.BG_COLOR)]

    def change_text(self, new_text : str) -> None :
        self.l_texts[0].set_txt(new_text)

    def resize(self) -> None :
        for i in range(1,len(self.l_texts)) :
            self.l_texts[i].set_position((660, 50 + 20 * i))
            self.l_texts[i].reset()
    
    def add_text(self, text) -> None :
        pos = self.get_position()
        new_text = txt.Text((pos[0], pos[1] + 20), text, pg.font.Font("font/sh-pinscher/SHPinscher-Regular.otf", 18), dt.Colors.BLACK, dt.Colors.BG_COLOR, True)
        self.l_texts.append(new_text)
        if (self.get_position()[1] > 500):  # si on dépasse pas la zone propre à l'historique de move
            self.l_texts.pop(1)
            self.resize()

    def reset_state(self) -> None :
        self.l_texts = [self.l_texts[0]]
        self.resize()

    def get_position(self) -> tuple[int] :
        return self.l_texts[-1].position

    def display(self, window) -> None :
        for text in self.l_texts :
            text.display(window)
