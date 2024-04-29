from typing import Optional
from .BaseObject import BaseObject


class Timer(BaseObject):
    def __init__(self, id: int, name: Optional[str] = None, pos: tuple[int, int] = (0, 0), size: tuple[int, int] = (75, 18), background_color: tuple[int, int, int] = (0xFF, 0xFF, 0xFF), event_hovered: bool = False) -> None:
        super().__init__(id)
        if name == None:
            name = f"{id}_canvas"
        self.name = name
        self.pos: tuple[int, int] = pos
        self.size: tuple[int, int] = size
        self.background_color: tuple[int, int, int] = background_color
        self.event_hovered: bool = event_hovered