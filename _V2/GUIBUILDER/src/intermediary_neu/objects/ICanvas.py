from typing import Optional
from .IBaseObjectWidgetVisible import IBaseObjectWidgetVisible


class ICanvas(IBaseObjectWidgetVisible):
    ATTRIBUTES = IBaseObjectWidgetVisible.ATTRIBUTES.copy()
    ATTRIBUTES.update({})

    def __init__(self, id: int, name: Optional[str] = None, pos: tuple[int, int] = (0, 0), size: tuple[int, int] = (100, 100), background_color: tuple[int, int, int] = (0xFF, 0xFF, 0xFF), event_hovered: bool = False) -> None:
        if name == None:
            name = f"{id}_canvas"
        IBaseObjectWidgetVisible.__init__(self, id, name, pos, size, background_color, event_hovered)