from typing import Optional
from .BaseObject import BaseObject


class Button(BaseObject):
    def __init__(self, id: int, name: Optional[str] = None, text: str = "Button", pos: tuple[int, int] = (0, 0), size: tuple[int, int] = (75, 18), text_color: tuple[int, int, int] = (0x00, 0x00, 0x00), background_color: tuple[int, int, int] = (0xEE, 0xEE, 0xEE), event_pressed: bool = True, event_double_pressed: bool = False, event_hovered: bool = False) -> None:
        super().__init__(id)
        if name == None:
            name = f"{id}_button"
        self.name = name
        self.text = text
        self.pos: tuple[int, int] = pos
        self.size: tuple[int, int] = size
        self.text_color: tuple[int, int, int] = text_color
        self.background_color: tuple[int, int, int] = background_color
        self.event_pressed: bool = event_pressed
        self.event_double_pressed: bool = event_double_pressed
        self.event_hovered: bool = event_hovered
