import views.boardDisplayer as boardD
import views.menuDisplayer as menuD
import data as dt
import views.tile as tl
import models.game as gm
import views.popup as pup
import views.text as txt
import views.button as btn

class GameDisplayer :
    def __init__(self, font) -> None:
        self.__font = font
        self.__board_displayer : boardD.BoardDisplayer = None
        self.__menu_displayer = menuD.MenuDisplayer()
        self.__popup_game_has_ended: pup.Popup = pup.Popup((350, 350), position=(dt.Utils.DEFAULT_WINDOW_WIDTH - 405, dt.Utils.DEFAULT_WINDOW_HEIGHT - 500))
        self._init_game_has_ended_popup(font)
        self.__popup_pawn_promotion : pup.Popup = pup.Popup((300, 100))
        self._init_pawn_promotion_popup(font)
        self.__popup_game_has_ended_updated = False

    def _init_pawn_promotion_popup(self, font) -> None :
        self.pawn_promotion_popup.add_widget(txt.Text(
            (self.pawn_promotion_popup.x + 50, self.pawn_promotion_popup.y), 
            "Choisissez la promotion du pion", font))
        button_pos : tuple[int] = (self.pawn_promotion_popup.x + 20, self.pawn_promotion_popup.y + 50)
        text_pos : tuple[int] = (button_pos[0] + 20, button_pos[1] + 50)
        for name in ["knight", "bishop", "rook", "queen"] :
            text : txt.Text = txt.Text(text_pos, name, font, dt.Colors.BLACK)
            button : btn.Button = btn.Button(button_pos, (50, 40), text, dt.ButtonType.UP_ANIMATION)
            self.pawn_promotion_popup.add_widget(button)
            button_pos = (button_pos[0] + 70, button_pos[1])
            text_pos = (text_pos[0] + 70, text_pos[1])

    def _init_game_has_ended_popup(self, font) -> None:
        self.__popup_game_has_ended.reset_content()
        self.__popup_game_has_ended.add_widget(txt.Text((self.__popup_game_has_ended.x + 100, self.__popup_game_has_ended.y + 45), "La partie est terminée.", font))
        self.__popup_game_has_ended.add_widget(txt.Text((self.__popup_game_has_ended.x + 60, self.__popup_game_has_ended.y + 125), "Cliquez sur CLOSE pour fermer la jeu.", font))
        # Création du bouton CLOSE (ferme le programme)
        button_pos : tuple[int] = (self.__popup_game_has_ended.x + 140, self.__popup_game_has_ended.y + 190)
        button_text_pos : tuple[int] = (button_pos[0] + 20, button_pos[1] + 50)
        button_text : txt.Text = txt.Text(button_text_pos, "CLOSE", font, dt.Colors.BLACK)
        button = btn.Button(button_pos, (70, 55), button_text, dt.ButtonType.UP_ANIMATION)
        self.__popup_game_has_ended.add_widget(button)

    @property
    def board_displayer(self) -> boardD.BoardDisplayer : return self.__board_displayer

    @property
    def menu_displayer(self) -> menuD.MenuDisplayer : return self.__menu_displayer

    @property
    def pawn_promotion_popup(self) -> pup.Popup : return self.__popup_pawn_promotion

    @property
    def end_game_popup(self) -> pup.Popup : return self.__popup_game_has_ended

    def get_tile(self, position : tuple[int] | int) -> tl.Tile :
        if isinstance(position, int) :
            position = (8 - position // 8 - 1, position % 8)
        return self.board_displayer[position]

    def set_game(self, game : gm.Game) : self.__board_displayer = boardD.BoardDisplayer(game.board)

    def display(self, window) -> None : 
        if window.game_running:
            self.__board_displayer.display(window)
            self.__menu_displayer.display(window)
            if self.pawn_promotion_popup.is_active :
                self.pawn_promotion_popup.display(window)
        else:
            self.__board_displayer.display(window)
            self.__menu_displayer.display(window)
            if not self.__popup_game_has_ended_updated:
                self.__popup_game_has_ended.add_widget(txt.Text((self.__popup_game_has_ended.x + 87, self.__popup_game_has_ended.y + 85), f"Les gagnants sont les {window.winner}", self.__font, color=dt.Colors.BLACK if window.winner=="Blacks" else dt.Colors.BROWN))
                self.__popup_game_has_ended_updated = True
            self.__popup_game_has_ended.display(window)