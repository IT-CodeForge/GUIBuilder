from .IBaseObjectWidget import IBaseObjectWidget


class IBaseObjectWidgetVisible(IBaseObjectWidget):
    ATTRIBUTES = IBaseObjectWidget.ATTRIBUTES.copy()
    ATTRIBUTES.update({"event_hovered": bool, "background_color": tuple[int, int, int]})
    
    def __init__(self, id: int, name: str, pos: tuple[int, int], size: tuple[int, int], background_color: tuple[int, int, int], event_hovered: bool) -> None:
        IBaseObjectWidget.__init__(self, id, name, pos, size)
        if IBaseObjectWidgetVisible in getattr(self, "_initialized", []):
            return
        self._initialized.append(IBaseObjectWidgetVisible)
        self.event_hovered: bool = event_hovered
        self.background_color: tuple[int, int, int] = background_color