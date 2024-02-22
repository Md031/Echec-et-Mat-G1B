import views.resetButtonDisplayer as resetBD
import views.takeBackMove as tkb
import data as dt
import views.text as txt
import pygame as pg

class MenuDisplayer :
    def __init__(self, text=None, position=(660, 20)) -> None:
        self.text = text
        self.position = position
        self.texts = [txt.Text(position, text , pg.font.Font("font/sh-pinscher/SHPinscher-Regular.otf", 18))]

    def change_text(self, text) -> None :
        # supprimer l'ancien texte
        self.texts[0].set_color(pg.Color(245, 245, 220)) # rendre le texte transparent (couleur de la fenêtre)
        self.texts[0].set_txt(text)
        self.texts[0].set_color(dt.Colors.BLACK)
    
    def add_text(self, text) -> None :
        self.set_position((self.position[0], self.position[1] + 20))
        new_text = txt.Text(self.position, text, pg.font.Font("font/sh-pinscher/SHPinscher-Regular.otf", 18))
        self.texts.append(new_text)
    
    def set_position(self, position) -> None :
        self.position = position

    def get_position(self) -> tuple[int] :
        return self.position

    def display(self, window) -> None :
        for text in self.texts :
            text.display(window)
