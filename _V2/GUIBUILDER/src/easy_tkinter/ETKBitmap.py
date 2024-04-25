from typing import Iterable
from .vector2d import vector2d
from tkinter  import Label, PhotoImage, Tk
from .ETKNoTKEventBase import ETKNoTKEventBase

class ETKBitmap(ETKNoTKEventBase):
    def __init__(self, my_tk:Tk, pos_x:int=0, pos_y:int=0, width:int=100, height:int=100) -> None:
        self.object_id = PhotoImage(width=width,height=height)
        self.__container = Label(my_tk, text="", image=self.object_id)
        self.__object_pos = vector2d(pos_x, pos_y)
        self.__dimensions = vector2d(width, height)
        self.__place_object()

    def __getitem__(self, index:vector2d|Iterable)->int:
        if type(index) in [vector2d, Iterable]:
            raise TypeError(f"You can only check Bitmap on a specific position, so use an vector or an iterable with lenght two, {type(index)} is not supported")
        if type(index) == vector2d:
            index = [index.x,index.y]
        self.object_id.get(*index)
    
    def __setitem__(self, index:vector2d|Iterable, value:int)->int:
        if type(index) in [vector2d, Iterable]:
            raise TypeError(f"You can only check Bitmap on a specific position, so use an vector or an iterable with lenght two, {type(index)} is not supported")
        if type(index) == vector2d:
            index = [index.x,index.y]
        if type(value) != int:
            raise TypeError(f"You can only assign an integer to a color")
        if value > 0xFFFFFF:
            raise ValueError(f"The maximum color is 0xFFFFFF, inputted value: {hex(value)}")
        color = "#%06x"%value
        self.object_id.put(color, index)

    
    @property
    def abs_pos(self)->vector2d:
        return self.__object_pos

    @property
    def pos(self)->vector2d:
        if self.parent != None:
            return self._parent._get_pos_in_parent(self)
        return self.__object_pos
    
    @pos.setter
    def pos(self, value:vector2d):
        if self.parent != None and not self._parent._validate("move", self):
            return
        self.__place_object(value)
        if self.parent != None:
            self._parent._element_changed(self)
    
    @property
    def width(self)->int:
        return int(self.__dimensions.x)
    
    @width.setter
    def width(self, value:int):
        if self.parent != None and not self._parent._validate("width", self):
            return
        self.__dimensions.x = value
        self.__place_object()
        if self.parent != None:
            self._parent._element_changed(self)
    
    @property
    def height(self)->int:
        return int(self.__dimensions.y)
    
    @height.setter
    def height(self, value:int):
        if self.parent != None and not self._parent._validate("height", self):
            return
        self.__dimensions.y = value
        self.__place_object()
        if self.parent != None:
            self._parent._element_changed(self)
    
    @property
    def visible(self)->bool:
        return self.__visibility
    
    @visible.setter
    def visible(self, value:bool):
        if value:
            self.__visibility = True
            if self.parent != None and not self._parent._validate("visible", self):
                return
            self.__place_object()
            self._eventhandler("<Visible>")
        else:
            self.__visibility = False
            if self.parent != None and not self._parent._validate("visible", self):
                return
            self.object_id.place_forget()
            self._eventhandler("<Visible>")
        if self.parent != None:
            self._parent._element_changed(self)

    def move(self, mov_vec:vector2d):
        self.pos = self.__object_pos+mov_vec

    def __place_object(self, pos:vector2d|None=None, dim:vector2d|None=None):
        if pos == None:
            pos = self.__object_pos
        else:
            self.__object_pos = pos
        if dim == None:
            dim = self.__dimensions
        else:
            self.__dimensions = dim
        self.__container.place(x=pos.x + self.anchor.x, y=pos.y + self.anchor.y, width=dim.x, height=dim.y)
        #self.object_id.configure(width=dim.x,height=dim.y)
    
    def draw_rect(self, top_left:vector2d, bottom_right:vector2d, color:int):
        self.object_id.put("#%06x"%color,to=(int(top_left.x),int(top_left.y) , int(bottom_right.x),int(bottom_right.y)))
        self.__container.configure(image=self.object_id)
    
    def clear(self):
        self.object_id.blank()