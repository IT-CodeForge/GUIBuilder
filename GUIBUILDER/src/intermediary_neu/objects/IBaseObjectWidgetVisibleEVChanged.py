from .IBaseObjectWidgetVisible import IBaseObjectWidgetVisible


class IBaseObjectWidgetVisibleEVChanged(IBaseObjectWidgetVisible):
    ATTRIBUTES = IBaseObjectWidgetVisible.ATTRIBUTES.copy()
    ATTRIBUTES.update({"event_changed": bool})
    
    def __init__(self, id: int, name: str, pos: tuple[int, int], size: tuple[int, int], background_color: tuple[int, int, int], event_hovered: bool, event_changed: bool) -> None:
        IBaseObjectWidgetVisible.__init__(self, id, name, pos, size, background_color, event_hovered)
        if IBaseObjectWidgetVisibleEVChanged in getattr(self, "_initialized", []):
            return
        self._initialized.append(IBaseObjectWidgetVisibleEVChanged)
        self.event_changed = event_changed