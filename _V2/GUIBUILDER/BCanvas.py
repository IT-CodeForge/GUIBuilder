from tkinter import Canvas, Tk
from BBaseWidget import BBaseWidget
from vector2d import vector2d
from enum import Enum
from BCanvasItem import BCanvasItem
from typing import Callable, Final
from Framework_utils import gen_col_from_int
import math

class DrawMode(Enum):
    TOP_LEFT_CORNER: Final = 0,
    CENTER: Final = 1,
    BOTTOM_RIGHT_CORNER: Final = 2

class BCanvas(BBaseWidget):
    def __init__(self, myTk:Tk, pos_x:int=0, pos_y:int=0, width:int=100, height:int=100, fill:int=0xFFFFFF) -> None:
        self.__bg_col = gen_col_from_int(fill)
        self.object_id:Canvas = Canvas(myTk,bg=self.__bg_col)
        super().__init__(vector2d(pos_x, pos_y), vector2d(width, height))
        self.__draw_mode_trans = {
                        DrawMode.TOP_LEFT_CORNER:lambda pos, width, height : [pos,pos+vector2d(width, height)],
                        DrawMode.BOTTOM_RIGHT_CORNER:lambda pos, width, height : [pos,pos-vector2d(width, height)],
                        DrawMode.CENTER:lambda pos, width, height : [pos-vector2d(width/2, height/2),pos+vector2d(width/2, height/2)]}
    
    def draw_square(self, pos:vector2d, side_lenght:int, fill_col:int=0xFF0000, outline_col:int=0x000000, draw_mode:DrawMode = DrawMode.TOP_LEFT_CORNER)->BCanvasItem:
        top_left,bottom_right = self.__draw_mode_trans[draw_mode](pos,side_lenght,side_lenght)
        my_fill_col = gen_col_from_int(fill_col)
        my_outline_col = gen_col_from_int(outline_col)
        return BCanvasItem(self.object_id, "square", top_left, bottom_right, my_fill_col, my_outline_col)
    
    def draw_rect(self, top_left:vector2d, bottom_right:vector2d, fill_col:int=0xFF0000, outline_col:int=0x000000)->BCanvasItem:
        my_fill_col = gen_col_from_int(fill_col)
        my_outline_col = gen_col_from_int(outline_col)
        return BCanvasItem(self.object_id, "rectangle", top_left, bottom_right, my_fill_col, my_outline_col)
    
    def draw_circle(self, center:vector2d, radian:int, fill_col:int=0x00FF00, outline_col:int=0x000000)->BCanvasItem:
        my_fill_col = gen_col_from_int(fill_col)
        my_outline_col = gen_col_from_int(outline_col)
        return BCanvasItem(self.object_id, "circle", center, radian, radian, my_fill_col, my_outline_col)

    def draw_oval(self, center:vector2d, radian_x:int, radian_y:int, fill_col:int=0x00FF00, outline_col:int=0x000000)->BCanvasItem:
        my_fill_col = gen_col_from_int(fill_col)
        my_outline_col = gen_col_from_int(outline_col)
        return BCanvasItem(self.object_id, "oval", center, radian_x, radian_y, my_fill_col, my_outline_col)
    
    def draw_polygon(self, corner_list:list[vector2d], fill_col:int=0x0000FF, outline_col:int=0x000000)->BCanvasItem:
        my_fill_col = gen_col_from_int(fill_col)
        my_outline_col = gen_col_from_int(outline_col)
        return BCanvasItem(self.object_id, "polygon", corner_list, my_fill_col, my_outline_col)
    
    def draw_line(self, pos1:vector2d, pos2:vector2d, line_col:int=0x000000, line_thickness:int=2)->BCanvasItem:
        my_fill_col = gen_col_from_int(line_col)
        return BCanvasItem(self.object_id, "line", [pos1, pos2], my_fill_col, line_thickness)