from tkinter import END, Event, EventType, Text, Tk
from typing import Any
from .vector2d import vector2d
from .Internal.ETKBaseTkWidgetText import ETKBaseTkWidgetText
from .Internal.ETKBaseTkObject import ETKBaseEvents  # type:ignore


class ETKLabel(ETKBaseTkWidgetText):
    def __init__(self, tk: Tk, pos: vector2d = vector2d(0, 0), size: vector2d = vector2d(80, 17), text: str = "Label", *, visibility: bool = True, background_color: int = 0xEEEEEE, text_color: int = 0, outline_color: int = 0x0, outline_thickness: int = 0, **kwargs: Any) -> None:
        self._tk_object: Text = Text(tk)  # type:ignore
        self._send_button_event_break = True

        super().__init__(pos=pos, size=size, text=text, visibility=visibility, background_color=background_color, text_color=text_color, outline_color=outline_color, outline_thickness=outline_thickness, **kwargs)

        self._tk_object["state"] = "disabled"
        self.add_event(ETKBaseEvents.MOUSE_DOWN, lambda: None)
        self._tk_object.configure(cursor="")

    # region Properties

    @property
    def text(self) -> str:
        return self._tk_object.get("1.0", 'end-1c')

    @text.setter
    def text(self, value: str) -> None:
        state = self._tk_object["state"]
        self._tk_object["state"] = "normal"
        self._tk_object.delete(1.0, END)
        self._tk_object.insert(1.0, value)
        self._tk_object["state"] = state

    def _handle_tk_event(self, event: Event) -> str | None:  # type:ignore
        super()._handle_tk_event(event)  # type:ignore
        match event.type:
            case EventType.ButtonPress:
                if self._send_button_event_break:
                    return "break"
            case _:
                pass

    # endregion
