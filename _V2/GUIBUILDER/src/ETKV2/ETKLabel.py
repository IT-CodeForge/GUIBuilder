from tkinter import END, Event, EventType, Text, Tk
from .vector2d import vector2d
from .Internal.ETKBaseTkWidgetText import ETKBaseTkWidgetText
from .Internal.ETKBaseTkObject import ETKBaseEvents  # type:ignore


class ETKLabel(ETKBaseTkWidgetText):
    def __init__(self, tk: Tk, text: str = "", pos: vector2d = vector2d(0, 0), size: vector2d = vector2d(80, 17), background_color: int = 0xEEEEEE, text_color: int = 0) -> None:
        self._tk_object: Text = Text(tk)  # type:ignore
        ETKBaseTkWidgetText.__init__(
            self, text, pos, size, background_color, text_color)
        self._tk_object["state"] = "disabled"
        self._send_button_event_break = True
        self.add_event(ETKBaseEvents.MOUSE_DOWN, lambda: None)

    # region Properties

    @property
    def text(self) -> str:
        return self._tk_object.get("1.0", 'end-1c')

    @text.setter
    def text(self, value: str) -> None:
        self._tk_object.delete(1.0, END)
        self._tk_object.insert(1.0, value)
    

    def _handle_tk_event(self, event: Event) -> str|None:  # type:ignore
        ETKBaseTkWidgetText._handle_tk_event(self, event)  # type:ignore
        match event.type:
            case EventType.ButtonPress:
                if self._send_button_event_break:
                    return "break"
            case _:
                pass

    # endregion
