from typing import Any
from .IBaseObjectWidgetVisible import IBaseObjectWidgetVisible


class IBaseObjectWidgetVisibleEVChanged(IBaseObjectWidgetVisible):
    ATTRIBUTES = IBaseObjectWidgetVisible.ATTRIBUTES.copy()
    ATTRIBUTES.update({"event_changed": bool})
    
    def __init__(self, *, id: int, name: str, pos: tuple[int, int], size: tuple[int, int], background_color: tuple[int, int, int], event_hovered: bool, event_changed: bool, **kwargs: Any) -> None:
        super().__init__(id=id, name=name, pos=pos, size=size, background_color=background_color, event_hovered=event_hovered, **kwargs)
        self.event_changed = event_changed