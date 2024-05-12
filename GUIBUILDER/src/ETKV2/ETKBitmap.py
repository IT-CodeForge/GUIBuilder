from .Internal.ETKBaseTkWidgetDisableable import ETKBaseTkWidgetDisableable
from .Internal.ETKBaseTkObject import ETKBaseEvents  # type:ignore
from .Internal.ETKUtils import gen_col_from_int
from .vector2d import vector2d
from tkinter import PhotoImage, Label, Tk
from typing import Any, Iterable


class ETKBitmap(ETKBaseTkWidgetDisableable):
    def __init__(self, tk: Tk, pos: vector2d, size: vector2d, *, visibility: bool = True, enabled: bool = True, background_color: int = 0xAAAAAA, outline_color: int = 0x0, outline_thickness: int = 0, **kwargs: Any) -> None:
        self.__bitmap = PhotoImage(width=int(size.x), height=int(size.y))
        self._tk_object: Label = Label(  # type:ignore
            tk, text="", image=self.__bitmap)
        super().__init__(pos=pos, size=size, visibility=visibility, enabled=enabled, background_color=background_color, outline_color=outline_color, outline_thickness=outline_thickness, **kwargs)

    # region Properties

    @ETKBaseTkWidgetDisableable.size.setter
    def size(self, value: vector2d) -> None:
        ETKBaseTkWidgetDisableable.size.fset(self, value)  # type:ignore
        self.__bitmap.configure(width=int(value.x), height=int(value.y))

    # endregion
    # region Methods

    def __getitem__(self, index: vector2d | Iterable[int]) -> int:
        if type(index) not in [vector2d, Iterable]:
            raise TypeError(
                f"You can only check Bitmap on a specific position, so use an vector or an iterable with lenght two, {type(index)} is not supported")
        my_index: Iterable[int]
        if type(index) == vector2d:
            my_index = [int(index.x), int(index.y)]
        else:
            my_index = index  # type:ignore
        red, green, blue = self.__bitmap.get(*my_index)
        color = blue + (green << 8) + (red << 16)
        return color

    def __setitem__(self, index: vector2d | Iterable[int], value: int) -> None:
        if type(index) not in [vector2d, Iterable]:
            raise TypeError(
                f"You can only check Bitmap on a specific position, so use an vector or an iterable with lenght two, {type(index)} is not supported")
        my_index: tuple[int, int]
        if type(index) == vector2d:
            my_index = (int(index.x), int(index.y))
        else:
            my_index = tuple(index)  # type:ignore
        color = gen_col_from_int(value)
        self.__bitmap.put(color, my_index)
        self._tk_object.configure(image=self.__bitmap)

    def clear(self) -> None:
        self.__bitmap.blank()

    # endregion
