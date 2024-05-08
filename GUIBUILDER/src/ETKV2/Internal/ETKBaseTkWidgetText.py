from typing import Any
from ..vector2d import vector2d
from .ETKBaseTkWidget import ETKBaseTkWidget
from .ETKUtils import gen_col_from_int
from .ETKBaseTkObject import ETKBaseEvents  # type:ignore


class ETKBaseTkWidgetText(ETKBaseTkWidget):
    def __init__(self, text: str, pos: vector2d, size: vector2d, background_color: int, text_color: int, **kwargs: Any) -> None:
        super().__init__(pos=pos, size=size, background_color=background_color, **kwargs)

        self.text_color = text_color
        self.text = text

    # region Properties

    @property
    def text(self) -> str:
        return self._tk_object.cget("text")

    @text.setter
    def text(self, value: str) -> None:
        self._tk_object.config(text=value)  # type:ignore

    @property
    def text_color(self) -> int:
        return int(self._tk_object["fg"][1:], 16)

    @text_color.setter
    def text_color(self, value: int) -> None:
        self._tk_object.configure(fg=gen_col_from_int(value))  # type:ignore

    # endregion
