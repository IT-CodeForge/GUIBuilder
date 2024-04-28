from abc import abstractmethod
from enum import auto
from tkinter import Event, Tk, EventType
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
    def __init__(self, pos: vector2d = vector2d(0, 0), size: vector2d = vector2d(2048, 512), caption: str = "Tk", background_color: int = 0xAAAAAA) -> None:
        self._tk_object: Tk = Tk()
        self.caption = caption
        self.__topmost = False
        self.exit_locked = False
        self.canvas = ETKCanvas(self._tk_object, vector2d(), size)
        ETKBaseTkObject.__init__(self, pos, size, background_color)
        self._tk_object.protocol("WM_DELETE_WINDOW", self.exit)
        self._event_lib.update({e: [] for e in ETKWindowEvents})

        self._tk_object.after(0, self._handle_event, ETKWindowEvents.START)
        self._on_init()

        self._add_elements()

    # region Properties

    @ETKBaseTkObject.pos.setter
    def pos(self, value: vector2d) -> None:
        ETKBaseTkObject.pos.fset(self, value) #type:ignore
        self.__place_object()

    @ETKBaseTkObject.size.setter
    def size(self, value: vector2d) -> None:
        ETKBaseTkObject.size.fset(self, value) #type:ignore
        self.__place_object()

    @property
    def caption(self) -> str:
        return self._tk_object.title()

    @ETKBaseTkObject.visibility.setter
    def visibility(self, value: bool) -> None:
        ETKBaseTkObject.visibility.fset(self, value) #type: ignore
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
            exit()

    def force_focus(self) -> None:
        self._tk_object.attributes('-topmost', 1)  # type:ignore
        self._tk_object.focus_force()
        self._tk_object.attributes('-topmost', self.__topmost)  # type:ignore
    
    def exec_gui_function(self, function: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
        self._tk_object.after(0, lambda: function(*args, **kwargs))

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
