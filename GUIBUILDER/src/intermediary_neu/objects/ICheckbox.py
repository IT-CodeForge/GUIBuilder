from typing import Any, Optional
from .IBaseObjectWidgetText import IBaseObjectWidgetText
from.IBaseObjectWidgetVisibleEVChanged import IBaseObjectWidgetVisibleEVChanged


class ICheckbox(IBaseObjectWidgetVisibleEVChanged, IBaseObjectWidgetText):
    ATTRIBUTES = IBaseObjectWidgetVisibleEVChanged.ATTRIBUTES.copy()
    ATTRIBUTES.update(IBaseObjectWidgetText.ATTRIBUTES)
    ATTRIBUTES.update({"checked": bool})

    def __init__(self, id: int, name: Optional[str] = None, text: str = "Checkbox", pos: tuple[int, int] = (0, 0), size: tuple[int, int] = (100, 25), text_color: tuple[int, int, int] = (0x00, 0x00, 0x00), background_color: tuple[int, int, int] = (0xEE, 0xEE, 0xEE), checked: bool = False, event_changed: bool = True, event_hovered: bool = False, **kwargs: Any) -> None:
        if name is None:
            name = f"{id}_checkbox"
        super().__init__(id=id, name=name, pos=pos, size=size, text=text, text_color=text_color, background_color=background_color, event_hovered=event_hovered, event_changed=event_changed, **kwargs)
        self.checked: bool = checked