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
            if piece0.name == "king" : self.__kings_pos[0] = piece0.position
            if piece1.name == "king" : self.__kings_pos[1] = piece1.position
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
        return self.__active_player_actions

    @property
    def activer_player_castling_rights(self) -> str :
        """Renvoie les droits de 'castling' du joueur actif"""
        return self.__castling_rights[self.active_player]

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
        self.__castling_rights[self.active_player] = ""
        rook_pos: list[str]  = ["a1, h1"] if self.active_player == 0 else ["a8, h8"]
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

    def _add_action(self, action : str) -> None : 
        """
        Ajoute un mouvement dans la liste des actions valides pour le joueur actif

        Parameters
        ----------
        action : Moves
            le mouvement à ajouter
        """
        self.__active_player_actions.append(action)

    ###################
    # OTHER FUNCTIONS #
    ###################
    def _set_move_type(self, move : Mv.Move) -> None :
        if self.is_promotion(move) :
            move.set_type(Dt.MoveType.PROMOTION)
        elif self.is_castling(move) :
            move.set_type(Dt.MoveType.CASTLING)
            self._get_castling_rook(move)
            self.set_casling_rights()
        elif self.is_en_passant(move) :
            ...

    def _get_castling_rook(self, move : Mv.Move) -> None :
        king_side : bool = move.dest_pos - move.start_pos == (0, 2) 
        rook_pos : str = ""
        if king_side : rook_pos += "h"
        else : rook_pos += "a"
        if self.active_player == 0 : rook_pos += "1"
        else : rook_pos += "8"
        move.set_castling_rook(self.board[rook_pos])

    def push_move(self, move : Mv.Move) -> None :
        move.piece_moved.set_position(move.dest_pos)
        if move.move_type == Dt.MoveType.CASTLING :
            self._push_castling(move)
            self.__kings_pos[self.active_player] = move.dest_pos
        elif move.move_type == Dt.MoveType.EN_PASSANT :
            ...
        else :
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

    def _push_default(self, move : Mv.Move) -> None :
        if move.piece_moved.name == "king" :
            self.__kings_pos[self.active_player] = move.dest_pos
        self.update_board(move)
        if (move.piece_moved.name == "pawn" and move.piece_moved.can_double_start) :
            move.piece_moved.set_double_start(False)
        if move.piece_moved.name in ["rook", "king"] :
            self.set_casling_rights()

    def pop_move(self) -> Mv.Move :
        """"Annule le dernier mouvement efféctué dans la partie"""
        move : Mv.Move = self.__moves.pop()
        move.piece_moved.set_position(move.start_pos)
        if move.move_type == Dt.MoveType.CASTLING :
            self._pop_castling(move)
            self.__kings_pos[move.piece_moved.owner] = move.start_pos
        elif move.move_type == Dt.MoveType.EN_PASSANT :
            ...
        else :
            # move.piece_moved.set_position(move.start_pos)
            self._pop_default(move)
        self.__round -= 1
        self.set_active_player(self.__round % 2)
        self.__active_player_actions.clear()
        return move

    def _pop_default(self, move : Mv.Move) -> None :
        if move.piece_moved.name == "king" :
            self.__kings_pos[move.piece_moved.owner] = move.start_pos
        if move.piece_captured :
            move.piece_captured.set_position(move.dest_pos)
            # self.board.add_piece(move.piece_captured, move.piece_captured.owner)
        self.update_board(move, undo = True)
        if move.move_type == Dt.MoveType.PROMOTION :
            self._pop_promotion(move)
        if (move.piece_moved.name == "pawn" 
        and not move.piece_moved.can_double_start
        and ((move.start_pos.x == 6 and move.piece_moved.owner == 0)
        or (move.start_pos.x == 1 and move.piece_moved.owner == 1))) :
            move.piece_moved.set_double_start(True)
        if move.piece_moved.name in ["rook", "king"] :
            self.set_casling_rights()

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
        if move.piece_moved.name == "pawn" :
            if ((move.piece_moved.owner == 0 and move.dest_pos.x == 0) or 
            (move.piece_moved.owner == 1 and move.dest_pos.x == self.board.size[0] - 1)) :
                return True
            else : return False

    def is_castling(self, move : Mv.Move) -> bool :
        if (isinstance(move.piece_moved, Pcs.King) and 
        move.dest_pos - move.start_pos in [(0, 2), (0, -2)]) : 
            return True
        else :
            return False

    def is_en_passant(self, move : Mv.Move) -> bool :
        ...

    def _available_actions(self) -> list[str] :
        """Renvoie une liste de toutes les actions possibles pour le joueur actif"""
        actions : list[str] = []
        for piece in self.board.get_player_pieces(self.active_player) :
            actions.extend(piece.available_actions(self))
        return actions

    def _valid_actions(self) -> list[str] :
        """Renvoie une liste de toutes les actions valides pour le joueur actif"""
        actions = self._available_actions()
        for i in range(len(actions) - 1, -1, -1) :
            action : str = actions[i]
            move : Mv.Move = Mv.Move(Dt.convert_coordinates(action[:2]), 
                Dt.convert_coordinates(action[2:]), self.board)
            self._set_move_type(move)
            self.push_move(move)
            if self._is_in_check() :
                actions.remove(action)
            self.set_active_player(self.round % 2)
            self.pop_move()
        return actions

    def _is_in_check(self) -> bool :
        """Vérifie si la partie se trouve dans l'état 'échec' (check)"""
        other_player_actions : list[str] = self._available_actions()
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

    def is_over(self) -> bool :
        return self.state == Dt.State.CHECKMATE or self.state == Dt.State.STALEMATE

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
        self.__active_player_actions = self._valid_actions()
        self.__round += 1
        if len(self.active_player_actions) == 0 :
            if self._is_in_check() : self.set_state(Dt.State.CHECKMATE)
            else : self.set_state(Dt.State.STALEMATE)
        else :
            if self._is_in_check() : self.set_state(Dt.State.CHECK)
            else : self.set_state(Dt.State.ONGOING)
        self.__round -= 1

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
