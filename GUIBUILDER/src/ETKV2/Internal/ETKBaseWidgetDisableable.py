from typing import Any
from ..vector2d import vector2d
from .ETKBaseWidget import ETKBaseWidget


class ETKBaseWidgetDisableable(ETKBaseWidget):
    def __init__(self, *, pos: vector2d, size: vector2d, background_color: int, **kwargs: Any) -> None:
        super().__init__(pos=pos, size=size, background_color=background_color, **kwargs)

        self.enabled = self._enabled

    # region Properties

    @ETKBaseWidget.enabled.setter
    def enabled(self, value: bool) -> None:
        """ """
        self._enabled = value
        self._update_enabled()

    # endregion
