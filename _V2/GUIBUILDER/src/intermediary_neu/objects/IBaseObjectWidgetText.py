from typing import Optional
from .IBaseObjectWidget import IBaseObjectWidget


class IBaseObjectWidgetText(IBaseObjectWidget):
    ATTRIBUTES = IBaseObjectWidget.ATTRIBUTES.copy()
    ATTRIBUTES.update({"text": str, "text_color": tuple[int, int, int]})
    
    def __init__(self, id: int, name: Optional[str], pos: tuple[int, int], size: tuple[int, int], text: str = "Button", text_color: tuple[int, int, int] = (0x00, 0x00, 0x00)) -> None:
        super().__init__(id, name, pos, size)
        self.text: str = text
        self.text_color: tuple[int, int, int] = text_color