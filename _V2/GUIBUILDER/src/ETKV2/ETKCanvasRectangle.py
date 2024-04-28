from tkinter import Canvas
from .vector2d import vector2d
from .ETKCanvasItem import ETKCanvasItem


class ETKCanvasRectangle(ETKCanvasItem):
    def __init__(self, canvas: Canvas, top_left: vector2d, bottom_right: vector2d, background_color: int, outline_color: int) -> None:
        temp_pointlist = [top_left, vector2d(
            bottom_right.x, top_left.y), bottom_right, vector2d(top_left.x, bottom_right.y)]
        ETKCanvasItem.__init__(self, canvas, temp_pointlist,
                               background_color, outline_color)
        self._item_type = "rectangle"
