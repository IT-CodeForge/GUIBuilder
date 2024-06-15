from typing import Any, Optional
from .IBaseObjectWidgetVisible import IBaseObjectWidgetVisible


class ICanvas(IBaseObjectWidgetVisible):
    ATTRIBUTES = IBaseObjectWidgetVisible.ATTRIBUTES.copy()
    ATTRIBUTES.update({})

    def __init__(self, id: int, name: Optional[str] = None, pos: tuple[int, int] = (0, 0), size: tuple[int, int] = (100, 100), background_color: tuple[int, int, int] = (0xFF, 0xFF, 0xFF), event_hovered: bool = False, **kwargs: Any) -> None:
        if name is None:
            name = f"{id}_canvas"
        super().__init__(id=id, name=name, pos=pos, size=size, background_color=background_color, event_hovered=event_hovered, **kwargs)