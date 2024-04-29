from typing import Optional
from .BaseObject import BaseObject


class Timer(BaseObject):
    def __init__(self, id: int, name: Optional[str] = None, pos: tuple[int, int] = (0, 0), size: tuple[int, int] = (75, 18), interval: int = 1000, enabled: bool = True) -> None:
        super().__init__(id)
        if name == None:
            name = f"{id}_timer"
        self.name = name
        self.pos: tuple[int, int] = pos
        self.size: tuple[int, int] = size
        self.interval: int = interval
        self.enabled: bool = enabled