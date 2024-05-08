from typing import Any, Optional
from .IBaseObjectWidget import IBaseObjectWidget


class ITimer(IBaseObjectWidget):
    ATTRIBUTES = IBaseObjectWidget.ATTRIBUTES.copy()
    ATTRIBUTES.update({"interval": int, "enabled": bool})

    def __init__(self, id: int, name: Optional[str] = None, pos: tuple[int, int] = (0, 0), size: tuple[int, int] = (50, 18), interval: int = 1000, enabled: bool = True, **kwargs: Any) -> None:
        if name == None:
            name = f"{id}_timer"
        super().__init__(id=id, name=name, pos=pos, size=size, **kwargs)
        self.interval: int = interval
        self.enabled: bool = enabled