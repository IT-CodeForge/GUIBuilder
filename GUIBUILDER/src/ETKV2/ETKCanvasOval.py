import math
from tkinter import Canvas
from .vector2d import vector2d
from .ETKCanvasItem import ETKCanvasItem


class ETKCanvasOval(ETKCanvasItem):
    def __init__(self, canvas: Canvas, center: vector2d, radius_x: int, radius_y: int, background_color: int, outline_color: int) -> None:
        self._center = center
        temp_pointlist: list[vector2d] = self.__poly_oval(
            center, radius_x, radius_y)
        ETKCanvasItem.__init__(self, canvas, temp_pointlist,
                               background_color, outline_color)
        self._item_type = "oval"

    # region Properties

    @ETKCanvasItem.pos.getter
    def pos(self) -> vector2d:
        return self._center.copy()

    # endregion
    # region Methods

    def __poly_oval(self, center: vector2d, radius_x: int, radius_y: int) -> list[vector2d]:
        """generates the cornerpoints, for a polygon which symbolizes the oval"""
        # steps is the number of corners the polygon has
        steps = int((radius_x * radius_y) / 4)
        point_list: list[vector2d] = []
        theta = 0
        for _ in range(steps):
            my_point = center + \
                vector2d(radius_x * math.cos(theta),
                         radius_y * math.sin(theta))
            point_list.append(my_point)
            theta += (2*math.pi) / steps
        return point_list

    # endregion
