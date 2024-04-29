from enum import auto
from tkinter import Event, Tk, EventType

from .Internal.ETKBaseObject import ETKEvents
from .vector2d import vector2d
from .ETKLabel import ETKLabel
from .Internal.ETKBaseTkWidgetDisableable import ETKBaseTkWidgetDisableable
from .Internal.ETKBaseTkObject import ETKBaseEvents  # type:ignore


class ETKEditEvents(ETKEvents):
    CHANGED = ("<KeyPress>", auto())


class ETKEdit(ETKBaseTkWidgetDisableable, ETKLabel):
    def __init__(self, tk: Tk, text: str = "", pos: vector2d = vector2d(0, 0), size: vector2d = vector2d(80, 17), background_color: int = 0xEEEEEE, text_color: int = 0) -> None:
        ETKLabel.__init__(self, tk, text, pos, size,
                          background_color, text_color)
        self._tk_object["state"] = "normal"
        ETKBaseTkWidgetDisableable.__init__(self, pos, size, background_color)
        self._event_lib.update({e: [] for e in ETKEditEvents})

    #region Properties
        
    @ETKBaseTkWidgetDisableable.enabled.setter
    def enabled(self, value: bool) -> None:
        ETKBaseTkWidgetDisableable.enabled.fset(self, value) #type:ignore
        if value:
            self._send_button_event_break = False
            self._tk_object.configure(cursor="xterm")
        else:
            self._send_button_event_break = True
            self._tk_object.configure(cursor="")

    #endregion
    # region Methods

    def _handle_tk_event(self, event: Event) -> None|str:  # type:ignore
        match event.type:
            case EventType.KeyPress:
                if self.abs_enabled:
                    self._handle_event(ETKEditEvents.CHANGED,
                                       [event])  # type:ignore
                    return
            case _:
                pass
        return ETKLabel._handle_tk_event(  # type:ignore
            self, event)

    # endregion
