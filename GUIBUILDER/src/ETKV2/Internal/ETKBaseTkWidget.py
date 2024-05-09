from tkinter import Widget as tk_widget
from typing import Any

from .ETKUtils import gen_col_from_int

from ..vector2d import vector2d
from .ETKBaseWidget import ETKBaseWidget
from .ETKBaseTkObject import ETKBaseTkObject


class ETKBaseTkWidget(ETKBaseTkObject, ETKBaseWidget):

    def __init__(self, *, pos: vector2d, size: vector2d, background_color: int, **kwargs: Any) -> None:
        self._tk_object: tk_widget
        self._outline_color: str = ""
        self._outline_thickness: int = 0

        super().__init__(pos=pos, size=size, background_color=background_color, **kwargs)

        self._place_object()
        self.outline_thickness = 0
        self.outline_color = 0

    # region Properties

    @ETKBaseWidget.size.setter
    def size(self, value: vector2d) -> None:
        ETKBaseWidget.size.fset(self, value)  # type:ignore
        self._place_object()

    @property
    def outline_color(self) -> int:
        return int(self._outline_color[1:], 16)

    @outline_color.setter
    def outline_color(self, value: int) -> None:
        col = gen_col_from_int(value)
        self._outline_color = col
        self._tk_object.configure(highlightbackground=col)  # type:ignore

    @property
    def outline_thickness(self) -> int:
        return self._outline_thickness

    @outline_thickness.setter
    def outline_thickness(self, value: int) -> None:
        self._outline_thickness = value
        self._tk_object.configure(highlightthickness=value)  # type:ignore

    # endregion
    # region Methods

    def _place_object(self) -> None:
        pos = self.abs_pos
        self._tk_object.place(
            x=pos.x, y=pos.y, width=self.size.x, height=self.size.y)

        # region update event methods

    def _update_pos(self) -> None:
        if self.abs_visibility:
            self._place_object()
        else:
            self._tk_object.place_forget()
            self._tk_object.update()

    def _update_visibility(self) -> None:
        if self.abs_visibility:
            self._place_object()
        else:
            self._tk_object.place_forget()
            self._tk_object.update()
    # endregion
    # endregion
