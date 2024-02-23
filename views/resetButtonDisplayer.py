import data as dt
import views.text as txt
import pygame as pg

class ResetButtonDisplayer(txt.Text) :

    def __init__(self, position : tuple[int], text : str, font : pg.font.Font, 
    color : pg.Color = dt.Colors.BLACK, bg_color : pg.Color = None) :
        super().__init__(position, text, font, color, bg_color)
    
    def __contains__(self, coords: tuple[int]) -> bool:
        x, y = coords
        return (800 < x < 920 and 540 < y < 630)