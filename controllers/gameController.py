import chess as ch
import pygame as pg
import data as dt
import views.pieceDisplayer as pieceD
import views.gameDisplayer as gameD
import views.tile as tl
import models.game as gm
import models.Ia as ia
import views.text as txt
import threading
import time

class GameController :
    def __init__(self, window, playerWhite, playerBlack) -> None:
        self.playerWhite = playerWhite
        self.playerBlack = playerBlack
        self.__game : gm.Game = gm.Game()
        if playerWhite != None:
            playerWhite.set_game(self.__game)
        if playerBlack != None:
            playerBlack.set_game(self.__game)
        self.__game_displayer : gameD.GameDisplayer = window.game_displayer
        self.__game_displayer.set_game(self.__game)
        self.__start_tile : tl.Tile = None
        self.__dest_tile : tl.Tile = None
        self.__move : dt.Move = dt.Move()
        # self.__ia : ia.Ai = ia.Ai(self.__game)
        self.__animate : bool = False
        self.__to_animate : list[tuple[any, tuple[int], tuple[int]]] = []
        self.__last_two_moves = [None, None]
        self.__iaType = ["Minimax", "Random", "Neural Network"]
        self.__thread = None
        self.__mutex_move = threading.Lock()
        self.__mutex_display = threading.Lock()

    @property
    def game(self) -> gm.Game : return self.__game

    @property
    def game_displayer(self) -> gameD.GameDisplayer : return self.__game_displayer

    @property
    def start_tile(self) -> tl.Tile : return self.__start_tile

    @property
    def dest_tile(self) -> tl.Tile : return self.__dest_tile

    @property
    def move(self) -> dt.Move : return self.__move

    def get_casling_rook_pos(self) -> tuple[int] :
        king_side : bool = self.move.direction == (0, 2) 
        rook_pos : str = ''
        piece_color : bool = self.dest_tile.piece.color \
            if self.dest_tile.piece_displayer else self.game.board.piece_at(self.move.movement.from_square).color
        if king_side : rook_pos += 'h'
        else : rook_pos += 'a'
        if piece_color == ch.WHITE : rook_pos += '1'
        else : rook_pos += '8'
        return dt.convert_coordinates(rook_pos)

    def set_move(self, move : ch.Move) -> None :
        self.move.movement = move
        if self.move.movement is not None :
            if self.start_tile is None :
                self.__start_tile = self.game_displayer.get_tile(move.from_square)
            self.__dest_tile = self.game_displayer.get_tile(move.to_square)
            self.move.direction = (self.dest_tile.grid_x - self.start_tile.grid_x, 
                self.dest_tile.grid_y - self.start_tile.grid_y)
            self.move.move_type = self.get_move_type()
            self.update_color_last_move()
        else : 
            self.move.direction = None
            self.move.move_type = dt.MoveType.DEFAULT
            self.__start_tile = None
            self.__dest_tile = None
    
    def update_color_last_move(self) -> None:  
    # d'abord vider last_two_moves et remettre les couleurs par défaut et ensuite
    # rajouter start_tile et dest_tile dans last_two_moves et changer leur couleurs  
        for elem in self.__last_two_moves:  # reset the colors of the last two tiles
            if elem:  # only if elem is not None
                elem.reset_color()  # remettre à default
        self.__last_two_moves = []
        self.__last_two_moves.append(self.__start_tile)
        self.__last_two_moves.append(self.__dest_tile)
        self.__last_two_moves[0].change_color(dt.Colors.L_YELLOW)  # change the colors of the tiles we used
        self.__last_two_moves[1].change_color(dt.Colors.L_GREEN)

    def update(self) -> None :
        """Met à jour les éléments de la liste 'to_animate'"""
        verif = 0
        for widget, dest, direction in self._to_animate :
            widget.set_position(dt.Point(widget.position.x + direction[0], widget.position.y + direction[1]))
            widget.display(self.window)
            if (abs(dest.x - widget.position.x) <= 10 and abs(dest.y - widget.position.y) <= 10) :
                widget.set_position(dest)
                verif += 1
        self._animate = verif != len(self._to_animate)
        if not self._animate :
            self.clear_animations()

    def update_available_moves(self, tile : tl.Tile, is_choice : bool) -> None :
        for move in self.game.active_player_actions :
            str_move : str = move.uci()
            if str_move[:2] == tile.chess_position :
                dest : tl.Tile = self.game_displayer.get_tile(move.to_square)
                dest.set_choice(is_choice)

    def update_board_displayer(self, start_tile : tl.Tile = None, 
    dest_tile : tl.Tile = None, undo : bool = False) -> None :
        if start_tile is None or dest_tile is None :
            start_tile = self.start_tile  
            dest_tile = self.dest_tile
        if not undo :
            dest_tile.set_piece(start_tile.piece_displayer)
            start_tile.set_piece(None)
        else :
            piece_captured_type : int = self.game.board.piece_at(self.move.movement.to_square)
            start_tile.set_piece(dest_tile.piece_displayer)
            dest_tile.set_piece(None)
            if piece_captured_type is not None :
                dest_tile.set_piece(pieceD.PieceDisplayer(
                    ch.Piece(piece_captured_type.piece_type, not self.game.active_player)))

    def set_move_start_pos(self, tile : tl.Tile) -> None :
        if (not tile.is_clicked or 
        (self.start_tile is not None and tile != self.start_tile)) :
            self.update_available_moves(self.start_tile, is_choice = False)
        if tile.is_clicked:
            self.__start_tile = tile
            self.update_available_moves(tile, is_choice = True)
        else:
            self.__start_tile = None

    def set_move_dest_pos(self, tile) -> ch.Move :
        self.update_available_moves(self.start_tile, is_choice = False)
        uci : str = (self.start_tile.chess_position + tile.chess_position)
        return ch.Move.from_uci(uci)

    def is_promotion(self) -> bool :
        return (self.move.direction in [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0)] and
        ((self.start_tile.grid_x == 1 and self.game.active_player == ch.WHITE) 
        or (self.start_tile.grid_x == 6 and self.game.active_player == ch.BLACK))) 

    def is_castling(self) -> bool : return self.move.direction in [(0, 2), (0, -2)]

    def is_en_passant(self) -> bool :
        piece_captured_pos : tuple[int] = (self.start_tile.grid_x, 
            self.start_tile.grid_y + self.move.direction[1])
        piece_captured : ch.Piece = self.game.board.piece_at(
            56 - 8 * piece_captured_pos[0] + piece_captured_pos[1]) 
        return (self.move.direction in [(1, 1), (1, -1), (-1, 1), (-1, -1)] 
        and piece_captured is not None and piece_captured.color != self.game.active_player)

    def is_drop(self) -> bool : return ((self.dest_tile.piece_displayer is not None 
    and self.dest_tile.piece.color == (not self.game.active_player)) 
    or self.move.movement.drop is not None)

    def get_move_type(self) -> int :
        piece_moved = self.start_tile.piece if self.start_tile.piece_displayer is not None \
            else self.game.board.piece_at(self.move.movement.from_square) 
        if piece_moved.piece_type == ch.PAWN :
            if self.is_promotion() : return dt.MoveType.PROMOTION
            elif self.is_en_passant() : return dt.MoveType.EN_PASSANT
        elif piece_moved.piece_type == ch.KING :
            if self.is_castling() : return dt.MoveType.CASTLING
        if self.is_drop() : return dt.MoveType.DROP
        return dt.MoveType.DEFAULT

    def play_castling(self) -> None : 
        rook_start_pos : tuple[int] = self.get_casling_rook_pos()
        rook_dest_pos : tuple[int] = (rook_start_pos[0], 
            rook_start_pos[1] + (-2) if self.move.direction[1] == 2 else 3)
        start_tile : tl.Tile = self.game_displayer.get_tile(rook_start_pos)
        dest_tile : tl.Tile = self.game_displayer.get_tile(rook_dest_pos)
        self.update_board_displayer(start_tile, dest_tile)

    def play_en_passant(self) -> None :
        piece_captured_pos : tuple[int] = (self.start_tile.grid_x, 
            self.start_tile.grid_y + self.move.direction[1])
        tile : tl.Tile = self.game_displayer.get_tile(piece_captured_pos)
        # tile.set_piece(None)

    def play_promotion(self) -> None :
        piece : ch.Piece = ch.Piece(self.move.movement.promotion, 
            self.dest_tile.piece.color)
        self.dest_tile.set_piece(pieceD.PieceDisplayer(piece))

    def play_move(self) -> None :
        self.update_board_displayer()
        match self.move.move_type :
            case dt.MoveType.CASTLING : self.play_castling()
            case dt.MoveType.EN_PASSANT : self.play_en_passant()
            case dt.MoveType.PROMOTION : self.play_promotion()
        txt = ""
        if self.game.active_player and (isinstance(self.playerWhite, ia.Ai)):  # joueur blanc == ia
            txt = f'{self.move.movement} by {self.playerWhite.type_ia()} in {self.playerWhite.get_timer()} seconds' 
            if type(self.playerWhite) == ia.Minimax:
                txt += f', {self.playerWhite.nodes_expanded} nodes expanded.'
        elif not self.game.active_player and isinstance(self.playerBlack, ia.Ai):  # joueur noir == ia
            txt = f'{self.move.movement} by {self.playerBlack.type_ia()} in {self.playerBlack.get_timer()} seconds' 
            if type(self.playerBlack) == ia.Minimax:
                txt += f', {self.playerBlack.nodes_expanded} nodes expanded.'
        elif self.game.active_player:  # humain vs humain
            txt = f'{self.move.movement} by White'
            txt += "                     " # pour effacer la partie du texte qui reste inchangée (pas la bonne manière de faire, à remplacer sûrement)
        else:
            txt = f'{self.move.movement} by Black'
            txt += "                     "  # pour effacer la partie du texte qui reste inchangée

        self.game_displayer.menu_displayer.moves_displayer.add_text(txt)
            # self.game_displayer.menu_displayer.moves_displayer.l_texts[0].draw_background(pg.display.set_mode(dt.Utils.DEFAULT_WINDOW_WIDTH, dt.Utils.DEFAULT_WINDOW_HEIGHT))
        self.game.push_move(self.move.movement)

    def revert_promotion(self) -> None :
        piece : ch.Piece = ch.Piece(ch.PAWN, self.game.active_player)
        self.start_tile.set_piece(pieceD.PieceDisplayer(piece))

    def revert_castling(self) -> None :
        rook_start_pos : tuple[int] = self.get_casling_rook_pos()
        rook_dest_pos : tuple[int] = (rook_start_pos[0], 
            rook_start_pos[1] + (-2) if self.move.direction[1] == 2 else 3)
        start_tile : tl.Tile = self.game_displayer.get_tile(rook_start_pos)
        dest_tile : tl.Tile = self.game_displayer.get_tile(rook_dest_pos)
        self.update_board_displayer(dest_tile, start_tile)

    def revert_en_passant(self) -> None :
        piece : ch.Piece = ch.Piece(ch.PAWN, not self.game.active_player)
        piece_captured_pos : tuple[int] = (self.start_tile.grid_x, 
            self.start_tile.grid_y + self.move.direction[1])
        tile : tl.Tile = self.game_displayer.get_tile(piece_captured_pos)
        tile.set_piece(pieceD.PieceDisplayer(piece))
        self.set_move(None)

    def revert_move(self) -> None :
        self.set_move(self.game.pop_move())
        self.update_board_displayer(undo = True)
        match self.move.move_type :
            case dt.MoveType.CASTLING : self.revert_castling()
            case dt.MoveType.EN_PASSANT : self.revert_en_passant()
            case dt.MoveType.PROMOTION : self.revert_promotion()
        self.set_move(None)

    def handle_tile_selection(self, mouse_position : tuple[int]) -> None :
        for tile in self.game_displayer.board_displayer:
            if mouse_position in tile:
                if tile.piece_displayer and tile.piece.color == self.game.active_player:
                    tile.set_clicked(not tile.is_clicked)
                    self.set_move_start_pos(tile)
                elif self.start_tile is not None :
                    if tile.is_choice :
                        move : ch.Move = self.set_move_dest_pos(tile)
                        self.set_move(move)
                        if self.move.move_type == dt.MoveType.PROMOTION :  # if we arrive on a tile for promotion
                            self.game_displayer.pawn_promotion_popup.set_active(True)
                        else : self.play_move()
                    self.update_available_moves(self.start_tile, is_choice = False)
                    if self.move.move_type != dt.MoveType.PROMOTION : self.set_move(None)
            else :
                tile.set_clicked(False)

    def promote_pawn(self, piece : str) -> None :
        match piece :
            case "knight" : self.move.movement.promotion = ch.KNIGHT
            case "bishop" : self.move.movement.promotion = ch.BISHOP
            case "rook" : self.move.movement.promotion = ch.ROOK
            case "queen" : self.move.movement.promotion = ch.QUEEN
        self.play_move()
        self.set_move(None)

    def handle_popup_mouse_motion(self, event) -> None :
        pawn_promotion_popup = self.game_displayer.pawn_promotion_popup
        mouse_pos : tuple[int] = event.pos
        for widget in pawn_promotion_popup.content :
            if widget.name != "Text" :
                if mouse_pos in widget : 
                    widget.set_visited(True)
                else : 
                    widget.set_visited(False)

    def handle_popup_mouse_click(self, event) -> None :
        pawn_promotion_popup = self.game_displayer.pawn_promotion_popup
        mouse_pos : tuple[int] = event.pos
        for widget in pawn_promotion_popup.content :
            if widget.name != "text" :
                if mouse_pos in widget : 
                    widget.set_clicked(not widget.is_clicked)
                    if widget.is_clicked :
                        self.promote_pawn(widget.content.text)
                        pawn_promotion_popup.reset() 

    def handle_pawn_promotion(self, event) -> None :
        match event.type :
            case pg.MOUSEMOTION : self.handle_popup_mouse_motion(event)
            case pg.MOUSEBUTTONDOWN : self.handle_popup_mouse_click(event)

    def handle_mouse_motion(self, event) -> None :
        mouse_pos : tuple[int] = event.pos
        for tile in self.game_displayer.board_displayer :
            tile.set_visited(True) if mouse_pos in tile else tile.set_visited(False)

    def handle_mouse_click(self, event) -> None :
        mouse_pos : tuple[int] = event.pos
        if mouse_pos in self.game_displayer.board_displayer :
            self.handle_tile_selection(mouse_pos)
        elif mouse_pos in self.game_displayer.menu_displayer.reset_button_displayer :
            self.handle_reset_button_pressed()
        elif mouse_pos in self.game_displayer.menu_displayer.take_back_move :
            self.handle_take_back_move_pressed()

    def handle_take_back_move_pressed(self):
        if len(self.game.moves) > 0 :  # you must have done at least one move
                self.__start_tile = None  # in case the player clicked on a piece before trying to revert
                self.__dest_tile = None
                self.revert_move()    
        
    def handle_reset_button_pressed(self):
        self.game.reset()
        self.game_displayer.set_game(self.game)
        self.game_displayer.pawn_promotion_popup.reset()
        self.game_displayer.menu_displayer.moves_displayer.reset_state()
        
    def handle_key_pressed(self, event) -> None :
        key = event.key
        if key == pg.K_b or key == pg.K_r :
            if self.start_tile :
                self.start_tile.set_clicked(False)
                self.update_available_moves(self.start_tile, False)
        if key == pg.K_b :  # revert the last move
            if len(self.game.moves) > 0 :  # you must have done at least one move
                self.__start_tile = None  # in case the player clicked on a piece before trying to revert
                self.__dest_tile = None
                self.revert_move()
        if key == pg.K_r :  # reset the board
            self.game.reset()
            self.game_displayer.set_game(self.game)
            self.game_displayer.pawn_promotion_popup.reset()

    def handle_move(self, color: ch.Color, event):
        if (self.playerBlack == None and color == ch.BLACK) or (self.playerWhite == None and color == ch.WHITE): # Human player
            match event.type :
                case pg.MOUSEMOTION : self.handle_mouse_motion(event)
                case pg.MOUSEBUTTONDOWN : self.handle_mouse_click(event)
                case pg.KEYDOWN : self.handle_key_pressed(event)
        else:  # Ai is playing
            if color == ch.WHITE:
                move = self.playerWhite.move()
            else:
                move = self.playerBlack.move()
            #time.sleep(0.1) # Pour pas que les moves s'enchainent trop vite (si AI vs AI)
            self.__start_tile = None
            self.set_move(move)
            self.__mutex_display.acquire()
            try:
                self.play_move()
            finally:
                self.__mutex_display.release()
            self.game.next_round
        
            
    def handle_move_in_background(self, color: ch.Color, event):
        thread = threading.Thread(target=self.handle_move, args=(color, event))
        thread.start()
        return thread

    def handle(self, event) -> None :
        if self.game.state not in [dt.State.CHECKMATE, dt.State.STALEMATE] :
            if self.game_displayer.pawn_promotion_popup.is_active :  # when the popup of the promotion is active
                self.handle_pawn_promotion(event)
            else :
                if self.game.active_player and isinstance(self.playerWhite, ia.Ai) or not self.game.active_player and isinstance(self.playerBlack, ia.Ai): # To know if an AI is playing
                    if self.__thread is None or not self.__thread.is_alive():
                        if self.game.active_player : # White player
                            self.__thread = self.handle_move_in_background(ch.WHITE, event)
                        else:  # Black player
                            self.__thread = self.handle_move_in_background(ch.BLACK, event)
                else:
                    self.__mutex_move.acquire()
                    try:
                        if self.game.active_player: # White player
                            self.handle_move(ch.WHITE, event)
                        else:  # Black player
                            self.handle_move(ch.BLACK, event)
                    finally:
                        self.__mutex_move.release()
