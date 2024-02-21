import views.boardDisplayer as boardD
import views.menuDisplayer as menuD

import data as dt
import views.tile as tl
import models.game as gm
import views.popup as pup
import views.text as txt
import views.button as btn
import pygame as pg

class GameDisplayer :
    def __init__(self, font) -> None:
        self.__board_displayer : boardD.BoardDisplayer = None
        self.__menu_displayer = menuD.MenuDisplayer()
        self.__popup_pawn_promotion : pup.Popup = pup.Popup((300, 100))
        self._init_pawn_promotion_popup(font)
        # self.ai_move_timer = txt.Text((660, 20), "Minimax played move in 2.00ms" , pg.font.Font("font/sh-pinscher/SHPinscher-Regular.otf", 18))


    def _init_pawn_promotion_popup(self, font) -> None :
        self.pawn_promotion_popup.add_widget(txt.Text(
            (self.pawn_promotion_popup.x + 50, self.pawn_promotion_popup.y), 
            "Choisissez la promotion du pion", font))
        button_pos : tuple[int] = (self.pawn_promotion_popup.x + 20, self.pawn_promotion_popup.y + 50)
        text_pos : tuple[int] = (button_pos[0] + 20, button_pos[1] + 50)

        for name in ["knight", "bishop", "rook", "queen"] :
            text : txt.Text = txt.Text(text_pos, name, font, dt.Colors.GREEN)
            button : btn.Button = btn.Button(button_pos, (50, 40), text, dt.ButtonType.UP_ANIMATION)
            self.pawn_promotion_popup.add_widget(button)
            button_pos = (button_pos[0] + 70, button_pos[1])
            text_pos = (text_pos[0] + 70, text_pos[1])

    @property
    def board_displayer(self) -> boardD.BoardDisplayer : return self.__board_displayer

    @property
    def menu_displayer(self) -> menuD.MenuDisplayer : return self.__menu_displayer

    @property
    def pawn_promotion_popup(self) -> pup.Popup : return self.__popup_pawn_promotion

    def get_tile(self, position : tuple[int] | int) -> tl.Tile :
        if isinstance(position, int) :
            position = (8 - position // 8 - 1, position % 8)
        return self.board_displayer[position]

    def set_game(self, game : gm.Game) : self.__board_displayer = boardD.BoardDisplayer(game.board)

    def display(self, window) -> None : 
        self.__board_displayer.display(window)
        self.__menu_displayer.display(window)
        if self.pawn_promotion_popup.is_active :
            self.pawn_promotion_popup.display(window)