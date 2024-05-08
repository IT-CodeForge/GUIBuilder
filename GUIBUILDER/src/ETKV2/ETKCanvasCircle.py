from tkinter import Canvas
from typing import Any
from .ETKCanvasOval import ETKCanvasOval
from .vector2d import vector2d


class ETKCanvasCircle(ETKCanvasOval):
    def __init__(self, canvas: Canvas, center: vector2d, radius: int, background_color: int, outline_color: int, **kwargs: Any) -> None:
        super().__init__(canvas, center,
                               radius, radius, background_color, outline_color, **kwargs)
        self._item_type = "circle"
