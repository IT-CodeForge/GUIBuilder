from typing import Any, Optional

from .IBaseObjectWidgetVisible import IBaseObjectWidgetVisible
from .IBaseObjectWidgetText import IBaseObjectWidgetText


class ILabel(IBaseObjectWidgetVisible, IBaseObjectWidgetText):
    ATTRIBUTES = IBaseObjectWidgetVisible.ATTRIBUTES.copy()
    ATTRIBUTES.update(IBaseObjectWidgetText.ATTRIBUTES)
    ATTRIBUTES.update({})

    def __init__(self, id: int, name: Optional[str] = None, text: str = "Label", pos: tuple[int, int] = (0, 0), size: tuple[int, int] = (75, 18), text_color: tuple[int, int, int] = (0x00, 0x00, 0x00), background_color: tuple[int, int, int] = (0xEE, 0xEE, 0xEE), event_hovered: bool = False, **kwargs: Any) -> None:
        if name == None:
            name = f"{id}_label"
        super().__init__(id=id, name=name, pos=pos, size=size, text=text, text_color=text_color, background_color=background_color, event_hovered=event_hovered, **kwargs)