from enum import auto
from tkinter import Event, Tk, EventType

from .Internal.ETKBaseObject import ETKEvents
from .vector2d import vector2d
from .ETKLabel import ETKLabel
from .Internal.ETKBaseTkWidgetDisableable import ETKBaseTkWidgetDisableable
from .Internal.ETKBaseTkObject import ETKBaseEvents  # type:ignore


class ETKEditEvents(ETKEvents):
    CHANGED = ("<KeyRelease>", auto())
    CHANGED_DELAYED = ("<KeyRelease>", auto())


class ETKEdit(ETKBaseTkWidgetDisableable, ETKLabel):
    def __init__(self, tk: Tk, text: str = "Edit", pos: vector2d = vector2d(0, 0), size: vector2d = vector2d(80, 17), background_color: int = 0xEEEEEE, text_color: int = 0) -> None:
        self.__old_text: str = ""
        self.__delay_cycles: int = -1
        ETKLabel.__init__(self, tk, text, pos, size,
                          background_color, text_color)
        self._tk_object["state"] = "normal"
        ETKBaseTkWidgetDisableable.__init__(self, pos, size, background_color)
        self._event_lib.update({e: [] for e in ETKEditEvents})

    # region Properties

    @ETKBaseTkWidgetDisableable.enabled.setter
    def enabled(self, value: bool) -> None:
        ETKBaseTkWidgetDisableable.enabled.fset(self, value)  # type:ignore
        if value:
            self._send_button_event_break = False
            self._tk_object.configure(cursor="xterm")
        else:
            self._send_button_event_break = True
            self._tk_object.configure(cursor="")

    @ETKLabel.text.setter
    def text(self, value: str) -> None:
        ETKLabel.text.fset(self, value)  # type:ignore
        self.__old_text = value

    # endregion
    # region Methods

    def __send_delayed_changed_event(self, event: Event) -> None:  # type:ignore
        if self.__delay_cycles == 0:
            self._handle_event(ETKEditEvents.CHANGED_DELAYED,
                               [event])  # type:ignore
        self.__delay_cycles -= 1

    def _handle_tk_event(self, event: Event) -> None | str:  # type:ignore
        match event.type:
            case EventType.KeyRelease:
                if self.abs_enabled and self.text != self.__old_text:
                    self.__delay_cycles += 1
                    self._handle_event(ETKEditEvents.CHANGED,
                                       [event])  # type:ignore
                    self._tk_object.after(1000, self.__send_delayed_changed_event, event)  # type:ignore
                    self.__old_text = self.text
                return
            case _:
                pass
        return ETKLabel._handle_tk_event(  # type:ignore
            self, event)

    # endregion
