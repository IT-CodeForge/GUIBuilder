from enum import auto
from typing import Any

from .Internal.ETKUtils import gen_col_from_int

from .vector2d import vector2d
from .Internal.ETKBaseObject import ETKEvents
from .Internal.ETKBaseTkWidgetDisableable import ETKBaseTkWidgetDisableable
from .Internal.ETKBaseTkWidgetText import ETKBaseTkWidgetText
from .Internal.ETKBaseTkObject import ETKBaseEvents  # type:ignore
from tkinter import Checkbutton, IntVar, Tk


class ETKCheckboxEvents(ETKEvents):
    CHECKED = ("<Custom>", auto())
    UNCHECKED = ("<Custom>", auto())
    TOGGLED = ("<Custom>", auto())


class ETKCheckbox(ETKBaseTkWidgetDisableable, ETKBaseTkWidgetText):
    def __init__(self, tk: Tk, text: str = "Checkbox", pos: vector2d = vector2d(0, 0), size: vector2d = vector2d(70, 18), state: bool = False, background_color: int = 0xEEEEEE, text_color: int = 0x0, **kwargs: Any) -> None:
        self.__state = IntVar()
        self.__ignore_next_change_event: bool = False
        self._tk_object: Checkbutton = Checkbutton(  # type:ignore
            tk, variable=self.__state)
        super().__init__(text=text, pos=pos, size=size, background_color=background_color, text_color=text_color, **kwargs)
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

    @ETKBaseTkWidgetText.text_color.setter
    def text_color(self, value: int) -> None:
        ETKBaseTkWidgetText.text_color.fset(self, value)  # type:ignore
        self._tk_object.configure(disabledforeground=gen_col_from_int(value))  # type:ignore

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
