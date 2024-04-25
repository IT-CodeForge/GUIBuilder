from abc import abstractmethod
from typing import Any, Callable
from enum         import Enum, auto
from .ETKBaseWidget import ETKBaseWidget
from .ETKBaseObject import BaseEvents
from .vector2d     import vector2d
from tkinter      import Button, Event, Tk
from .Framework_utils import gen_col_from_int

class ButtonEvents(Enum):
    BTN_PRESSED        = auto()
    BTN_RELEASED       = auto()

class ETKButton(ETKBaseWidget):
    def __init__(self, myTk:Tk, txt:str="", pos_x:int=0, pos_y:int=0, width:int=80, height:int=17, fill:int=0xEEEEEE, text_col:int=0x0) -> None:
        self.__bg_col = gen_col_from_int(fill)
        self.__text_col = gen_col_from_int(text_col)
        self.object_id:Button = Button(myTk, text=txt, bg=self.__bg_col, fg=self.__text_col)
        super().__init__(vector2d(pos_x, pos_y), vector2d(width, height))
        self.__event_trans:dict[ButtonEvents, str] = {
            ButtonEvents.BTN_PRESSED:"<ButtonPress>",
            ButtonEvents.BTN_RELEASED:"<ButtonRelease>"
        }
        self.__event_truth_funcs:dict[ButtonEvents, str] = {
            ButtonEvents.BTN_PRESSED:lambda event, object_id: object_id.cget("state") != "disabled",
            ButtonEvents.BTN_RELEASED:lambda event, object_id: object_id.cget("state") != "disabled"
        }

    @property
    def text(self)->str:
        return self.object_id.cget("text")
    
    @text.setter
    def text(self, value:str):
        self.object_id.config(text=value)
    
    def add_event(self, event_type: BaseEvents, eventhandler: Callable[..., None], truth_func:Callable[..., None]|None=None):
        if type(event_type) == ButtonEvents:
            super().add_event(event_type, eventhandler, self.__event_trans[event_type], self.__event_truth_funcs[event_type])
        elif type(event_type) == BaseEvents:
            super().add_event(event_type, eventhandler)
        elif type(event_type) == str:
            super().add_event(event_type, eventhandler, truth_func=truth_func)
        else:
            #Raise Error
            pass  
    
    def remove_event(self, event_type: BaseEvents, eventhandler:Callable[..., None]):
        if type(event_type) == ButtonEvents:
            super().remove_event(event_type, eventhandler, self.__event_trans[event_type])
        elif type(event_type) == BaseEvents or event_type == "<Custom>":
            super().remove_event(event_type, eventhandler)
        else:
            #Raise Error
            pass