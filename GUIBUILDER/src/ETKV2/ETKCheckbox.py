from enum import auto
from typing import Any

from .Vector2d import Vector2d
from .Internal.ETKBaseObject import ETKEvents
from .Internal.ETKBaseTkWidgetButton import ETKBaseTkWidgetButton
from .Internal.ETKBaseTkObject import ETKBaseEvents  # type:ignore
from tkinter import Checkbutton, IntVar, Tk


class ETKCheckboxEvents(ETKEvents):
    CHECKED = ("<Custom>", auto())
    UNCHECKED = ("<Custom>", auto())
    TOGGLED = ("<Custom>", auto())


class ETKCheckbox(ETKBaseTkWidgetButton):
    def __init__(self, tk: Tk, pos: Vector2d = Vector2d(0, 0), size: Vector2d = Vector2d(70, 18), text: str = "Checkbox", state: bool = False, *, visibility: bool = True, enabled: bool = True, background_color: int = 0xEEEEEE, text_color: int = 0x0, outline_color: int = 0x0, outline_thickness: int = 0, **kwargs: Any) -> None:
        self.__state = IntVar()
        self.__ignore_next_change_event: bool = False
        self._create_outline(tk)
        self._tk_object: Checkbutton = Checkbutton(  # type:ignore
            self._outline, variable=self.__state)
        super().__init__(pos=pos, size=size, text=text, visibility=visibility, enabled=enabled, background_color=background_color, text_color=text_color, outline_color=outline_color, outline_thickness=outline_thickness, **kwargs)
        self._event_lib.update({e: [] for e in ETKCheckboxEvents})
        self.__state.trace_add("write", self.__checkbox_event_handler)
        self.state = state

    # region Properties

    @property
    def state(self) -> bool:
        return bool(self.__state.get())

    @state.setter
    def state(self, value: bool) -> None:
        self.__ignore_next_change_event = True
        self.__state.set(value)

    # endregion
    # region Methods

    def __checkbox_event_handler(self, *args: str) -> None:
        if self.__ignore_next_change_event:
            self.__ignore_next_change_event = False
            return
        self._handle_event(ETKCheckboxEvents.TOGGLED)
        if self.state:
            self._handle_event(ETKCheckboxEvents.CHECKED)
        else:
            self._handle_event(ETKCheckboxEvents.UNCHECKED)

    # endregion
