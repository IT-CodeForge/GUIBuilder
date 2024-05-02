from abc import abstractmethod
from enum import auto
import sys
from tkinter import Event, Tk, EventType
from types import NoneType
from typing import Any, Callable, Optional

from .ETKCanvas import ETKCanvas
from .vector2d import vector2d
from .Internal.ETKBaseTkObject import ETKBaseTkObject
from .Internal.ETKBaseTkObject import ETKBaseEvents  # type:ignore
from .Internal.ETKBaseObject import ETKEvents


class ETKWindowEvents(ETKEvents):
    KEY_PRESSED = ("<KeyDown>", auto())
    KEY_RELEASED = ("<KeyRelease>", auto())
    FOCUS_IN = ("<FocusIn>", auto())
    FOCUS_OUT = ("<FocusOut>", auto())
    START = ("<Custom>", auto())
    EXIT = ("<Custom>", auto())


class ETKMainWindow(ETKBaseTkObject):
    def __init__(self, pos: vector2d = vector2d(0, 0), size: Optional[vector2d] = None, caption: str = "Window-Title", fullscreen: bool = True, background_color: int = 0xAAAAAA) -> None:
        self._tk_object: Tk = Tk()
        self.caption = caption
        self.__topmost = False
        self.exit_locked = False
        self.__fullscreen = False
        self.canvas = ETKCanvas(self._tk_object, vector2d(), vector2d())
        self.canvas.outline_color = 0x0
        self.canvas.outline_thickness = 2
        ETKBaseTkObject.__init__(
            self, pos, vector2d(1920, 1080), background_color)
        self.fullscreen = fullscreen
        self.size = size
        self._tk_object.protocol("WM_DELETE_WINDOW", self.exit)
        self._event_lib.update({e: [] for e in ETKWindowEvents})
        self._tk_object.bind(
            "<Configure>", self.__resize_event_handler)  # type:ignore

        self._tk_object.after(0, self._add_elements)
        self._tk_object.after(1, self._handle_event, ETKWindowEvents.START)
        self._on_init()

    # region Properties

    @ETKBaseTkObject.pos.setter
    def pos(self, value: vector2d) -> None:
        ETKBaseTkObject.pos.fset(self, value)  # type:ignore
        self.__place_object()
    
    @property
    def abs_pos(self) -> vector2d:
        """READ-ONLY"""
        return vector2d(self._tk_object.winfo_rootx(), self._tk_object.winfo_rooty())

    @ETKBaseTkObject.size.setter
    def size(self, value: Optional[vector2d]) -> None:
        if type(value) == NoneType:
            old_state = self._tk_object.state()
            self._tk_object.state("zoomed")
            self._tk_object.update()
            t_value = vector2d(self._tk_object.winfo_width(),
                               self._tk_object.winfo_height())
            self._tk_object.state(old_state)
        else:
            t_value = value
        ETKBaseTkObject.size.fset(self, t_value)  # type:ignore
        self.canvas.size = t_value
        self.__place_object()

    @property
    def fullscreen(self) -> bool:
        return self.__fullscreen

    @fullscreen.setter
    def fullscreen(self, value: bool) -> None:
        self.__fullscreen = value
        if value:
            self._tk_object.state("zoomed")
        else:
            self._tk_object.state("normal")

    @property
    def caption(self) -> str:
        return self._tk_object.title()

    @ETKBaseTkObject.visibility.setter
    def visibility(self, value: bool) -> None:
        ETKBaseTkObject.visibility.fset(self, value)  # type: ignore
        if not value:
            self._tk_object.withdraw()
        else:
            self._tk_object.deiconify()
            self.force_focus()

    @caption.setter
    def caption(self, value: str) -> None:
        self._tk_object.title(value)

    @ETKBaseTkObject.background_color.setter
    def background_color(self, value: Optional[int]) -> None:
        ETKBaseTkObject.background_color.fset(self, value)  # type:ignore
        self.canvas.background_color = value

    @property
    def topmost(self) -> bool:
        return self.__topmost

    @topmost.setter
    def topmost(self, value: bool) -> None:
        self.__topmost = value
        self._tk_object.attributes('-topmost', self.__topmost)  # type:ignore

    # endregion
    # region Methods

    @abstractmethod
    def _on_init(self) -> None:
        pass

    @abstractmethod
    def _add_elements(self) -> None:
        pass

    def run(self) -> None:
        self._tk_object.mainloop()

    def exit(self) -> None:
        self._handle_event(ETKWindowEvents.EXIT)
        if not self.exit_locked:
            sys.exit()

    def force_focus(self) -> None:
        self._tk_object.attributes('-topmost', 1)  # type:ignore
        self._tk_object.focus_force()
        self._tk_object.attributes('-topmost', self.__topmost)  # type:ignore

    def exec_gui_function(self, function: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
        self._tk_object.after(0, lambda: function(*args, **kwargs))

    def __resize_event_handler(self, event: Event):  # type:ignore
        if self.fullscreen:
            self.fullscreen = True

    def __place_object(self) -> None:
        self._tk_object.geometry(
            f"{int(self.size.x)}x{int(self.size.y)}+{self.pos.x}+{self.pos.y}")

    def _handle_tk_event(self, event: Event) -> None:  # type:ignore
        match event.type:
            case EventType.KeyPress:
                self._handle_event(ETKWindowEvents.KEY_PRESSED,
                                   [event])  # type:ignore
                return
            case EventType.KeyRelease:
                self._handle_event(ETKWindowEvents.KEY_RELEASED,
                                   [event])  # type:ignore
                return
            case EventType.FocusIn:
                self._handle_event(ETKWindowEvents.FOCUS_IN,
                                   [event])  # type:ignore
                return
            case EventType.FocusOut:
                self._handle_event(ETKWindowEvents.FOCUS_OUT,
                                   [event])  # type:ignore
                return
            case _:
                pass
        ETKBaseTkObject._handle_tk_event(self, event)  # type:ignore

    # endregion
