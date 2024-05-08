from tkinter import Canvas
from typing import Any
from .ETKCanvasRectangle import ETKCanvasRectangle
from .vector2d import vector2d


class ETKCanvasSquare(ETKCanvasRectangle):
    def __init__(self, canvas: Canvas, top_left: vector2d, side_length: float, background_color: int, outline_color: int, **kwargs: Any) -> None:
        bottom_right = top_left + vector2d(side_length, side_length)
        ETKCanvasRectangle.__init__(
            self, canvas, top_left, bottom_right, background_color, outline_color, **kwargs)
        self._item_type = "square"
