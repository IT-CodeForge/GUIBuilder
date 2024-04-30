from typing import Optional
from .IBaseObjectWidget import IBaseObjectWidget


class ITimer(IBaseObjectWidget):
    ATTRIBUTES = IBaseObjectWidget.ATTRIBUTES.copy()
    ATTRIBUTES.update({"interval": int, "enabled": bool})

    def __init__(self, id: int, name: Optional[str] = None, pos: tuple[int, int] = (0, 0), size: tuple[int, int] = (50, 18), interval: int = 1000, enabled: bool = True) -> None:
        super().__init__(id, name, pos, size)
        self.interval: int = interval
        self.enabled: bool = enabled