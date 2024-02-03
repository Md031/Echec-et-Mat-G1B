import pygame as Pg
import Data as Dt
import views.GameDisplayer as GameD
import views.Tile as Tl
import models.Game as Gm
import controllers.Controller as Ctrl
import models.Move as Mv
import views.PieceDisplayer as PieceD
import random as rd

class GameController(Ctrl.Controller) :
    """
    Classe qui va gérer les intéractions entre le joueur et le jeu
    """

    def __init__(self, window, type: int = Dt.CanvasType.GAME) -> None :
        """
        Initialise une instance de GameController
        (voir contstructeur de la classe "Controller")
        """
        super().__init__(window, type)
        self.__game : Gm.Game = Gm.Game()
        self.__gamePage : GameD.GameDisplayer = window.canvas(Dt.CanvasType.GAME)
        self.__gamePage.set_game(self.__game)
        self.__selected_tiles : list[Tl.Tile] = [None, None]

    @property
    def game(self) -> Gm.Game :
        """Renvoie la partie en cours"""
        return self.__game

    @property
    def gamePage(self) -> GameD.GameDisplayer :
        """Renvoie la page controllé"""
        return self.__gamePage

    @property
    def selected_tiles(self) -> list[Tl.Tile] :
        """Renvoie la case sélectionnée par le joueur actif"""
        return self.__selected_tiles

    def handle_mouse_motion(self, event) -> None :
        mouse_pos : tuple[int] = event.pos
        for tile in self.gamePage.baordDisplayer :
                tile.set_visited(True) if mouse_pos in tile else tile.set_visited(False)

    def handle_mouse_click(self, event) -> None :
        mouse_pos : tuple[int] = event.pos
        for tile in self.gamePage.baordDisplayer :
            if mouse_pos in tile :
                if tile.piece and (tile.piece.owner == self.game.active_player) : # when the active_player click on one of his pawn
                    tile.set_clicked()
                    if tile.is_clicked : 
                        if self.selected_tiles[0] is None or \
                        tile.grid_position != self.selected_tiles[0].grid_position :
                            print(tile.piece)
                            if self.selected_tiles[0] is not None :
                                self._update_choice_tiles(self.selected_tiles[0].piece, False)
                            self.selected_tiles[0] = tile
                            self._update_choice_tiles(tile.piece, True)
                elif self.selected_tiles[0] is not None :
                    if tile.is_choice : # if it's not an illegal move
                        self._update_choice_tiles(self.selected_tiles[0].piece, False)
                        self.selected_tiles[1] = tile
                        move : Mv.Move = Mv.Move(self.selected_tiles[0].grid_position, \
                            self.selected_tiles[1].grid_position, self.game.board)
                        self._play_move(move)
                        print(self.game.state)
                    else: # to remove the circle showing the possible move of a pawn
                        self._update_choice_tiles(self.selected_tiles[0].piece, False)
                    self.__selected_tiles = [None, None]
            else :
                tile.set_clicked(False) if tile.is_clicked else None

    def _play_move(self, move : Mv.Move) -> None :
        print(move.uci)
        self.game.push_move(move)
        print(len(self.game.board.get_player_pieces(0)))
        print(len(self.game.board.get_player_pieces(1)))
        start_tile : Tl.Tile = self.gamePage.baordDisplayer[move.start_pos]
        dest_tile : Tl.Tile = self.gamePage.baordDisplayer[move.dest_pos]
        dest_tile.set_piece(start_tile.pieceDisplayer)
        start_tile.set_piece(None)
        self.game.update_state()

    def _revert_move(self) -> None :
        move : Mv.Move = self.game.pop_move()
        start_tile : Tl.Tile = self.gamePage.baordDisplayer[move.start_pos]
        dest_tile : Tl.Tile = self.gamePage.baordDisplayer[move.dest_pos]
        start_tile.set_piece(dest_tile.pieceDisplayer)
        dest_tile.set_piece(
            PieceD.PieceDisplayer(Dt.Point(0, 0), move.piece_captured) 
            if move.piece_captured else None)
        self.game.update_state()

    def _update_choice_tiles(self, piece, is_choice : bool) -> None :
        """
        Met à jour l'affichage des positions possible pour une pièce
        quand un joueur clique sur le plateau de jeu
        """
        for move in self.game.active_player_actions :
            if move[:2] == piece.chess_positon :
                tile : Tl.Tile = self.gamePage.baordDisplayer[Dt.convert_coordinates(move[2:])]
                tile.set_choice(False) if not is_choice else tile.set_choice(True)
                print(move)

    def handle_key_pressed(self, event) -> None :
        key = event.key
        if key == Pg.K_b or key == Pg.K_r :
            if self.__selected_tiles[0] :
                self.__selected_tiles[0].set_clicked(False)
                if self.__selected_tiles[0].piece :
                    self._update_choice_tiles(self.__selected_tiles[0].piece, False)

        if key == Pg.K_b :
            if len(self.game.moves) > 0 :
                self._revert_move()
        if key == Pg.K_r :
            # print(self.game)
            self.game.reset()
            # print(self.game)
            self.gamePage.set_game(self.game)

    def random_ia(self):
        choice_move = rd.choice(self.game._valid_actions())
        begin = Dt.convert_coordinates(choice_move[0:2])
        ending = Dt.convert_coordinates(choice_move[2:])
        return begin, ending

    def handle(self, event) -> None :
        """Gère les événements qui ont lieu dans la fenêtre de l'application"""
        if self.game.active_player == 0:
            super().handle(event)
        else:
            begin, ending = self.random_ia()
            choice = Mv.Move(begin, ending, self.game.board)
            self._play_move(choice)