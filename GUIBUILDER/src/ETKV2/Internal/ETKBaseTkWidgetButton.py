from tkinter import FLAT, LabelFrame, Tk
from typing import Any

from .ETKUtils import gen_col_from_int
from .ETKBaseTkWidgetDisableable import ETKBaseTkWidgetDisableable
from .ETKBaseTkWidgetText import ETKBaseTkWidgetText
from ..Vector2d import Vector2d


class ETKBaseTkWidgetButton(ETKBaseTkWidgetDisableable, ETKBaseTkWidgetText):
    def __init__(self, *, pos: Vector2d, size: Vector2d, text: str, visibility: bool, enabled: bool, background_color: int, text_color: int, outline_color: int, outline_thickness: int, **kwargs: Any) -> None:
        self._outline: LabelFrame

        super().__init__(text=text, pos=pos, size=size, visibility=visibility, enabled=enabled, background_color=background_color, text_color=text_color, outline_color=outline_color, outline_thickness=outline_thickness, **kwargs)

    # region Properties

    @ETKBaseTkWidgetText.text_color.setter
    def text_color(self, value: int) -> None:
        ETKBaseTkWidgetText.text_color.fset(self, value)  # type:ignore
        self._tk_object.configure(disabledforeground=gen_col_from_int(value))  # type:ignore

    @ETKBaseTkWidgetDisableable.outline_color.setter
    def outline_color(self, value: int) -> None:
        ETKBaseTkWidgetDisableable.outline_color.fset(self, value)  # type:ignore
        self._outline.configure(bg=self._outline_color)  # type:ignore

    @ETKBaseTkWidgetDisableable.outline_thickness.setter
    def outline_thickness(self, value: int) -> None:
        ETKBaseTkWidgetDisableable.outline_thickness.fset(self, value)  # type:ignore
        self._outline.configure(bd=value)  # type:ignore
        self._outline.pack(padx=value*2, pady=value*2)
        self._place_object()

    # endregion
    # region Methods

    def _create_outline(self, tk: Tk) -> None:
        self._outline = LabelFrame(tk, relief=FLAT)

    def _update_visibility(self) -> None:
        if self.abs_visibility:
            self._place_object()
        else:
            self._tk_object.place_forget()
            self._outline.place_forget()
            self._tk_object.update()
            self._outline.update()

    def _place_object(self) -> None:
        pos = self.abs_pos
        self._tk_object.place(x=0, y=0, width=self.size.x, height=self.size.y)
        self._outline.place(x=pos.x, y=pos.y, width=self.size.x+2*self.outline_thickness, height=self.size.y+2*self.outline_thickness)

    # endregion
