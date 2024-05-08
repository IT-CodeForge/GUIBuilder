from __future__ import annotations
from enum import Enum, auto
import traceback
from typing import Any, Callable, Optional

from ..vector2d import vector2d


class ETKEvents(Enum):
    pass


class ETKBaseEvents(ETKEvents):
    MOUSE_DOWN = ("<ButtonPress>", auto())
    MOUSE_UP = ("<ButtonRelease>", auto())
    ENTER = ("<Enter>", auto())
    LEAVE = ("<Leave>", auto())
    MOUSE_MOVED = ("<Motion>", auto())


class ETKBaseObject:
    def __init__(self, *, pos: vector2d, size: vector2d, background_color: int) -> None:
        self.__pos: vector2d = vector2d()
        self.__size: vector2d = vector2d()
        self.__background_color: int = 0x0
        self.__visibility: bool = True
        self._event_lib: dict[ETKEvents, list[Callable[..., Any]]] = {
            e: [] for e in ETKBaseEvents}

        self.background_color = background_color
        self.pos = pos
        self.size = size
        self.visibility = True

    # region Properties

    @property
    def pos(self) -> vector2d:
        return self.__pos.copy()

    @pos.setter
    def pos(self, value: vector2d) -> None:
        self.__pos = value

    @property
    def abs_pos(self) -> vector2d:
        """READ-ONLY"""
        return self.__pos.copy()

    @property
    def size(self) -> vector2d:
        return self.__size.copy()

    @size.setter
    def size(self, value: vector2d) -> None:
        self.__size = value

    @property
    def visibility(self) -> bool:
        return self.__visibility

    @visibility.setter
    def visibility(self, value: bool) -> None:
        self.__visibility = value

    @property
    def abs_visibility(self) -> bool:
        """READ-ONLY"""
        return self.__visibility

    @property
    def background_color(self) -> int:
        return self.__background_color

    @background_color.setter
    def background_color(self, value: int) -> None:
        self.__background_color = value

    @property
    def events(self) -> dict[ETKEvents, list[Callable[..., Any]]]:
        """READ-ONLY"""
        return self._event_lib.copy()

    # endregion
    # region Methods
    # region Eventhandling Methods

    def add_event(self, event_type: ETKEvents, eventhandler: Callable[[], None] | Callable[[tuple[ETKBaseObject, ETKEvents, Any]], None]) -> None:
        self._event_lib[event_type].append(eventhandler)

    def remove_event(self, event_type: ETKEvents, eventhandler: Callable[[], None] | Callable[[tuple[ETKBaseObject, ETKEvents, Any]], None]) -> None:
        self._event_lib[event_type].remove(eventhandler)

    def _handle_event(self, event: ETKEvents, event_data: Optional[list[Any]] = None) -> None:
        if event_data == None:
            event_data = []
        err_1 = ""
        for c in self._event_lib[event]:
            try:
                c((self, event, *event_data))
                continue
            except TypeError as ex:
                err_1 = traceback.format_exc()
                if str(ex).find("positional argument") == -1:
                    raise ex
            try:
                c()
            except TypeError as ex:
                if str(ex).find("positional argument") == -1:
                    raise ex
                ret_val = c.__code__.co_varnames
                name = c.__name__  # type:ignore
                print(err_1)
                print(traceback.format_exc())
                raise TypeError(
                    f"invalid parametercount for event function ({name}) (can only be 0, 1 (self, cls, etc not included)), parameter: {ret_val}")

    # endregion
    # endregion
