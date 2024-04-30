from typing import Optional
from .IBaseObjectWidgetVisible import IBaseObjectWidgetVisible


class IBaseObjectWidgetVisibleEVChanged(IBaseObjectWidgetVisible):
    ATTRIBUTES = IBaseObjectWidgetVisible.ATTRIBUTES.copy()
    ATTRIBUTES.update({"event_changed": bool})
    
    def __init__(self, id: int, name: Optional[str], pos: tuple[int, int], size: tuple[int, int], background_color: tuple[int, int, int], event_hovered: bool, event_changed: bool) -> None:
        super().__init__(id, name, pos, size, background_color, event_hovered)
        self.event_changed = event_changed