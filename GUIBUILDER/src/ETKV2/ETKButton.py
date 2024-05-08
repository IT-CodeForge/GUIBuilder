from enum import auto
from typing import Any

from .Internal.ETKUtils import gen_col_from_int
from .Internal.ETKBaseObject import ETKEvents
from .Internal.ETKBaseTkWidgetDisableable import ETKBaseTkWidgetDisableable
from .Internal.ETKBaseTkWidgetText import ETKBaseTkWidgetText
from .Internal.ETKBaseTkObject import ETKBaseEvents  # type:ignore
from .vector2d import vector2d
from tkinter import Button, Event, Tk, EventType


class ETKButtonEvents(ETKEvents):
    PRESSED = ("<ButtonPress>", auto())
    RELEASED = ("<ButtonRelease>", auto())


class ETKButton(ETKBaseTkWidgetDisableable, ETKBaseTkWidgetText):
    def __init__(self, tk: Tk, text: str = "Button", pos: vector2d = vector2d(0, 0), size: vector2d = vector2d(70, 18), background_color: int = 0xEEEEEE, text_color: int = 0x0, **kwargs: Any) -> None:
        self._tk_object: Button = Button(tk)  # type:ignore
        super().__init__(text=text, pos=pos, size=size, background_color=background_color, text_color=text_color, **kwargs)
        self._event_lib.update({e: [] for e in ETKButtonEvents})

    # region Properties

    @ETKBaseTkWidgetText.text_color.setter
    def text_color(self, value: int) -> None:
        ETKBaseTkWidgetText.text_color.fset(self, value)  # type:ignore
        self._tk_object.configure(disabledforeground=gen_col_from_int(value))  # type:ignore

    # endregion
    # region Methods

    def _handle_tk_event(self, event: Event) -> None:  # type:ignore
        match event.type:
            case EventType.ButtonPress:
                if self.abs_enabled:
                    self._handle_event(
                        ETKButtonEvents.PRESSED, [event])  # type:ignore
            case EventType.ButtonRelease:
                if self.abs_enabled:
                    self._handle_event(
                        ETKButtonEvents.RELEASED, [event])  # type:ignore
            case _:
                pass
        return super()._handle_tk_event(event)  # type:ignore

    # endregion
