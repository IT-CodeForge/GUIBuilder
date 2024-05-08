from typing import Any
from .vector2d import vector2d
from .Internal.ETKBaseTkWidgetDisableable import ETKBaseTkWidgetDisableable
from .Internal.ETKBaseTkObject import ETKBaseEvents  # type:ignore
from .ETKCanvasItem import ETKCanvasItem
from .ETKCanvasRectangle import ETKCanvasRectangle
from .ETKCanvasSquare import ETKCanvasSquare
from .ETKCanvasOval import ETKCanvasOval
from .ETKCanvasCircle import ETKCanvasCircle
from .ETKCanvasLine import ETKCanvasLine
from tkinter import Canvas, Tk


class ETKCanvas(ETKBaseTkWidgetDisableable):
    def __init__(self, tk: Tk, pos: vector2d, size: vector2d, background_color: int = 0xFFFFFF, **kwargs: Any) -> None:
        self._tk_object: Canvas = Canvas(tk, highlightthickness=0)  # type:ignore
        self.__canvas_items: list[ETKCanvasItem] = []
        super().__init__(pos=pos, size=size, background_color=background_color, **kwargs)

    # region Properties

    @property
    def canvas_items(self) -> list[ETKCanvasItem]:
        """READ-ONLY"""
        return self.__canvas_items.copy()

    # endregion

    # region Methods

    def draw_square(self, top_left: vector2d, side_length: int, background_color: int = 0xFF0000, outline_color: int = 0x000000) -> ETKCanvasItem:
        self.__canvas_items.append(ETKCanvasSquare(self._tk_object, top_left, side_length, background_color, outline_color))
        return self.__canvas_items[-1]

    def draw_rectangle(self, top_left: vector2d, bottom_right: vector2d, background_color: int = 0xFF0000, outline_color: int = 0x000000) -> ETKCanvasItem:
        self.__canvas_items.append(ETKCanvasRectangle(self._tk_object, top_left, bottom_right, background_color, outline_color))
        return self.__canvas_items[-1]

    def draw_circle(self, center: vector2d, radius: int, background_color: int = 0x00FF00, outline_color: int = 0x000000) -> ETKCanvasItem:
        self.__canvas_items.append(ETKCanvasCircle(self._tk_object, center, radius, background_color, outline_color))
        return self.__canvas_items[-1]

    def draw_oval(self, center: vector2d, radius_x: int, radius_y: int, background_color: int = 0x00FF00, outline_color: int = 0x000000) -> ETKCanvasItem:
        self.__canvas_items.append(ETKCanvasOval(self._tk_object, center, radius_x, radius_y, background_color, outline_color))
        return self.__canvas_items[-1]

    def draw_polygon(self, corner_list: list[vector2d], background_color: int = 0x0000FF, outline_color: int = 0x000000) -> ETKCanvasItem:
        self.__canvas_items.append(ETKCanvasItem(self._tk_object, corner_list, background_color, outline_color))
        return self.__canvas_items[-1]

    def draw_line(self, start_point: vector2d, end_point: vector2d, thickness: float = 2, background_color: int = 0x000000, outline_color: int = 0x000000) -> ETKCanvasItem:
        self.__canvas_items.append(ETKCanvasLine(self._tk_object, start_point, end_point, thickness, background_color, outline_color))
        return self.__canvas_items[-1]

    def delete_item(self, item: ETKCanvasItem) -> None:
        for index, canvas_item in enumerate(self.__canvas_items):
            if canvas_item == item:
                self.delete_item_at_index(index)
                break

    def delete_item_at_index(self, index: int) -> None:
        self.__canvas_items[index]._isdeleted = True  # type:ignore
        del self.__canvas_items[index]

    def clear(self) -> None:
        for index, canvasitem in enumerate(self.__canvas_items):
            canvasitem._isdeleted = True  # type:ignore
            del self.__canvas_items[index]

    # endregion
