from typing import Optional
from .BaseObject import BaseObject


class Edit(BaseObject):
    def __init__(self, id: int, name: Optional[str] = None, text: str = "Edit", pos: tuple[int, int] = (0, 0), size: tuple[int, int] = (75, 18), text_color: tuple[int, int, int] = (0x00, 0x00, 0x00), background_color: tuple[int, int, int] = (0xEE, 0xEE, 0xEE), multiple_lines: bool = True, event_changed: bool = False, event_hovered: bool = False) -> None:
        super().__init__(id)
        if name == None:
            name = f"{id}_edit"
        self.name = name
        self.text = text
        self.pos: tuple[int, int] = pos
        self.size: tuple[int, int] = size
        self.text_color: tuple[int, int, int] = text_color
        self.background_color: tuple[int, int, int] = background_color
        self.multiple_lines: bool = multiple_lines
        self.event_changed: bool = event_changed
        self.event_hovered: bool = event_hovered
