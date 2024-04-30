from .IBaseObjectWidget import IBaseObjectWidget


class IBaseObjectWidgetText(IBaseObjectWidget):
    ATTRIBUTES = IBaseObjectWidget.ATTRIBUTES.copy()
    ATTRIBUTES.update({"text": str, "text_color": tuple[int, int, int]})
    
    def __init__(self, id: int, name: str, pos: tuple[int, int], size: tuple[int, int], text: str, text_color: tuple[int, int, int]) -> None:
        IBaseObjectWidget.__init__(self, id, name, pos, size)
        if IBaseObjectWidgetText in getattr(self, "_initialized", []):
            return
        self._initialized.append(IBaseObjectWidgetText)
        self.text: str = text
        self.text_color: tuple[int, int, int] = text_color