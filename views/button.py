import pygame as Pg
import data as dt
import views.widget as wdgt

class Button(wdgt.Widget) :

    def __init__(self, position: tuple[int], size : tuple[int], content : wdgt.Widget = None, 
    button_type : int = dt.ButtonType.NO_ANIMATION, color : Pg.Color = dt.Colors.BEIGE, 
    visited_color : Pg.Color = dt.Colors.BROWN, clicked_color : Pg.Color = dt.Colors.BROWN) :
        super().__init__(position, "button")
        self.__size : tuple[int] = size
        self.__content : wdgt.Widget = content
        self.__visited : bool = False
        self.__clicked : bool = False
        self.__type : int = button_type
        self.__surface : Pg.Surface = Pg.Surface(self.size)
        self.__colors : dict[str : Pg.Color] = {"default" : color, "visited" : visited_color, "clicked" : clicked_color}
        self.__surface.fill(self.__colors["default"])

    @property
    def size(self) -> tuple[int] : return self.__size

    @property
    def content(self) -> wdgt.Widget : return self.__content

    @property
    def is_visited(self) -> bool : return self.__visited

    @property
    def is_clicked(self) -> bool : return self.__clicked

    @property
    def button_type(self) -> int : return self.__type

    def set_clicked(self, value : bool) -> None : self.__clicked = value

    def set_visited(self, value : bool) -> None : self.__visited = value

    def __contains__(self, coords : tuple[int]) -> bool :
        return (self.x < coords[0] < self.x + self.size[0] and
        self.y < coords[1] < self.y + self.size[1])

    def up_animation_display(self, window) -> None :
        position : tuple[int] = None
        if self.is_clicked :
            position = self.position
            self.content.set_position((self.x + 5, self.y + 5))
            self.__surface.fill(self.__colors["clicked"])
        elif self.is_visited : 
            self.__surface.fill(self.__colors["default"])
            self.content.set_position((self.x + 5, self.y - 5))
            position = (self.x, self.y - 10)
            visited_rect = Pg.Surface(self.size)
            visited_rect.fill(self.__colors["visited"])
            window.screen.blit(visited_rect, self.position)
        else : 
            self.__surface.fill(self.__colors["default"])
            self.content.set_position((self.x + 5, self.y + 5))
            position = self.position
        window.screen.blit(self.__surface, position)

    def down_animation_display(self, window) -> None :
        ...

    def no_animation_display(self, window) -> None :
        ...

    def reset(self) -> None:
        self.set_visited(False)
        self.set_clicked(False)

    def display(self, window) -> None:
        match self.button_type :
            case dt.ButtonType.NO_ANIMATION : self.no_animation_display(window)
            case dt.ButtonType.UP_ANIMATION : self.up_animation_display(window)
            case dt.ButtonType.DOWN_ANIMATION : self.down_animation_display(window)
        if isinstance(self.content, wdgt.Widget) :
            self.content.display(window)

    def __str__(self) -> str :
        popup_str : str = "button :\n"
        popup_str += str(self.content)
        return popup_str