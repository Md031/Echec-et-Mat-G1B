import pygame as Pg
import Data as Dt
import views.GameDisplayer as GameD
import views.Tile as Tl
import models.Game as Gm
import controllers.Controller as Ctrl

class GameController(Ctrl.Controller) :
    def __init__(self, window, type: int = Dt.CanvasType.GAME) -> None:
        super().__init__(window, type)
        self.__game : Gm.Game = Gm.Game()
        self.__gamePage : GameD.GameDisplayer = window.canvas(Dt.CanvasType.GAME)
        self.__gamePage.set_game(self.__game)
        self.__selected_tiles : list[Tl.Tile] = [None, None]

    @property
    def game(self) -> Gm.Game : return self.__game

    @property
    def gamePage(self) -> GameD.GameDisplayer : return self.__gamePage

    @property
    def selected_tiles(self) -> list[Tl.Tile] : return self.__selected_tiles

    def handle_mouse_motion(self, event) -> None :
        mouse_pos : tuple[int] = event.pos
        for tile in self.gamePage.baordDisplayer :
                tile.set_visited(True) if mouse_pos in tile else tile.set_visited(False)

    def handle_mouse_click(self, event) -> None :
        mouse_pos : tuple[int] = event.pos
        for tile in self.gamePage.baordDisplayer :
            if mouse_pos in tile :
                if tile.piece :
                    if tile.piece.owner == self.game.active_player :
                        tile.set_clicked()
                    if tile.is_clicked :
                        self.selected_tiles[0] = tile
            else :
                tile.set_clicked(False) if tile.is_clicked else None

        return super().handle_mouse_click(event)

    def handle_key_pressed(self, event) -> None :
        return super().handle_key_pressed(event)

    def update(self) -> None:
        super().update()
        verif = 0
        for widget, dest, direction in self._to_animate :
            if widget.position == dest :
                verif += 1
        self._animate = verif != len(self._to_animate)
        if not self._animate :
            self.clear_animations()

