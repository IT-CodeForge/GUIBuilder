from ..vector2d import vector2d
from .ETKBaseTkWidget import ETKBaseTkWidget
from .ETKBaseWidgetDisableable import ETKBaseWidgetDisableable
from .ETKBaseTkObject import ETKBaseEvents  # type:ignore


class ETKBaseTkWidgetDisableable(ETKBaseWidgetDisableable, ETKBaseTkWidget):
    def __init__(self, pos: vector2d, size: vector2d, background_color: int) -> None:
        ETKBaseTkWidget.__init__(self, pos, size, background_color)
        ETKBaseWidgetDisableable.__init__(self, pos, size, background_color)

    # region Methods
    # region update event methods

    def _update_enabled(self) -> None:
        if self.abs_enabled:
            self._tk_object["state"] = "normal"
        else:
            self._tk_object["state"] = "disabled"

    # endregion
    # endregion
