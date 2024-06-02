from __future__ import annotations
from typing import Any, Literal

from .ETKMainWindow import ETKMain
from .Internal.ETKBaseWidget import ETKBaseWidget

from .Vector2d import Vector2d

from .Internal.ETKBaseContainer import _ETKSubAlignments  # type:ignore
from .Internal.ETKBaseContainer import ETKAlignments, ETKContainerSize, SizeError, PosError, ETKBaseContainer


class ETKContainer(ETKBaseContainer):
    def __init__(self, main: ETKMain, pos: Vector2d = Vector2d(0, 0), size: ETKContainerSize = ETKContainerSize(0, 0, True, True), *, visibility: bool = True, enabled: bool = True, background_color: int = 0xAAAAAA, outline_color: int = 0x0, outline_thickness: int = 0, **kwargs: Any) -> None:
        super().__init__(main=main, pos=pos, size=size, visibility=visibility, enabled=enabled, background_color=background_color, outline_color=outline_color, outline_thickness=outline_thickness, **kwargs)
        self.__element_alignments: dict[ETKBaseWidget, ETKAlignments] = {}

    # region Properties

    @ETKBaseContainer.size.setter
    def size(self, value: ETKContainerSize | Vector2d) -> None:
        ETKBaseContainer.size.fset(self, value)  # type:ignore
        try:
            self._update_all_element_pos()
        except ValueError:
            raise SizeError(
                f"size of container {self} is too small\ncontainer: size: {self.size}")

    # endregion
    # region Methods

    def _update_all_element_pos(self) -> None:
        elements = [e for e in self._element_rel_pos.keys() if e.abs_visibility]

        max_size = [0, 0]

        if len(elements) == 0:
            return

        for e in elements:
            alignment = self.__element_alignments[e].value
            for i, sal in enumerate(alignment):
                if sal == _ETKSubAlignments.MAX:
                    size = e.size[i] + e.pos[i] * -1
                elif sal == _ETKSubAlignments.MIDDLE:
                    size = e.size[i] + abs(e.pos[i]) * 2
                else:
                    size = e.size[i] + e.pos[i]
                if size > max_size[i]:
                    max_size[i] = int(size)

        if self.size.dynamic_x:
            self._container_size.x = max_size[0] + self.size.padding_x_r
        if self.size.dynamic_y:
            self._container_size.y = max_size[1] + self.size.padding_y_u

        ETKBaseContainer.size.fset(self, self.size)  # type:ignore

        for e in elements:
            self._element_rel_pos[e] = self._calculate_rel_element_pos(e)
            self.__validate_size_pos(self._element_rel_pos[e], e.size)
            self._scheduler.schedule_event_action(e._update_pos, False)

    def _calculate_rel_element_pos(self, element: ETKBaseWidget) -> Vector2d:
        x = self._calculate_rel_element_pos_part(
            element, 0, self.size.padding_x_r)
        y = self._calculate_rel_element_pos_part(
            element, 1, self.size.padding_y_u)
        return Vector2d(x, y)

    def _calculate_rel_element_pos_part(self, element: ETKBaseWidget, index: Literal[0, 1], padding_part: float) -> float:
        match self.__element_alignments[element].value[index]:
            case _ETKSubAlignments.MIN:
                return element.pos[index]
            case _ETKSubAlignments.MIDDLE:
                return 0.5 * self.size[index] - 0.5 * element.size[index] + element.pos[index]
            case _ETKSubAlignments.MAX:
                return self.size[index] - element.size[index] + element.pos[index] - padding_part

    def __validate_size_pos(self, rel_pos: Vector2d, size: Vector2d) -> None:
        s_size = self.size

        if s_size.x > self.size.x or s_size.y > self.size.y:
            raise SizeError(
                f"size is outside of container {self}\nparameter: size: {size}; container: abs_pos: size: {self.size}")

        if rel_pos.x + size.x > s_size.x or rel_pos.y + size.y > s_size.y or rel_pos.x < 0 or rel_pos.y < 0:
            raise PosError(
                f"pos is outside of container {self}\nparameter: rel_pos: {rel_pos}, size: {size}; container: size: {self.size}")

    def add_element(self, element: ETKBaseWidget, alignment: ETKAlignments = ETKAlignments.TOP_LEFT) -> None:
        self.__element_alignments.update({element: alignment})
        super().add_element(element)

    def remove_element(self, element: ETKBaseWidget) -> None:
        super().remove_element(element)
        self.__element_alignments.pop(element)

    # endregion
