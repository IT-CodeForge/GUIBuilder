from .ETKBaseWidget import ETKBaseWidget
from .ETKEdit import ETKEdit
from .vector2d import vector2d
from tkinter  import Message, Tk
from .Framework_utils import gen_col_from_int

class ETKLabel(ETKEdit):
    def __init__(self, myTk:Tk, txt:str="", pos_x:int=0, pos_y:int=0, width:int=80, height:int=17, fill:int=0xFFFFFF, text_col:int=0x0) -> None:
        super().__init__(myTk, txt, pos_x, pos_y, width, height, fill, text_col)
        self.object_id["state"] = "disabled"
    
    @property
    def enabled(self) -> bool:
        return True
    
    @enabled.setter
    def enabled(self, value: bool) -> bool:
        pass

