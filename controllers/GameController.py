import pygame as Pg
import Data as Dt
import views.GameDisplayer as GameD
import views.Tile as Tl
import models.Game as Gm
import controllers.Controller as Ctrl
import models.Move as Mv
import views.PieceDisplayer as PieceD
import models.Pieces as Pcs
from models.Ia import Ia

class GameController(Ctrl.Controller) :
    """
    Classe qui va gérer les intéractions entre le joueur et le jeu
    """

    def __init__(self, window, ctrl_type: int = Dt.CanvasType.GAME, game_type: bool = False) -> None :
        """
        Initialise une instance de GameController
        (voir contstructeur de la classe "Controller")
        """
        super().__init__(window, ctrl_type, game_type)
        self.__game_type : bool = game_type
        self.__game : Gm.Game = Gm.Game()
        self.__gamePage : GameD.GameDisplayer = window.canvas(Dt.CanvasType.GAME)
        self.__gamePage.set_game(self.__game)
        self.__selected_tiles : list[Tl.Tile] = [None, None]
        self.__ia : Ia = Ia(self.__game, self)

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
                                print(self.game.active_player_actions)
                                if self.selected_tiles[0] is not None :
                                    self._update_choice_tiles(self.selected_tiles[0].piece, False)
                                self.selected_tiles[0] = tile
                                self._update_choice_tiles(tile.piece, True)
                        else :
                            self._update_choice_tiles(self.selected_tiles[0].piece, False)
                    elif self.selected_tiles[0] is not None :
                        if tile.is_choice : # if it's not an illegal move
                            self._update_choice_tiles(self.selected_tiles[0].piece, False)
                            self.selected_tiles[1] = tile
                            move : Mv.Move = Mv.Move(self.selected_tiles[0].grid_position, \
                                self.selected_tiles[1].grid_position, self.game.board)
                            self.game._set_move_type(move)
                            self._play_move(move)
                        else: # to remove the circle showing the possible move of a pawn
                            self._update_choice_tiles(self.selected_tiles[0].piece, False)
                        self.__selected_tiles = [None, None]
                else :
                    tile.set_clicked(False) if tile.is_clicked else None

    def _get_castling_rook(self, move : Mv.Move) -> None :
        king_side : bool = move.dest_pos - move.start_pos == (0, 2) 
        rook_pos : str = ""
        if king_side : rook_pos += "h"
        else : rook_pos += "a"
        if self.game.active_player == 0 : rook_pos += "1"
        else : rook_pos += "8"
        move.set_castling_rook(self.game.board[rook_pos])
        self.game.set_casling_rights(None)

    def _handle_pawn_promotion(self, event) -> None :
        pawn_promotion_popup = self.gamePage.pawn_promotion_popup
        match event.type :
            case Pg.MOUSEMOTION :
                mouse_pos : tuple[int] = event.pos
                for widget in pawn_promotion_popup.content :
                    if widget.name != "text" :
                        if mouse_pos in widget : 
                            widget.set_visited(True)
                        else : 
                            widget.set_visited(False)
            case Pg.MOUSEBUTTONDOWN :
                mouse_pos : tuple[int] = event.pos
                for widget in pawn_promotion_popup.content :
                    if widget.name != "text" :
                        if mouse_pos in widget : 
                            widget.set_clicked(not widget.is_clicked)
                            if widget.is_clicked :
                                self._promote_pawn(self.game.moves[-1], widget.content.text)
                                pawn_promotion_popup.set_active(False)

    def _promote_pawn(self, move : Mv.Move, promotion_piece_name : str) -> None :
        piece : Pcs.Piece = move.piece_moved
        promotion_piece : Pcs.Piece = None
        match promotion_piece_name :
            case "knight" :
                promotion_piece = Pcs.Knight(piece.position, piece.owner)
            case "bishop" :
                promotion_piece = Pcs.Bishop(piece.position, piece.owner)
            case "rook" :
                promotion_piece = Pcs.Rook(piece.position, piece.owner)
            case "queen" :
                promotion_piece = Pcs.Queen(piece.position, piece.owner)
        self.game.board[piece.position] = promotion_piece
        self._update_board_display(promotion_piece)
        move.set_type(Dt.MoveType.PROMOTION)
        move.set_promotion(promotion_piece.name)

    def _play_move(self, move : Mv.Move) -> None :
        self.game.push_move(move)
        start_tile : Tl.Tile = self.gamePage.baordDisplayer[move.start_pos]
        dest_tile : Tl.Tile = self.gamePage.baordDisplayer[move.dest_pos]
        dest_tile.set_piece(start_tile.pieceDisplayer)
        start_tile.set_piece(None)
        if move.move_type == Dt.MoveType.CASTLING :
            self._play_castling(move)
        elif move.move_type == Dt.MoveType.EN_PASSANT :
            ...
        elif move.move_type == Dt.MoveType.PROMOTION :
            self.gamePage.pawn_promotion_popup.set_active(True)
        self.game.update_state()

    def _play_castling(self, move : Mv.Move) -> None :
        king_side : bool = move.dest_pos - move.start_pos == (0, 2) 
        rook_pos : str = ""
        if king_side : rook_pos += "h"
        else : rook_pos += "a"
        if move.piece_moved.owner == 0 : rook_pos += "1"
        else : rook_pos += "8"
        start_tile : Tl.Tile = self.gamePage.baordDisplayer[Dt.convert_coordinates(rook_pos)]
        dest_tile : Tl.Tile = self.gamePage.baordDisplayer[move.castling_rook.position]
        dest_tile.set_piece(start_tile.pieceDisplayer)
        start_tile.set_piece(None)

    def _revert_move(self) -> None :
        move : Mv.Move = self.game.pop_move()
        start_tile : Tl.Tile = self.gamePage.baordDisplayer[move.start_pos]
        dest_tile : Tl.Tile = self.gamePage.baordDisplayer[move.dest_pos]
        start_tile.set_piece(dest_tile.pieceDisplayer)
        dest_tile.set_piece(
            PieceD.PieceDisplayer(dest_tile.position, move.piece_captured) 
            if move.piece_captured else None)
        if move.move_type == Dt.MoveType.PROMOTION :
            self._revert_promotion(move)
        elif move.move_type == Dt.MoveType.CASTLING :
            self._revert_castling(move)
        elif move.move_type == Dt.MoveType.EN_PASSANT :
            ...
        if self.game.board[move.start_pos] == "pawn" :
            self.check_pawn_promotion(move.piece_moved)
        self.game.update_state()

    def _revert_promotion(self, move : Mv.Move) -> None :
        pawn_screen_pos : Dt.Point = self.gamePage.baordDisplayer[move.start_pos].position
        pawn_displayer : PieceD.PieceDisplayer = PieceD.PieceDisplayer(pawn_screen_pos, 
            self.game.board[move.start_pos])
        self.gamePage.baordDisplayer[move.start_pos].set_piece(pawn_displayer)

    def _revert_castling(self, move : Mv.Move) -> None :
        if move.castling_rook.position.y == 0 :
            rook_dest_pos : Dt.Point = move.castling_rook.position + (0, 3)
        else :
            rook_dest_pos : Dt.Point = move.castling_rook.position + (0, -2)
        start_tile : Tl.Tile = self.gamePage.baordDisplayer[move.castling_rook.position]
        dest_tile : Tl.Tile = self.gamePage.baordDisplayer[rook_dest_pos]
        start_tile.set_piece(dest_tile.pieceDisplayer)
        dest_tile.set_piece(None)

    def _update_choice_tiles(self, piece, is_choice : bool) -> None :
        """
        Met à jour l'affichage des positions possible pour une pièce
        quand un joueur clique sur le plateau de jeu
        """
        for move in self.game.active_player_actions :
            if move[:2] == piece.chess_positon :
                tile : Tl.Tile = self.gamePage.baordDisplayer[Dt.convert_coordinates(move[2:])]
                tile.set_choice(False) if not is_choice else tile.set_choice(True)
                # print(move)

    def _update_board_display(self, piece : Pcs.Piece) -> None :
        position : Dt.Point = self.gamePage.baordDisplayer[piece.position].position
        piece_displayer : PieceD.PieceDisplayer = PieceD.PieceDisplayer(position, piece)
        self.gamePage.baordDisplayer[piece.position].set_piece(piece_displayer)

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
            self.game.reset()
            self.gamePage.set_game(self.game)
            self.gamePage.pawn_promotion_popup.set_active(False)

    def handle(self, event) -> None :
        """Gère les événements qui ont lieu dans la fenêtre de l'application"""
        if self.game.active_player == 0 or not self.__game_type :
            if not self.gamePage.pawn_promotion_popup.is_active :
                super().handle(event)
            else : 
                self._handle_pawn_promotion(event)
        else:
            action = self.__ia.minimax(3)
            self._play_move(action)            
            # begin, ending = self.__ia.random_ia()
            # choice = Mv.Move(begin, ending, self.game.board)
            # self._play_move(choice)
            # self.__ia.evaluation(self.game)

    def action_conversion(self, action: str) -> Mv.Move :
        begin_action = Dt.convert_coordinates(action[0:2])
        end_action = Dt.convert_coordinates(action[2:])
        return Mv.Move(begin_action, end_action, self.game.board)