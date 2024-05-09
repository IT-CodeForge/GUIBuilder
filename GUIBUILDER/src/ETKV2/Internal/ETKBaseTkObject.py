from tkinter import Event, EventType
from typing import Any, Callable, Optional

from .ETKUtils import gen_col_from_int

from ..vector2d import vector2d
from .ETKBaseObject import ETKBaseObject, ETKEvents, ETKBaseEvents


class ETKBaseTkObject(ETKBaseObject):
    def __init__(self, *, pos: vector2d, size: vector2d, background_color: int, **kwargs: Any) -> None:
        self._tk_object: Any

        super().__init__(pos=pos, size=size, background_color=background_color, **kwargs)

        self._tk_object.configure(borderwidth=0)

    # region Properties

    @ETKBaseObject.background_color.setter
    def background_color(self, value: Optional[int]) -> None:
        ETKBaseObject.background_color.fset(self, value)  # type:ignore
        self._tk_object.configure(background=gen_col_from_int(value))

    # endregion
    # region Methods

    def __del__(self) -> None:
        self.visibility = False

    # region Eventhandling Methods

    def add_event(self, event_type: ETKEvents, eventhandler: Callable[[], None] | Callable[[tuple[ETKBaseObject, ETKEvents, Any]], None]) -> None:
        if event_type.value[0] != "<Custom>":
            if len(self._event_lib[event_type]) == 0:
                self._tk_object.bind(
                    event_type.value[0], self._handle_tk_event)  # type:ignore
        super().add_event(event_type, eventhandler)

    def remove_event(self, event_type: ETKEvents, eventhandler: Callable[[], None] | Callable[[tuple[ETKBaseObject, ETKEvents, Any]], None]) -> None:
        super().remove_event(event_type, eventhandler)
        if event_type.value[0] != "<Custom>":
            if len(self._event_lib[event_type]) == 0:
                self._tk_object.unbind(event_type.value[0])

    def _handle_tk_event(self, event: Event) -> None:  # type:ignore
        match event.type:
            case EventType.ButtonPress:
                event_type = ETKBaseEvents.MOUSE_DOWN
            case EventType.ButtonRelease:
                event_type = ETKBaseEvents.MOUSE_UP
            case EventType.Enter:
                event_type = ETKBaseEvents.ENTER
            case EventType.Leave:
                event_type = ETKBaseEvents.LEAVE
            case EventType.Motion:
                event_type = ETKBaseEvents.MOUSE_MOVED
            case _:
                raise ValueError(f"invalid event {event}")

        self._handle_event(event_type, [event])  # type:ignore

    # endregion
    # endregion
