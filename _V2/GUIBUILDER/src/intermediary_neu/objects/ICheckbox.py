from typing import Optional
from .IBaseObjectWidgetText import IBaseObjectWidgetText
from.IBaseObjectWidgetVisibleEVChanged import IBaseObjectWidgetVisibleEVChanged


class ICheckbox(IBaseObjectWidgetVisibleEVChanged, IBaseObjectWidgetText):
    ATTRIBUTES = IBaseObjectWidgetVisibleEVChanged.ATTRIBUTES.copy()
    ATTRIBUTES.update(IBaseObjectWidgetText.ATTRIBUTES)
    ATTRIBUTES.update({"checked": bool})

    def __init__(self, id: int, name: Optional[str] = None, text: str = "Checkbox", pos: tuple[int, int] = (0, 0), size: tuple[int, int] = (100, 25), text_color: tuple[int, int, int] = (0x00, 0x00, 0x00), background_color: tuple[int, int, int] = (0xEE, 0xEE, 0xEE), checked: bool = False, event_changed: bool = True, event_hovered: bool = False) -> None:
        if name == None:
            name = f"{id}_checkbox"
        IBaseObjectWidgetVisibleEVChanged.__init__(self, id, name, pos, size, background_color, event_hovered, event_changed)
        IBaseObjectWidgetText.__init__(self, id, name, pos, size, text, text_color)
        self.checked: bool = checked