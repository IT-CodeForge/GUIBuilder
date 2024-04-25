from __future__ import annotations
from tkinter    import Canvas
from .vector2d   import vector2d
from ast        import literal_eval
from .Framework_utils import gen_col_from_int
import math

#types: "line" "rectangle" "square" "oval" "circle" "polygon"

class ETKCanvasItem:
    def __init__(self, canvas:Canvas, item_type:str, *args) -> None:
        self.__temp_sort_vec = vector2d()
        self.__my_Canvas = canvas
        self.__item_type = item_type.removeprefix("json")
        if type(args[0]) == vector2d:
            self.anchor = args[0]
        elif type(args[0]) == list:
            self.anchor = args[0][0]
        self.item_id = 0
        if item_type.startswith("json"):
            self.__col        = args.get("col", "")
            self.__line_col   = args.get("line_col", "")
            self.__thickness  = args.get("thickness", 10)
            if self.__thickness != None:
                self.__gen_line(args.get("pointlist", []), self.__line_col, self.__thickness)
            else:
                self.__make_shape(args.get("pointlist", []), self.__col, self.__line_col)
            return
        if item_type == "line":
            self.__col       = None
            self.__line_col  = args[-2]
            self.__thickness = args[-1]
            self.__gen_line(*args)
            self.__point_list = [args[0][0].x, args[0][0].y, args[0][1].x, args[0][1].y]
            return
        self.__thickness = None
        self.__col       = args[-2]
        self.__line_col  = args[-1]
        self.__point_list = self.__generate_pointlist(*args[:-2])
        self.__make_shape(self.__point_list, self.__col, self.__line_col)
    
    @property
    def fill(self)->int|None:
        return literal_eval("0x" + self.__col[1])
    
    @fill.setter
    def fill(self, value):
        if self.__col == None:
            return
        self.__col = gen_col_from_int(value)

    @property
    def line_col(self)->int:
        return literal_eval("0x" + self.__line_col[1:])
    
    @line_col.setter
    def line_col(self, value):
        self.line_col = gen_col_from_int(value)
    
    @property
    def thickness(self)->int|None:
        return self.__thickness
    
    @thickness.setter
    def thickness(self, value):
        if self.__thickness == None:
            return
        self.__thickness = value
    
    @property
    def pointlist(self)->list(vector2d):
        return self.__point_list
    
    @pointlist.setter
    def pointlist(self, value):
        self.pointlist = value
        self.__make_shape()
    
    def get_item_type(self)->str:
        return self.__item_type
    
    def stretch(self, x_stretch:float = 1, y_stretch:float = 1):
        for point in self.__point_list:
            pass

    def __generate_pointlist(self, *args):
        if self.__item_type in ["oval", "circle"]:
            self.anchor  = args[0]
            return self.__poly_oval(*args)
        if self.__item_type in ["rectangle", "square"]:
            return self.__poly_quad(*args)
        if self.__item_type == "polygon":
            return self.__point_unpacking(*args)

    def __poly_oval(self, center:vector2d, radian_x:int, radian_y:int, rotation_in_radians:float=0):
        steps = int((radian_x + radian_y) / 4)
        point_list = []
        theta = 0
        for i in range(steps):
            my_point = center + vector2d(radian_x * math.cos(theta), radian_y * math.sin(theta)).rotate(rotation_in_radians)
            point_list.append(my_point.x)
            point_list.append(my_point.y)
            theta += (2*math.pi) / steps
        return point_list

    def __poly_quad(self, top_left:vector2d, bottom_right:vector2d, rotation_in_radians:float=0):
        vec_list = [top_left, vector2d(bottom_right.x, top_left.y), bottom_right, vector2d(top_left.x, bottom_right.y)]
        vec_list_fin = [point.rotate(rotation_in_radians) for point in vec_list]
        return self.__point_unpacking(vec_list_fin)

    def __point_unpacking(self, vec_list:list[vector2d])->list[float]:
        getx = lambda vec: vec.x
        gety = lambda vec: vec.y
        return [f(point) for point in vec_list for f in (getx, gety)]
    
    def __gen_line(self, pos_list:list[vector2d, vector2d], fill:str, line_thickness:int):
        print(fill)
        self.item_id = self.__my_Canvas.create_line(pos_list[0].x, pos_list[0].y, pos_list[1].x, pos_list[1].y, fill=fill, width=line_thickness)
    
    def __make_shape(self,pointlist:list[float], fill:str, outline:str):
        self.item_id = self.__my_Canvas.create_polygon(pointlist, fill=fill, outline=outline)
    
    def rotate_with_radians(self, radians:float):
        coords = self.__my_Canvas.coords(self.item_id)
        vec_list = [self.anchor + (vector2d(coords[index*2], coords[index*2+1]) - self.anchor).rotate(radians) for index in range(len(coords)//2)]
        self.__point_list = self.__point_unpacking(vec_list)
        self.__my_Canvas.coords(self.item_id, self.__point_list)
    
    def rotate_with_degrees(self, degrees:float):
        self.rotate_with_radians(degrees * math.pi / 180)

    
    def move(self, mov_vec:vector2d):
        self.move_to(self.anchor+mov_vec)

    def move_to(self, pos:vector2d):
        for index, x_or_y in enumerate(self.__point_list):
            if index%2:
                self.__point_list[index] = x_or_y - self.anchor.y + pos.y
            else:
                self.__point_list[index] = x_or_y - self.anchor.x + pos.x
        self.anchor = pos
        self.__my_Canvas.coords(self.item_id, self.__point_list)
    
    def find_intersections(self, shape:ETKCanvasItem)->list[vector2d]:
        sol_list = []
        other_pointlist = shape.__point_list.copy()
        my_pointlist = self.__point_list.copy()
        other_pointlist += other_pointlist[:2]
        my_pointlist += my_pointlist[:2]
        for i in range(len(my_pointlist) // 2 - 1):
            for n in range(len(other_pointlist) // 2 - 1):
                p1 = vector2d(my_pointlist[i * 2], my_pointlist[i * 2 + 1])
                p2 = vector2d(my_pointlist[i * 2 + 2], my_pointlist[i * 2 + 3])
                p3 = vector2d(other_pointlist[n * 2], other_pointlist[n * 2 + 1])
                p4 = vector2d(other_pointlist[n * 2 + 2], other_pointlist[n * 2 + 3])
                sol = self.__find_intersection(p1, p2, p3, p4)
                ret_vec = sol
                if ret_vec != None and ret_vec not in sol_list:
                    sol_list.append(ret_vec)
        return sol_list
    
    def ray_casting(self, point:vector2d, direction_vec:vector2d)->list[vector2d]:
        my_pointlist = self.__point_list.copy()
        my_pointlist += my_pointlist[:2]
        p3 = point
        x_list = [self.__point_list[i * 2] for i in range(len(self.__point_list) // 2)]
        y_list = [self.__point_list[i * 2 + 1] for i in range(len(self.__point_list) // 2)]
        distance_to_window_edge = vector2d(
            max(x_list) if direction_vec.x else min(x_list),
            max(y_list) if direction_vec.y else min(y_list))
        
        sol_list = []

        p4 = point + direction_vec.normalize() * distance_to_window_edge
        for i in range(len(self.__point_list) // 2):
            p1 = vector2d(my_pointlist[i *2], my_pointlist[i * 2 + 1])
            p2 = vector2d(my_pointlist[i * 2 + 2], my_pointlist[i * 2 + 3])
            sol = self.__find_intersection(p1,p2,p3,p4)
            if sol == None or sol in sol_list:
                continue
            sol_list.append(sol)
        sol_list.sort(key=self.__sort_list_by_dis_to_vec)
        return sol_list
    def __sort_list_by_dis_to_vec(self, vector:vector2d):
        if vector == None:
            return vector
        return (self.__temp_sort_vec - vector).lenght
    
    def __winding_numbers(self, point:vector2d):
        direction_vec = vector2d(1,0)
        my_pointlist = self.__point_list.copy()
        my_pointlist += my_pointlist[:2]
        p3 = point
        x_list = [self.__point_list[i * 2] for i in range(len(self.__point_list) // 2)]
        y_list = [self.__point_list[i * 2 + 1] for i in range(len(self.__point_list) // 2)]
        distance_to_window_edge = vector2d(
            max(x_list) if direction_vec.x else min(x_list),
            max(y_list) if direction_vec.y else min(y_list))
        
        retval = 0.0

        p4 = point + direction_vec.normalize() * distance_to_window_edge
        for i in range(len(self.__point_list) // 2):
            p1 = vector2d(my_pointlist[i *2], my_pointlist[i * 2 + 1])
            p2 = vector2d(my_pointlist[i * 2 + 2], my_pointlist[i * 2 + 3])
            sol = self.__find_intersection(p1,p2,p3,p4)
            if sol == None:
                continue
            poly_edge_dir = p2 - p1
            sign = (poly_edge_dir*vector2d(0,1)).normalize().y
            if sign not in [-1,1]:
                print((poly_edge_dir*vector2d(0,1)).normalize())
                print("sign:", sign)
            if sol in [p1,p2]:
                retval += 0.5 * sign
            else:
                retval += sign
            
        return retval
    
    def is_point_in_shape(self, point:vector2d)->bool:
        w = self.__winding_numbers(point)
        if w == 0:
            return False
        else:
            return True

    def __find_intersection(self, p1:vector2d, p2:vector2d, p3:vector2d, p4:vector2d):
        s1 = p2 - p1
        s2 = p4 - p3

        denominator = s1.crossproduct(s2)

        if denominator == 0:
            return None

        s = p3 - p1
        t = s.crossproduct(s2) / denominator
        u = s.crossproduct(s1) / denominator

        if 0 <= t <= 1 and 0 <= u <= 1:
            intersection = p1 + t * s1
            return intersection
        else:
            return None
        
    def delete(self):
        del self
    
    def __del__(self):
        self.__my_Canvas.delete(self.item_id)