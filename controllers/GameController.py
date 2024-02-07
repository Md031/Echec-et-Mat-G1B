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
                                # print(tile.piece)
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
                            self._set_move_type(move.piece_moved)
                            # print(self.game.state)
                        else: # to remove the circle showing the possible move of a pawn
                            self._update_choice_tiles(self.selected_tiles[0].piece, False)
                        self.__selected_tiles = [None, None]
                else :
                    tile.set_clicked(False) if tile.is_clicked else None

    def _set_move_type(self, move : Mv.Move) -> None :
        if self.game.is_promotion(move) :
            self.gamePage.pawn_promotion_popup.set_active(True)
            move.set_type(Dt.MoveType.PROMOTION)
        elif self.game.is_castling(move) :
            ...
        elif self.game.is_en_passant(move) :
            ...

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
            self.game.board.get_player_pieces(piece.owner).remove(piece)
            self.game.board.add_piece(promotion_piece, piece.owner)
            self._update_board_display(promotion_piece)
            move.set_type(Dt.MoveType.PROMOTION)
            move.set_promotion(promotion_piece.name)


    def _play_move(self, move : Mv.Move) -> None :
        # print(move.uci)
        self.game.push_move(move)
        # print(len(self.game.board.get_player_pieces(0)))
        # print(len(self.game.board.get_player_pieces(1)))
        start_tile : Tl.Tile = self.gamePage.baordDisplayer[move.start_pos]
        dest_tile : Tl.Tile = self.gamePage.baordDisplayer[move.dest_pos]
        dest_tile.set_piece(start_tile.pieceDisplayer)
        start_tile.set_piece(None)
        self.game.update_state()

    def _revert_move(self) -> None :
        if self.game.moves[-1].move_type == Dt.MoveType.PROMOTION :
            promotion_piece : Pcs.Piece = self.game.board[self.game.moves[-1].dest_pos]
        move : Mv.Move = self.game.pop_move()
        start_tile : Tl.Tile = self.gamePage.baordDisplayer[move.start_pos]
        dest_tile : Tl.Tile = self.gamePage.baordDisplayer[move.dest_pos]
        start_tile.set_piece(dest_tile.pieceDisplayer)
        dest_tile.set_piece(
            PieceD.PieceDisplayer(Dt.Point(0, 0), move.piece_captured) 
            if move.piece_captured else None)
        if move.move_type == Dt.MoveType.PROMOTION :
            self._revert_promotion(move, promotion_piece)
        self.check_pawn_promotion(move.piece_moved)
        self.game.update_state()

    def _revert_promotion(self, move : Mv.Move, promotion_piece : Pcs.Piece) -> None :
        pawn : Pcs.Pawn = move.piece_moved
        self.game.board.get_player_pieces(pawn.owner).remove(promotion_piece)
        self.game.board[move.start_pos] = pawn
        self.game.board.add_piece(pawn, pawn.owner)
        self._update_board_display(pawn)

    def is_promotion(self, move : Mv.Move) -> None :
        if move.piece_moved.name == "pawn" :
            if ((move.piece_moved.owner == 0 and move.piece_moved.position.x == 0) or 
            (move.piece_moved.owner == 1 and move.piece_moved.position.x == self.game.board.size[0] - 1)) :
                return True
            else : self.gamePage.pawn_promotion_popup.set_active(False)

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
            # print(self.game)
            self.game.reset()
            # print(self.game)
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
        