from __future__ import annotations
from abc import abstractmethod
from enum import Enum, auto
from tkinter import Tk
from typing import Any, Callable, Optional
from .ETKBaseObject import ETKEvents, ETKBaseObject

from .ETKBaseWidget import ETKBaseWidget
from ..vector2d import vector2d
from .ETKBaseWidgetDisableable import ETKBaseWidgetDisableable
from ..ETKCanvas import ETKCanvas

# region Enums


class _ETKSubAlignments(Enum):
    MIN = auto()
    MIDDLE = auto()
    MAX = auto()


class ETKAlignments(Enum):
    TOP_LEFT = (_ETKSubAlignments.MIN, _ETKSubAlignments.MIN)
    TOP_CENTER = (_ETKSubAlignments.MIDDLE, _ETKSubAlignments.MIN)
    TOP_RIGHT = (_ETKSubAlignments.MAX, _ETKSubAlignments.MIN)
    MIDDLE_LEFT = (_ETKSubAlignments.MIN, _ETKSubAlignments.MIDDLE)
    MIDDLE_CENTER = (_ETKSubAlignments.MIDDLE, _ETKSubAlignments.MIDDLE)
    MIDDLE_RIGHT = (_ETKSubAlignments.MAX, _ETKSubAlignments.MIDDLE)
    BOTTOM_LEFT = (_ETKSubAlignments.MIN, _ETKSubAlignments.MAX)
    BOTTOM_CENTER = (_ETKSubAlignments.MIDDLE, _ETKSubAlignments.MAX)
    BOTTOM_RIGHT = (_ETKSubAlignments.MAX, _ETKSubAlignments.MAX)

# endregion

# region Dataclass: ContainerSize


class ETKContainerSize():
    def __init__(self, x: int | float = 0, y: int | float = 0, dynamic_x: bool = False, dynamic_y: bool = False, paddings_x_l: int = 0, paddings_x_r: int = 0, paddings_y_o: int = 0, paddings_y_u: int = 0) -> None:
        self.__x: int = 0
        self.__y: int = 0
        self.x = x
        self.y = y
        self.dynamic_x: bool = dynamic_x
        self.dynamic_y: bool = dynamic_y
        self.padding_x_l: int = paddings_x_l
        self.padding_x_r: int = paddings_x_r
        self.padding_y_o: int = paddings_y_o
        self.padding_y_u: int = paddings_y_u

    @property
    def x(self) -> int:
        return self.__x

    @x.setter
    def x(self, value: int | float) -> None:
        self.__x = int(value)

    @property
    def y(self) -> int:
        return self.__y

    @y.setter
    def y(self, value: int | float) -> None:
        self.__y = int(value)

    @staticmethod
    def from_vector2d(vec: vector2d) -> ETKContainerSize:
        return ETKContainerSize(vec.x, vec.y)

    def copy(self) -> ETKContainerSize:
        return ETKContainerSize(self.x, self.y, self.dynamic_x, self.dynamic_y, self.padding_x_l, self.padding_x_r, self.padding_y_o, self.padding_y_u)

    @property
    def vec(self) -> vector2d:
        """READ-ONLY"""
        return vector2d(self.x, self.y)

    def __str__(self) -> str:
        return f"<{self.x}, {self.y}, {self.dynamic_x}, {self.dynamic_y}, {self.padding_x_l}, {self.padding_x_r}, {self.padding_y_o}, {self.padding_y_u}>"

    def __setitem__(self, address: int, other: int | bool | float) -> None:
        if address not in range(0, 8):
            raise KeyError("Invalid index")
        match address:
            case 0:
                self.x = other
            case 1:
                self.y = other
            case 2:
                self.dynamic_x = bool(other)
            case 3:
                self.dynamic_y = bool(other)
            case 4:
                self.padding_x_l = int(other)
            case 5:
                self.padding_x_r = int(other)
            case 6:
                self.padding_y_o = int(other)
            case 7:
                self.padding_y_u = int(other)
            case _:
                pass

    def __getitem__(self, address: int) -> int | bool:
        if address not in range(0, 8):
            raise KeyError("Invalid index")
        match address:
            case 0:
                return self.x
            case 1:
                return self.y
            case 2:
                return self.dynamic_x
            case 3:
                return self.dynamic_y
            case 4:
                return self.padding_x_l
            case 5:
                return self.padding_x_r
            case 6:
                return self.padding_y_o
            case 7:
                return self.padding_y_u
            case _:
                raise KeyError

# endregion

# region ExceptionTypes


class ElementAlreadyAddedError(ValueError):
    pass


class AddContainerToItselfError(ValueError):
    pass


class ElementNotPartOfContainerError(ValueError):
    pass


class SizeError(ValueError):
    pass


class PosError(ValueError):
    pass

# endregion


