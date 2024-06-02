from enum import Enum, auto
from typing import Any

from .ETKMainWindow import ETKMain

from .Internal.ETKBaseContainer import ETKAlignments
from .Internal.ETKBaseWidget import ETKBaseWidget
from .ETKContainer import ETKContainerSize
from .Vector2d import Vector2d
from .Internal.ETKBaseContainer import ETKBaseContainer, _ETKSubAlignments, SizeError  # type:ignore


class ElementPosLockedError(AttributeError):
    pass


class ETKListingTypes(Enum):
    TOP_TO_BOTTOM = auto()
    BOTTOM_TO_TOP = auto()
    LEFT_TO_RIGHT = auto()
    RIGHT_TO_LEFT = auto()


class ETKListingContainer(ETKBaseContainer):
    def __init__(self, main: ETKMain, pos: Vector2d = Vector2d(0, 0), size: ETKContainerSize = ETKContainerSize(0, 0, True, True), alignment: ETKAlignments = ETKAlignments.TOP_LEFT, listing_type: ETKListingTypes = ETKListingTypes.TOP_TO_BOTTOM, offset: int = 10, *, visibility: bool = True, enabled: bool = True, background_color: int = 0xAAAAAA, outline_color: int = 0x0, outline_thickness: int = 0, **kwargs: Any) -> None:
        self.__alignment = alignment
        self.__listing_type = listing_type
        self.__offset = offset

        super().__init__(main=main, pos=pos, size=size, visibility=visibility, enabled=enabled, background_color=background_color, outline_color=outline_color, outline_thickness=outline_thickness, **kwargs)

    # region Properties

    @ETKBaseContainer.size.setter
    def size(self, value: ETKContainerSize | Vector2d) -> None:
        ETKBaseContainer.size.fset(self, value)  # type:ignore
        self._scheduler.schedule_event_action(self._update_all_element_pos)

    # endregion
    # region Methods

    def _update_all_element_pos(self) -> None:
        if self.__listing_type in [ETKListingTypes.TOP_TO_BOTTOM, ETKListingTypes.BOTTOM_TO_TOP]:
            listing_dir_index = 1
            non_listing_dir_index = 0
        else:
            listing_dir_index = 0
            non_listing_dir_index = 1

        elements = [e for e in self._element_rel_pos.keys() if e.abs_visibility]
        sizes = [e.size for e in elements]

        if len(elements) == 0:
            return

        listing_dir_size = sum([s[listing_dir_index]
                               for s in sizes]) + self.__offset * (len(sizes) - 1)
        non_listing_dir_size = max([s[non_listing_dir_index] for s in sizes])

        needed_size = Vector2d()
        needed_size[listing_dir_index] = listing_dir_size
        needed_size[non_listing_dir_index] = non_listing_dir_size

        if self.size.dynamic_x:
            self._container_size.x = int(
                needed_size.x) + self.size.padding_x_l + self.size.padding_x_r
        if self.size.dynamic_y:
            self._container_size.y = int(
                needed_size.y) + self.size.padding_y_o + self.size.padding_y_u

        # print(needed_size, self.size)

        ETKBaseContainer.size.fset(self, self.size)  # type:ignore

        # print(needed_size, self.size)

        if listing_dir_size > self.size[listing_dir_index] or non_listing_dir_size > self.size[non_listing_dir_index]:
            raise SizeError(
                f"size of container {self} is too small\ncontainer: size: {self.size}; needed: {needed_size}")

        listing_dir_pos = self.__calculate_pos_part(
            listing_dir_index, listing_dir_size, (self.size[4+2*listing_dir_index], self.size[5+2*listing_dir_index]))

        if self.__listing_type in [ETKListingTypes.BOTTOM_TO_TOP, ETKListingTypes.RIGHT_TO_LEFT]:
            elements = elements[::-1]

        for e in elements:
            non_listing_dir_pos = self.__calculate_pos_part(
                non_listing_dir_index, e.size[non_listing_dir_index], (self.size[4+2*non_listing_dir_index], self.size[5+2*non_listing_dir_index]))
            pos = Vector2d()
            pos[listing_dir_index] = listing_dir_pos
            pos[non_listing_dir_index] = non_listing_dir_pos
            self._element_rel_pos[e] = pos
            e._pos = pos
            self._scheduler.schedule_event_action(e._update_pos, False)
            listing_dir_pos += e.size[listing_dir_index] + self.__offset

    def __calculate_pos_part(self, index: int, size_part: float, padding_part: tuple[float, float]) -> float:
        match self.__alignment.value[index]:
            case _ETKSubAlignments.MIN:
                return padding_part[0]
            case _ETKSubAlignments.MIDDLE:
                return 0.5 * (self.size[index] - padding_part[0] - padding_part[1]) - 0.5 * size_part + padding_part[0]
            case _ETKSubAlignments.MAX:
                return self.size[index] - size_part - padding_part[1]

    def insert_element(self, element: ETKBaseWidget, index: int) -> None:
        self._prepare_element_add(element)

        element_list = list(self._element_rel_pos.items())
        element_list.insert(index, (element, Vector2d()))
        self._element_rel_pos = dict(element_list)

        self._scheduler.schedule_event_action(self._update_all_element_pos)

    # region child validation methods

    def _validate_pos(self, element: ETKBaseWidget) -> None:
        pass
        # raise ElementPosLockedError(
        #     f"pos of element {element} is locked by ListingContainer {self}")
        # NOTE!!!

    # endregion
    # endregion
