import pygame as Pg
import Data as Dt
import views.Widget as Wdgt

class Button(Wdgt.Widget) :
    """"""

    def __init__(self, position: Dt.Point, size : Dt.Point, content : Wdgt.Widget = None, button_type : int = Dt.ButtonType.NO_ANIMATION, 
    color : Pg.Color = Dt.Colors.BEIGE, visited_color : Pg.Color = Dt.Colors.BROWN, clicked_color : Pg.Color = Dt.Colors.BROWN) :
        """"""
        super().__init__(position, "button")
        self.__size : Dt.Point = size
        self.__content : Wdgt.Widget = content
        self.__visited : bool = False
        self.__clicked : bool = False
        self.__type : int = button_type
        self.__surface : Pg.Surface = Pg.Surface((size.x, size.y))
        self.__colors : dict[str : Pg.Color] = {"default" : color, "visited" : visited_color, "clicked" : clicked_color}
        self.__surface.fill(self.__colors["default"])

    @property
    def size(self) -> Dt.Point :
        return self.__size

    @property
    def content(self) -> Wdgt.Widget :
        return self.__content

    @property
    def is_visited(self) -> bool :
        return self.__visited

    @property
    def is_clicked(self) -> bool :
        return self.__clicked

    @property
    def button_type(self) -> int : 
        return self.__type

    def set_clicked(self, value : bool) -> None :
        self.__clicked = value

    def set_visited(self, value : bool) -> None :
        self.__visited = value

    def __contains__(self, coords : Dt.Point | tuple[int]) -> bool : 
        if not isinstance(coords, Dt.Point) :
            coords : Dt.Point = Dt.Point(coords[0], coords[1])
        return  (self.position.x <= coords.x <= self.position.x + self.size.x and
            self.position.y <= coords.y <= self.position.y + self.size.y)

    def up_animation_display(self, window) -> None :
        position : tuple[int] = None
        if self.is_clicked :
            position = (self.position.x, self.position.y)
            self.content.set_position(Dt.Point(self.position.x + 5, self.position.y + 5))
            self.__surface.fill(self.__colors["clicked"])
        elif self.is_visited : 
            self.__surface.fill(self.__colors["default"])
            self.content.set_position(Dt.Point(self.position.x + 5, self.position.y - 5))
            position = (self.position.x, self.position.y - 10)
            visited_rect = Pg.Surface((self.size.x, self.size.y))
            visited_rect.fill(self.__colors["visited"])
            window.screen.blit(visited_rect, (self.position.x, self.position.y))
        else : 
            self.__surface.fill(self.__colors["default"])
            self.content.set_position(Dt.Point(self.position.x + 5, self.position.y + 5))
            position = (self.position.x, self.position.y)
        window.screen.blit(self.__surface, position)

    def down_animation_display(self, window) -> None :
        ...

    def no_animation_display(self, window) -> None :
        ...

    def display(self, window) -> None:
        match self.button_type :
            case Dt.ButtonType.NO_ANIMATION : self.no_animation_display(window)
            case Dt.ButtonType.UP_ANIMATION : self.up_animation_display(window)
            case Dt.ButtonType.DOWN_ANIMATION : self.down_animation_display(window)
        if isinstance(self.content, Wdgt.Widget) :
            self.content.display(window)

    def __str__(self) -> str :
        popup_str : str = "button :\n"
        popup_str += str(self.content)
        return popup_str