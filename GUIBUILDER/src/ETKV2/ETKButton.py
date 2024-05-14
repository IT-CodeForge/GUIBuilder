from enum import auto
from typing import Any

from .Internal.ETKBaseObject import ETKEvents
from .Internal.ETKBaseTkWidgetButton import ETKBaseTkWidgetButton
from .Internal.ETKBaseTkObject import ETKBaseEvents  # type:ignore
from .Vector2d import Vector2d
from tkinter import FLAT, Button, Event, Tk, EventType


class ETKButtonEvents(ETKEvents):
    PRESSED = ("<ButtonPress>", auto())
    RELEASED = ("<ButtonRelease>", auto())


class ETKButton(ETKBaseTkWidgetButton):
    def __init__(self, tk: Tk, pos: Vector2d = Vector2d(0, 0), size: Vector2d = Vector2d(70, 18), text: str = "Button", *, visibility: bool = True, enabled: bool = True, background_color: int = 0xEEEEEE, text_color: int = 0x0, outline_color: int = 0x0, outline_thickness: int = 0, **kwargs: Any) -> None:
        super()._create_outline(tk)
        self._tk_object: Button = Button(self._outline, relief=FLAT)  # type:ignore
        super().__init__(pos=pos, size=size, text=text, visibility=visibility, enabled=enabled, background_color=background_color, text_color=text_color, outline_color=outline_color, outline_thickness=outline_thickness, **kwargs)
        self._event_lib.update({e: [] for e in ETKButtonEvents})

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
