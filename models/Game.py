import models.Board as Bd
import models.Pieces as Pcs
import Data as Dt
import models.Move as Mv
import itertools

class Game :
    """
    Représente une partie de jeu d'échecs

    Attributes
    ----------
    round : int
        représente le tour dans lequel la partie se trouve
    state : int
        représente l'état dans lequel la partie se trouve
    moves : list[Moves]
        la liste de tous les movemements effectués au long de la partie
    active_player_actions : list[Moves]
        la liste des actions valides pour le joueur actif
    board : Bd.Board
        le plateau de jeu
    active_player : int
        le joueur actif
    castling_rights : list[str]
        permet de savoir si les joueurs ont le droit d'effectuer le "castling"
    """

    def __init__(self, fen : str = None, ai = None) -> None :
        """
        Initialise une instance de Game

        Parameters
        ----------
        fen : str
            la partie d'échecs en notation fen
        ai : 
            l'intelligence artificielle qui va jouer la partie
        """
        self.__start_fen : str = fen if fen else Dt.Utils.DEFAULT_FEN
        self.__score : int = 0
        self._init_game()
        self.update_state()

    def _init_game(self) -> None :
        self.__round : int = 0
        self.__state : int = Dt.State.ONGOING
        self.__moves : list = []
        self.__active_player_actions : list[str] = []
        fen_tokens = self._parse_fen(self.__start_fen)
        self.__board : Bd.Board = Bd.Board(fen_tokens[0])
        self.__active_player : int = int(fen_tokens[1])
        self.__castling_rights : list[str] = fen_tokens[2].split("|")
        self.__kings_pos : list[Dt.Point] = [None, None]

        for piece0, piece1 in itertools.zip_longest(self.board.get_player_pieces(0), 
        self.board.get_player_pieces(1)) :
            if isinstance(piece0, Pcs.King) : self.__kings_pos[0] = piece0.position
            if isinstance(piece1, Pcs.King) : self.__kings_pos[1] = piece1.position
            if self.__kings_pos[0] and self.__kings_pos[1] : break

    def _parse_fen(self, fen : str) -> list[str] :
        """Renvoie une liste de tout les composants du fen de la partie"""
        fen_tokens : list[str] = fen.strip().split(" ") if fen else None
        return fen_tokens

    ###########
    # GETTERS #
    ###########
    @property
    def board(self) -> Bd.Board :
        """Renvoie la plateau de jeu de la partie"""
        return self.__board

    @property
    def active_player(self) -> int :
        """Renvoie le numéro du joueur actif"""
        return self.__active_player

    @property
    def round(self) -> int :
        """Renvoir le tour dans lequel se trouve la partie"""
        return self.__round

    @property
    def state(self) -> int :
        """Renvoie l'état dans lequel se trouve la partie"""
        return self.__state

    @property
    def moves(self) -> list :
        """Renvoie la liste de tout les mouvments éfectués dans la partie"""
        return self.__moves

    @property
    def active_player_actions(self) -> list[str] :
        """Renvoie la liste des actions valides pour le joueur actif"""
        if len(self.__active_player_actions) == 0 : 
            self.__active_player_actions = self._valid_actions()
        return self.__active_player_actions

    @property
    def activer_player_castling_rights(self) -> str :
        """Renvoie les droits de 'castling' du joueur actif"""
        return self.__castling_rights[self.active_player]

    @property
    def is_over(self) -> bool :
        return self.state == Dt.State.CHECKMATE or self.state == Dt.State.STALEMATE

    def get_last_move(self, piece : Pcs.Piece) -> Mv.Move :
        for i in range(len(self.moves) - 1, -1, -1) :
            move : Mv.Move = self.moves[i]
            if move.piece_moved == piece :
                return move

    ###########
    # SETTERS #
    ###########
    def set_board(self, board : str = Dt.Utils.DEFAULT_BOARD_FEN) -> None :
        """
        Modifie le plateau de jeu de la partie

        Parameters
        ----------
        board : str
            le nouveau plateau de jeu en notation fen
        """
        self.__board.set_board(board)

    def set_active_player(self, active_player : int) -> None :
        """
        Change le joueur actif de la partie

        Parameters
        ----------
        active_player : int
            le nouveau joueur actif
        """
        self.__active_player = active_player

    def set_casling_rights(self) -> None :
        """
        Modifie les droits de 'castling' des joueurs

        castling_rights : list[str]
            les noueveaux droits de 'castling'
        """
        row : int = self.board.size
        king_start_pos : list[str] = ["e1", f"e{row}"]
        self.__active_player = (self.round - 1) % 2
        if (Dt.convert_coordinates(self.__kings_pos[self.active_player]) 
        == king_start_pos[self.active_player]) :
            self.__castling_rights[self.active_player] = ""
            rook_pos : list[str] = None
            col : str = chr(ord('a') + self.board.size - 1)

            if self.active_player == 0 :
                rook_pos = ["a1", f"{col}1"]
            else :
                rook_pos = [f"a{row}", f"{col}{row}"]
        
            can_castle : bool = [True, True]
            for i, position in enumerate(rook_pos) :
                piece : Pcs.Piece = self.board[position]
                if piece is None or piece.name != "rook" :
                    can_castle[i] = [False]

            if all(can_castle) :
                self.__castling_rights[self.active_player] += "K" if self.active_player == 0 else "k"
                self.__castling_rights[self.active_player] += "Q" if self.active_player == 0 else "q"
            else :
                self.__castling_rights[self.active_player] = None
        else :
            self.__castling_rights[self.active_player] = None
        self.__active_player = self.round % 2

    def set_state(self, state : int) -> None :
        """
        Modifie l'état de la partie

        Parameters
        ----------
        state : int
            le nouvel état de la partie
        """
        self.__state = state

    def _add_move(self, move : Mv.Move) -> None : 
        """
        Ajouter un mouvement dans la liste des mouvements de la partie

        Parameters
        ----------
        move : Moves
            le mouvement à ajouter
        """
        self.__moves.append(move)

    ###################
    # OTHER FUNCTIONS #
    ###################
    def _set_move_type(self, move : Mv.Move) -> None :
        if isinstance(move.piece_moved, Pcs.Pawn) :
            if self.is_promotion(move) :
                move.set_type(Dt.MoveType.PROMOTION)
            elif self.is_en_passant(move) :
                direction : Dt.Point = move.dest_pos - move.start_pos
                move.set_type(Dt.MoveType.EN_PASSANT)
                move.set_piece_captured(self.board[
                    Dt.Point(move.start_pos.x, 
                    move.start_pos.y +  direction.y)
                ])
        elif isinstance(move.piece_moved, Pcs.King) :
            if self.is_castling(move) :
                move.set_type(Dt.MoveType.CASTLING)
                self._get_castling_rook(move)

    def _get_castling_rook(self, move : Mv.Move) -> None :
        rook_pos : str = self.get_castling_rook_start_pos(move)
        move.set_castling_rook(self.board[rook_pos])

    def get_castling_rook_start_pos(self, move : Mv.Move) -> Dt.Point :
        king_side : bool = move.dest_pos - move.start_pos == (0, 2) 
        col : str = chr(ord('a') + self.board.size - 1)
        row : int = self.board.size
        rook_pos : str = ""
        if king_side : rook_pos += f"{col}"
        else : rook_pos += 'a'
        if move.piece_moved.owner == 0 : rook_pos += '1'
        else : rook_pos += f"{row}"
        return rook_pos

    def push_move(self, move : Mv.Move) -> None :
        self._set_move_type(move)  # decide wether it's a castling, a normal move, a promotion or a "en passant" 
        move.piece_moved.set_position(move.dest_pos)
        if move.move_type == Dt.MoveType.CASTLING and move.castling_rook is not None :
            self._push_castling(move)
            self.__kings_pos[self.active_player] = move.dest_pos
            self.__castling_rights[self.active_player] = None
        elif move.move_type == Dt.MoveType.EN_PASSANT :
            self._push_en_passant(move)
        elif move.move_type == Dt.MoveType.DEFAULT:
            self._push_default(move)
        self.__round += 1
        self.set_active_player(self.round % 2)
        self._add_move(move)
        self.__active_player_actions.clear()

    def _push_castling(self, move : Mv.Move) -> None :
        rook_move : Mv.Move = None
        if move.castling_rook.position.y == 0 :
            rook_dest_pos : Dt.Point = move.castling_rook.position + (0, 3)
        else :
            rook_dest_pos : Dt.Point = move.castling_rook.position + (0, -2)
        rook_move = Mv.Move(move.castling_rook.position, rook_dest_pos, self.board)
        rook_move.piece_moved.set_position(rook_move.dest_pos)
        self.update_board(move)
        self.update_board(rook_move)

    def _push_en_passant(self, move : Mv.Move) -> None :
        self.board[move.piece_captured.position] = None
        self.update_board(move)

    def _push_default(self, move : Mv.Move) -> None :
        if isinstance(move.piece_moved, Pcs.King) :
            self.__kings_pos[self.active_player] = move.dest_pos
            self.__castling_rights[self.active_player] = None
        self.update_board(move)
        if (isinstance(move.piece_moved, Pcs.Pawn) and move.piece_moved.can_double_start) :
            move.piece_moved.set_double_start(False)
        elif isinstance(move.piece_moved, Pcs.Rook):
            self.set_casling_rights()

    def pop_move(self) -> Mv.Move :
        """"Annule le dernier mouvement efféctué dans la partie"""
        move : Mv.Move = self.__moves.pop()
        move.piece_moved.set_position(move.start_pos)
        if move.move_type == Dt.MoveType.CASTLING and move.castling_rook is not None :
            self._pop_castling(move)
            self.__kings_pos[move.piece_moved.owner] = move.start_pos
            self.set_casling_rights()
        elif move.move_type == Dt.MoveType.EN_PASSANT :
            self._pop_en_passant(move)
        else :
            self._pop_default(move)
        self.__round -= 1
        self.set_active_player(self.__round % 2)
        self.__active_player_actions.clear()
        return move

    def _pop_default(self, move : Mv.Move) -> None :
        if isinstance(move.piece_moved, Pcs.King) :
            self.__kings_pos[move.piece_moved.owner] = move.start_pos
        if move.piece_captured :
            move.piece_captured.set_position(move.dest_pos)
        self.update_board(move, undo = True)
        if isinstance(move.piece_moved, Pcs.Pawn) :
            self._pop_pawn_move(move)
        if isinstance(move.piece_moved, Pcs.King) :
            self.set_casling_rights()

    def _pop_pawn_move(self, move : Mv.Move) -> None :
        if move.move_type == Dt.MoveType.PROMOTION :
            self._pop_promotion(move)
        elif move.move_type == Dt.MoveType.EN_PASSANT :
            self._pop_en_passant(move)
        if (not move.piece_moved.can_double_start
        and ((move.start_pos.x == self.board.size - 2 and move.piece_moved.owner == 0)
        or (move.start_pos.x == 1 and move.piece_moved.owner == 1))) :
            move.piece_moved.set_double_start(True)

    def _pop_en_passant(self, move : Mv.Move) -> None :
        self.board[move.piece_captured.position] = move.piece_captured
        self.update_board(move, undo = True)
        self.board[move.dest_pos] = None

    def _pop_promotion(self, move : Mv.Move) -> None :
        pawn : Pcs.Pawn = Pcs.Pawn(move.start_pos, move.piece_moved.owner)
        self.board[move.start_pos] = pawn

    def _pop_castling(self, move : Mv.Move) -> None :
        rook_move : Mv.Move = None
        if move.castling_rook.position.y == 3 :
            rook_dest_pos : Dt.Point = move.castling_rook.position + (0, -3)
        else :
            rook_dest_pos : Dt.Point = move.castling_rook.position + (0, 2)
        rook_move = Mv.Move(move.castling_rook.position, rook_dest_pos, self.board)
        rook_move.piece_moved.set_position(rook_move.dest_pos)
        self.update_board(move, undo = True)
        self.update_board(rook_move)

    def is_promotion(self, move : Mv.Move) -> bool :
        return (move.piece_moved.owner == 0 and move.dest_pos.x == 0) or (move.piece_moved.owner == 1 and move.dest_pos.x == self.board.size - 1)

    def is_castling(self, move : Mv.Move) -> bool :
        return move.dest_pos - move.start_pos in [(0, 2), (0, -2)]

    def is_en_passant(self, move : Mv.Move) -> bool :
        if move.piece_captured is None :
            direction : Dt.Point = move.dest_pos - move.start_pos
            if direction in [(-1, 1), (1, 1), (-1, -1), (1, -1)] :
                dest = move.start_pos + (0, direction.y)
                piece_captured : Pcs.Piece = self.board[dest]
                if (isinstance(piece_captured, Pcs.Pawn) 
                and not piece_captured.can_double_start
                and piece_captured.owner != move.piece_moved.owner) :
                    p_captured_move : Mv.Move = self.get_last_move(piece_captured)
                    if (p_captured_move.dest_pos - p_captured_move.start_pos 
                    in [(-2, 0), (2, 0)]) :
                        return True
        return False

    def _available_actions(self) -> list[str] :
        """Renvoie une liste de toutes les actions possibles pour le joueur actif"""
        actions : set[str] = set()
        for piece in self.board.get_player_pieces(self.active_player) :
            piece.available_actions(self, actions)
        return actions

    def _valid_actions(self) -> set[str] :
        """Renvoie une liste de toutes les actions valides pour le joueur actif"""
        actions = self._available_actions()
        return_action = set()
        for elem in actions:
            move : Mv.Move = Mv.Move(Dt.convert_coordinates(elem[:2]), Dt.convert_coordinates(elem[2:]), self.board)
            self.push_move(move)
            if not self._is_in_check():
                return_action.add(elem)
            self.set_active_player(self.round % 2)
            self.pop_move()
        return return_action

        # for i in range(len(actions) - 1, -1, -1) :
        #     move : Mv.Move = Mv.Move(Dt.convert_coordinates(actions[i][:2]), 
        #         Dt.convert_coordinates(actions[i][2:]), self.board)
        #     self.push_move(move)
        #     if self._is_in_check() :
        #         actions.remove(actions[i])
        #     self.set_active_player(self.round % 2)
        #     self.pop_move()
        # return actions

    def _is_in_check(self) -> bool :
        """Vérifie si la partie se trouve dans l'état 'échec' (check)"""
        other_player_actions : set[str] = self._available_actions()
        self.set_active_player((self.round - 1) % 2)
        for other_action in other_player_actions :
            if Dt.convert_coordinates(other_action[2:]) == self.__kings_pos[self.active_player] :
                return True
        return False

    def _is_in_checkmate(self) -> bool :
        """Vérifie si la partie se trouve dans l'état 'échec et mat' (checkmate)"""
        return len(self.active_player_actions) == 0 and self._is_in_check()

    def _is_in_stalemate(self) -> bool :
        """Vérifie si la partie se trouve dans l'état 'match nul' (stalemate)"""
        return len(self.active_player_actions) == 0 and not self._is_in_check()

    def update_board(self, move : Mv.Move, undo : bool = False) -> None :
        """
        Met à jour le plateau de jeu de la partie
        
        Parameters
        ----------
        move : Mv.Move
            le mouvement à effectuer
        undo : bool
            permet de savoir s'il le mouvement à effectuer est son inverse 
        """
        if undo :
            self.board[move.dest_pos] = move.piece_captured
            self.board[move.start_pos] = move.piece_moved
        else :
            self.board[move.dest_pos] = move.piece_moved
            self.board[move.start_pos] = None

    def update_state(self) -> None :
        """Met à jour l'état de la partie"""
        actions = self._valid_actions()
        self.__round += 1
        if len(actions) == 0 :  # the game is over or it's a draw
            if self._is_in_check() : self.set_state(Dt.State.CHECKMATE)
            else : self.set_state(Dt.State.STALEMATE)
        else :
            if self._is_in_check() : self.set_state(Dt.State.CHECK)
            else : self.set_state(Dt.State.ONGOING)
        self.__round -= 1
        self.__active_player_actions = actions

    def reset(self) -> None :
        """Réinitialise à la partie"""
        self._init_game()
        self.update_state()

    def __str__(self) -> str :
        str_game : str = f"{self.__repr__()}\n\n{str(self.board)}"
        return str_game

    def __repr__(self) -> str :
        str_game : str = "Game\n"
        str_game += f"board : {self.board.fen}\n"
        str_game += f"player 1 : {self.board.get_player_pieces(0)}\n"
        str_game += f"player 2 : {self.board.get_player_pieces(1)}"
        return str_game