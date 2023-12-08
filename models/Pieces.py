import Data as Dt
import copy

class Piece :
    """
    """

    def __init__(self, position : Dt.Point, owner : int, image_type : str, name : str, \
        symbol : str, icon : str) -> None :
        """
        """
        self._name  : str = name
        self._symbol : str = symbol
        self._position : Dt.Point = position
        self._owner  : int = owner
        self._image_filename : str = f"images/{image_type}/W{self.name}.png" if self.owner == 0 \
            else f"images/{image_type}/B{self.name}.png"
        self._icon : str = icon

    ###########
    # GETTERS #
    ###########
    @property
    def name(self) -> str : return self._name

    @property
    def symbol(self) -> str : return self._symbol

    @property
    def position(self) -> Dt.Point : return self._position

    @property
    def chess_positon(self) -> Dt.Point :
        return Dt.convert_coordinates(self.position)

    @property
    def owner(self) -> int : return self._owner

    @property
    def image_filename(self) -> str : return self._image_filename

    @property
    def icon(self) -> str : return self._icon

    ###########
    # SETTERS #
    ###########
    def set_position(self, position : Dt.Point) -> None : self._position = position

    ###################
    # OTHER FUNCTIONS #
    ###################
    def available_actions(self, game) -> list[str] :
        """"""
        actions : list[str] = []
        directions : list[tuple[int]] = Dt.Utils.DEFAULT_PIECES_DIRECTIONS[self.name]
        dest : Dt.Point | list[Dt.Point] = None
        if self.name == "pawn" :
            for direction in directions[self.owner] :
                dest = copy.copy(self.position)
                dest += direction
                if dest in game.board :
                    if (direction == (-2, 0) or direction == (2, 0)) and self.can_double_start \
                    and game.board[dest] is None :
                        actions.append(self.chess_positon + Dt.convert_coordinates(dest))
                    elif direction != (1, 0) and direction != (-1, 0) and \
                    (direction[0] == -1 and self.owner == 0 or direction[0] == 1 and self.owner == 1) :
                        if game.board[dest] and game.board[dest].owner != self.owner :
                            actions.append(self.chess_positon + Dt.convert_coordinates(dest))
                    elif game.board[dest] is None :
                        actions.append(self.chess_positon + Dt.convert_coordinates(dest))
        elif self.name == "knight" or self.name == "king" :
            for direction in directions :
                dest : Dt.Point = copy.copy(self.position)
                dest += direction
                if dest in game.board and (game.board[dest] is None or game.board[dest].owner != self.owner) :
                    actions.append(self.chess_positon + Dt.convert_coordinates(dest))
        else :
            available_directions = [True] * len(directions)
            dest = [copy.copy(self.position) for i in range(len(directions))]
            while available_directions.count(False) != len(directions) :
                for i in range(len(dest)) :
                    available, direction = available_directions[i], directions[i]
                    if available :
                        dest[i] += direction
                        if dest[i] in game.board and (game.board[dest[i]] is None or game.board[dest[i]].owner != self.owner) :
                            actions.append(self.chess_positon + Dt.convert_coordinates(dest[i]))
                        else :
                            available_directions[i] = False
        return actions

    def __str__(self) -> str : 
        return f"{self.icon} ({self.name}) | pos : {self.chess_positon} {self.position} | owner : {self.owner}"

    def __repr__(self) -> str : return str(self)

    def __eq__(self, __value: object) -> bool :
        if isinstance(__value, Piece) :
            return (__value.name == self.name and __value.chess_positon == self.chess_positon \
                and __value.player == self.player)
        else :
            return False

class Pawn(Piece) :
    """
    """

    def __init__(self, position : Dt.Point, owner : int, image_type : str = "classic") -> None :
        """
        """
        super().__init__(position, owner, image_type, "pawn", "", "♙")
        self.__double_start : bool = True

    ###########
    # GETTERS #
    ###########
    @property
    def can_double_start(self) -> bool : return self.__double_start

    ###########
    # SETTERS #
    ###########
    def give_up_double_start(self) -> None : self.__double_start = False

    ###################
    # OTHER FUNCTIONS #
    ###################
    def available_actions(self, board) -> list[str] :
        return super().available_actions(board)

class Knight(Piece) :
    """
    """

    def __init__(self, position : Dt.Point, owner : int, image_type : str = "classic") -> None :
        """
        """
        super().__init__(position, owner, image_type, "knight", "N", "♘")

    def available_actions(self, board) -> list[str] :
        return super().available_actions(board)

class Bishop(Piece) :
    """
    """

    def __init__(self, position : Dt.Point, owner : int, image_type : str = "classic") -> None :
        """
        """
        super().__init__(position, owner, image_type, "bishop", "B", "♗")

    def available_actions(self, board) -> list[str] :
        return super().available_actions(board)

class Rook(Piece) :
    """
    """

    def __init__(self, position : Dt.Point, owner : int, image_type : str = "classic") -> None :
        """
        """
        super().__init__(position, owner, image_type, "rook", "R", "♖")

    def available_actions(self, board) -> list[str]:
        return super().available_actions(board)

class Queen(Piece) :
    """
    """

    def __init__(self, position : Dt.Point, owner : int, image_type : str = "classic") -> None :
        """
        """
        super().__init__(position, owner, image_type, "queen", "Q", "♕")

    def available_actions(self, board) -> list[str]:
        return super().available_actions(board)

class King(Piece) :
    """
    """

    def __init__(self, position : Dt.Point, owner : int, image_type : str = "classic") -> None :
        """
        """
        super().__init__(position, owner, image_type, "king", "K", "♔")

    def available_actions(self, board) -> list[str] :
        return super().available_actions(board)
