from typing import Any
from .IBaseObjectWidget import IBaseObjectWidget


class IBaseObjectWidgetText(IBaseObjectWidget):
    ATTRIBUTES = IBaseObjectWidget.ATTRIBUTES.copy()
    ATTRIBUTES.update({"text": str, "text_color": tuple[int, int, int]})
    
    def __init__(self, *, id: int, name: str, pos: tuple[int, int], size: tuple[int, int], text: str, text_color: tuple[int, int, int], **kwargs: Any) -> None:
        super().__init__(id=id, name=name, pos=pos, size=size, **kwargs)
        self.text: str = text
        self.text_color: tuple[int, int, int] = text_color