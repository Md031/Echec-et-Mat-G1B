import pygame as pg
import chess as ch
import data as dt
import views.pieceDisplayer as pieceD
import views.widget as wdgt
import views.text as txt

class Tile(wdgt.Widget) :
    def __init__(self, position : tuple[int], grid_position : tuple[int], color : pg.Color, piece : pieceD.PieceDisplayer = None, size : int = dt.Utils.DEFAULT_TILE_DIMENSIONS) -> None :
        super().__init__(position, "Tile")
        self.__surface : pg.Surface = pg.Surface((size, size))
        self.surface.fill(color)
        self.__color = color
        self.__grid_position : tuple[int] = grid_position
        self.__piece_diplayer : pieceD.PieceDisplayer = piece
        self.__visited : bool = False
        self.__clicked : bool = False
        self.__choice : bool = False
        self.__text : list[txt.Text] = [txt.Text((position[0], position[1]), "", pg.font.Font("font/sh-pinscher/SHPinscher-Regular.otf", 18))]

    @property
    def surface(self) -> pg.Surface : return self.__surface

    @property
    def center(self) -> tuple[int] : 
        return (self.x + dt.Utils.DEFAULT_TILE_DIMENSIONS // 2, 
            self.y + dt.Utils.DEFAULT_TILE_DIMENSIONS // 2)

    def change_txt(self, new_txt: str, pos: int = 0) -> None :
        self.__text[pos].set_txt(new_txt)

    def change_coord(self, new_coord : tuple[int], pos: int = 0) -> None:
        self.__text[pos].set_coord(new_coord)

    def two_txt(self) -> None:
        temp = txt.Text(self.position, "", pg.font.Font("font/sh-pinscher/SHPinscher-Regular.otf", 18))
        self.__text.append(temp)

    def change_color(self, new_color : pg.Color = dt.Colors.BLACK) -> None:
        self.surface.fill(new_color)

    def reset_color(self) -> None:
        self.surface.fill(self.__color)

    @property
    def center_x(self) -> int : return self.center[0]

    @property
    def center_y(self) -> int : return self.center[1]

    @property
    def grid_position(self) -> tuple[int] : return self.__grid_position

    @property
    def grid_x(self) -> tuple[int] : return self.__grid_position[0]

    @property
    def grid_y(self) -> tuple[int] : return self.__grid_position[1]

    @property
    def chess_position(self) -> tuple[int] : return dt.convert_coordinates(self.grid_position)

    @property
    def piece_displayer(self) -> pieceD.PieceDisplayer : return self.__piece_diplayer

    @property
    def piece(self) -> ch.Piece : return self.piece_displayer.piece

    @property
    def is_visited(self) -> bool : return self.__visited

    @property
    def is_clicked(self) -> bool : return self.__clicked

    @property
    def is_choice(self) -> bool : return self.__choice

    def set_piece(self, value : pieceD.PieceDisplayer) -> None :
        self.__piece_diplayer = value
        if self.piece_displayer is not None : 
            self.piece_displayer.set_position(
                (self.x + dt.Utils.DEFAULT_TILE_OFFSET, self.y + dt.Utils.DEFAULT_TILE_OFFSET))

    def set_visited(self, value : bool) -> None : self.__visited = value

    def set_clicked(self, value : bool) -> None : self.__clicked = value

    def set_choice(self, value : bool) -> None : self.__choice = value

    def reset(self) -> None : return super().reset()

    def __contains__(self, pos : tuple[int]) -> bool :
        x, y = pos
        return (self.x < x < self.x + dt.Utils.DEFAULT_TILE_DIMENSIONS 
            and self.y < y < self.y + dt.Utils.DEFAULT_TILE_DIMENSIONS)

    def __eq__(self, value : object) -> bool :
        if isinstance(value, Tile) :
            return (self.grid_position == value.grid_position and self.piece == value.piece)

    def display(self, window) -> None :
        window.screen.blit(self.__surface, self.position)
        for elem in self.__text:
            elem.display(window)
        if self.is_clicked :
            pg.draw.rect(window.screen, dt.Colors.RED, [self.x, self.y, 
                dt.Utils.DEFAULT_TILE_DIMENSIONS, dt.Utils.DEFAULT_TILE_DIMENSIONS], 2)
        elif self.is_visited :
            pg.draw.rect(window.screen, dt.Colors.GREEN, [self.x, self.y, 
                dt.Utils.DEFAULT_TILE_DIMENSIONS, dt.Utils.DEFAULT_TILE_DIMENSIONS], 1)
        if self.piece_displayer :
            self.piece_displayer.display(window)
        if self.is_choice : # the move possible for the selected pawn
            if self.piece_displayer is None : color : pg.Color = dt.Colors.YELLOW
            else : color : pg.Color = dt.Colors.PURPLE
            pg.draw.circle(window.screen, color, self.center, 10)

    def __str__(self) -> str : return  f"{self.name}({self.position}, {self.piece_displayer})"
