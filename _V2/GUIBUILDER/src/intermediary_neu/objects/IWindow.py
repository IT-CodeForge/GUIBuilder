from typing import Optional
from .IBaseObject import IBaseObject


class IWindow(IBaseObject):
    def __init__(self, id: int, name: Optional[str] = None, title: str = "Window-Title", pos: tuple[int, int] = (0, 0), size: tuple[int, int] = (500, 500), title_color: tuple[int, int, int] = (0x00, 0x00, 0x00), background_color: tuple[int, int, int] = (0xEE, 0xEE, 0xEE), event_create: bool = False, event_destroy: bool = False, event_paint: bool = False, event_resize: bool = False, event_mouse_click: bool = False, event_mouse_move: bool = False) -> None:
        super().__init__(id)
        if name == None:
            name = f"window"
        self.name = name
        self.title = title
        self.size: tuple[int, int] = size
        self.title_color: tuple[int, int, int] = title_color
        self.background_color: tuple[int, int, int] = background_color
        self.event_create: bool = event_create
        self.event_destroy: bool = event_destroy
        self.event_paint: bool = event_paint
        self.event_resize: bool = event_resize
        self.event_mouse_click: bool = event_mouse_click
        self.event_mouse_move: bool = event_mouse_move

    def __str__(self) -> str:
        return f'IEdit<id="{self.id}"; name="{self.name}"; title="{self.title}"; size="{self.size}"; title_color="{self.title_color}"; background_color="{self.background_color}"; event_create="{self.event_create}"; event_destroy="{self.event_destroy}"; event_paint="{self.event_paint}; event_resize="{self.event_resize}; event_mouse_click="{self.event_mouse_click}; event_mouse_move="{self.event_mouse_move}">'