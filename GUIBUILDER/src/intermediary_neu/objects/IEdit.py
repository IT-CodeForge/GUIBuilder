from typing import Any, Optional
from.IBaseObjectWidgetVisibleEVChanged import IBaseObjectWidgetVisibleEVChanged
from .IBaseObjectWidgetText import IBaseObjectWidgetText


class IEdit(IBaseObjectWidgetVisibleEVChanged, IBaseObjectWidgetText):
    ATTRIBUTES = IBaseObjectWidgetVisibleEVChanged.ATTRIBUTES.copy()
    ATTRIBUTES.update(IBaseObjectWidgetText.ATTRIBUTES)
    ATTRIBUTES.update({"multiple_lines": bool})

    def __init__(self, id: int, name: Optional[str] = None, text: str = "Edit", pos: tuple[int, int] = (0, 0), size: tuple[int, int] = (200, 100), text_color: tuple[int, int, int] = (0x00, 0x00, 0x00), background_color: tuple[int, int, int] = (0xEE, 0xEE, 0xEE), multiple_lines: bool = True, event_changed: bool = False, event_hovered: bool = False, **kwargs: Any) -> None:
        if name is None:
            name = f"{id}_edit"
        super().__init__(id=id, name=name, pos=pos, size=size, text=text, text_color=text_color, background_color=background_color, event_hovered=event_hovered, event_changed=event_changed, **kwargs)
        self.multiple_lines: bool = multiple_lines