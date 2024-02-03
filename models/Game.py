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
        self.__castling_rights : list[str] = fen_tokens[2]
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
        # if len(self.__active_player_actions) == 0 : self._valid_actions()
        return self.__active_player_actions

    @property
    def activer_player_castling_rights(self) -> str :
        """Renvoie les droits de 'castling' du joueur actif"""
        self.__castling_rights[self.active_player]

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

    def set_casling_rights(self, castling_rights : str) -> None :
        """
        Modifie les droits de 'castling' des joueurs

        castling_rights : list[str]
            les noueveaux droits de 'castling'
        """
        self.__castling_rights = castling_rights

    # def next_round(self) -> None :
    #     """Fait passer la partie au tour suivant"""
    #     self.__round += 1
    #     self.set_active_player(self.round % 2)

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
    def push_move(self, move : Mv.Move) -> None :
        move.piece_moved.set_position(move.dest_pos)
        if move.piece_moved.name == "king" :
            self.__kings_pos[move.piece_moved.owner] = move.dest_pos
        if move.piece_captured :
            self._capture(move.piece_captured)
        self._update_board(move)
        self.__round += 1
        self.set_active_player(self.round % 2)
        self._add_move(move)
        if (move.piece_moved.name == "pawn" and move.piece_moved.can_double_start) :
            move.piece_moved.set_double_start(False)
        self.__active_player_actions.clear()

    def pop_move(self) -> Mv.Move :
        """"Annule le dernier mouvement efféctué dans la partie"""
        self.__round -= 1
        self.set_active_player(self.round % 2)
        move : Mv.Move = self.__moves.pop()
        move.piece_moved.set_position(move.start_pos)
        if move.piece_moved.name == "king" :
            self.__kings_pos[move.piece_moved.owner] = move.start_pos
        if move.piece_captured :
            move.piece_captured.set_position(move.dest_pos)
            self.board.add_piece(move.piece_captured, move.piece_captured.owner)
        self._update_board(move, undo = True)
        if (move.piece_moved.name == "pawn" 
        and not move.piece_moved.can_double_start
        and ((move.start_pos.x == 6 and move.piece_moved.owner == 0) 
        or (move.start_pos.x == 1 and move.piece_moved.owner == 1))) :
            move.piece_moved.set_double_start(True)
        self.__active_player_actions.clear()
        return move

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
            self.push_move(move)
            self.set_active_player((self.round - 1) % 2)
            if self._is_in_check() :
                actions.remove(action)
            self.pop_move()
        return actions

    def _is_in_check(self) -> bool :
        """Vérifie si la partie se trouve dans l'état 'échec' (check)"""
        self.set_active_player(self.round % 2)
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

    def _capture(self, piece : Pcs.Piece) -> None :
        """
        Effectue l'action de manger une pièce

        Parameters
        ----------
        piece : Pcs.Piece
            la pièce à manger
        """
        self.__board.capture(piece)

    def _update_board(self, move : Mv.Move, undo : bool = False) -> None :
        """
        Met à jour le plateau de jeu de la partie
        
        Parameters
        ----------
        move : Mv.Move
            le mouvement à effectuer
        undo : bool
            permet de savoir s'il le mouvement à effectuer est son inverse 
        """
        self.board[move.dest_pos] = move.piece_moved if not undo else move.piece_captured 
        self.board[move.start_pos] = None if not undo else move.piece_moved

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
