from typing import Optional
from .IBaseObject import IBaseObject


class IWindow(IBaseObject):
    ATTRIBUTES = IBaseObject.ATTRIBUTES.copy()
    ATTRIBUTES.update({"title": str, "title_color": tuple[int, int, int], "background_color": tuple[int, int, int], "event_create": bool, "event_destroy": bool, "event_paint": bool, "event_resize": bool, "event_mouse_click": bool, "event_mouse_move": bool})
    
    def __init__(self, id: int, name: Optional[str] = None, title: str = "Window-Title", pos: tuple[int, int] = (0, 0), size: tuple[int, int] = (500, 500), title_color: tuple[int, int, int] = (0x00, 0x00, 0x00), background_color: tuple[int, int, int] = (0xEE, 0xEE, 0xEE), event_create: bool = False, event_destroy: bool = False, event_paint: bool = False, event_resize: bool = False, event_mouse_click: bool = False, event_mouse_move: bool = False) -> None:     
        super().__init__(id, name, size)
        self.title: str = title
        self.title_color: tuple[int, int, int] = title_color
        self.background_color: tuple[int, int, int] = background_color
        self.event_create: bool = event_create
        self.event_destroy: bool = event_destroy
        self.event_paint: bool = event_paint
        self.event_resize: bool = event_resize
        self.event_mouse_click: bool = event_mouse_click
        self.event_mouse_move: bool = event_mouse_move