class ETKBaseContainer(ETKBaseWidgetDisableable):
    def __init__(self, *, tk: Tk, pos: vector2d, size: ETKContainerSize, background_color: int, outline_thickness: int, outline_color: int, **kwargs: Any) -> None:
        self.__background = ETKCanvas(tk, pos, size.vec, background_color)
        self._container_size: ETKContainerSize = ETKContainerSize(0, 0)
        self._element_rel_pos: dict[ETKBaseWidget, vector2d] = {}

        super().__init__(pos=pos, size=size.vec, background_color=background_color, **kwargs)

        self.outline_color = outline_color
        self.outline_thickness = outline_thickness
        self.size = size

    # region properties

    @ETKBaseWidgetDisableable.pos.setter
    def pos(self, value: vector2d) -> None:
        ETKBaseWidgetDisableable.pos.fset(self, value)  # type:ignore
        self.__background.pos = self.abs_pos

    @property
    def size(self) -> ETKContainerSize:  # type:ignore
        return self._container_size.copy()

    @size.setter
    def size(self, value: ETKContainerSize | vector2d) -> None:
        if type(value) == ETKContainerSize:
            self._container_size = value
            vec = value.vec
        else:
            self._container_size = ETKContainerSize(int(value.x), int(value.y))
            vec = value
        ETKBaseWidgetDisableable.size.fset(self, vec)  # type:ignore
        self.__background.size = self.size.vec

    @property
    def elements(self) -> tuple[ETKBaseWidget, ...]:
        return tuple(self._element_rel_pos.keys())

    @property
    def outline_color(self) -> int:
        return self.__background.outline_color

    @outline_color.setter
    def outline_color(self, value: int) -> None:
        self.__background.outline_color = value

    @property
    def outline_thickness(self) -> int:
        return self.__background.outline_thickness

    @outline_thickness.setter
    def outline_thickness(self, value: int) -> None:
        self.__background.outline_thickness = value

    @property
    def background_color(self) -> int:
        return self.__background.background_color

    @background_color.setter
    def background_color(self, value: int) -> None:
        self.__background.background_color = value

    # endregion

    # region Methods

    @abstractmethod
    def _update_all_element_pos(self) -> None:
        pass

    def add_element(self, element: ETKBaseWidget) -> None:
        self._prepare_element_add(element)

        self._element_rel_pos.update({element: vector2d()})

        self._update_all_element_pos()

    def _prepare_element_add(self, element: ETKBaseWidget) -> None:
        if element in self._element_rel_pos.keys():
            raise ElementAlreadyAddedError(
                f"element {element} is already in container {self}")
        if element == self:
            raise AddContainerToItselfError(
                f"cannot add container {self} to itself")

        element._parent = self

        events = [ev for ev in self._event_lib.keys() if len(
            self._event_lib[ev]) != 0]
        for ev in events:
            element.add_event(ev, self.__event_handler)

    def remove_element(self, element: ETKBaseWidget) -> None:
        if element not in self._element_rel_pos.keys():
            raise ElementNotPartOfContainerError(
                f"element {element} is not in container {self}")
        self._element_rel_pos.pop(element)
        element._parent = None
        element.pos = vector2d(0, 0)

        events = [ev for ev in self._event_lib.keys() if len(
            self._event_lib[ev]) != 0]
        for ev in events:
            element.remove_event(ev, self.__event_handler)

        element._update_pos()
        self._update_all_element_pos()

    def add_event(self, event_type: ETKEvents, eventhandler: Callable[[], None] | Callable[[tuple[ETKBaseObject, ETKEvents, Any]], None]) -> None:
        super().add_event(event_type, eventhandler)
        self.__background.add_event(event_type, self.__event_handler)
        for e in self._element_rel_pos.keys():
            e.add_event(event_type, self.__event_handler)

    def remove_event(self, event_type: ETKEvents, eventhandler: Callable[[], None] | Callable[[tuple[ETKBaseObject, ETKEvents, Any]], None]) -> None:
        super().remove_event(event_type, eventhandler)
        self.__background.remove_event(event_type, self.__event_handler)
        for e in self._element_rel_pos.keys():
            e.remove_event(event_type, self.__event_handler)

    def __event_handler(self, data: tuple[ETKBaseObject, ETKEvents, Optional[Any]]) -> None:
        obj = data[0]
        if obj == self.__background:
            obj = self
        self._handle_event(data[1], [data[2], obj])

    # region update event methods

    def _update_pos(self) -> None:
        for e in self._element_rel_pos.keys():
            e._update_pos()
        self.__background.pos = self.abs_pos

    def _update_visibility(self) -> None:
        self._update_all_element_pos()
        for e in self._element_rel_pos.keys():
            e._update_visibility()
        self.__background.visibility = self.abs_visibility

    def _update_enabled(self) -> None:
        for e in self._element_rel_pos.keys():
            e._update_enabled()

    # endregion
    # region child validation methods

    def _get_childs_abs_pos(self, child: ETKBaseWidget) -> vector2d:
        if child not in self._element_rel_pos.keys():
            raise ElementNotPartOfContainerError(
                f"element {child} is not in container {self}")
        pos = self._element_rel_pos[child]
        return vector2d(pos.x + self.abs_pos.x, pos.y + self.abs_pos.y)

    def _detach_child(self, element: ETKBaseWidget) -> None:
        self.remove_element(element)

    def _validate_size(self, element: ETKBaseWidget) -> None:
        self._update_all_element_pos()
        element._update_pos()

    def _validate_pos(self, element: ETKBaseWidget) -> None:
        self._update_all_element_pos()
        element._update_pos()

    def _validate_visibility(self, element: ETKBaseWidget) -> None:
        self._update_all_element_pos()
        element._update_pos()

    # endregion
    # endregion
