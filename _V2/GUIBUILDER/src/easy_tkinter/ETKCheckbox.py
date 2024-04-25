from typing       import Any, Callable
from enum         import Enum, auto
from .ETKBaseWidget import ETKBaseWidget
from .ETKBaseObject import BaseEvents
from .vector2d     import vector2d
from tkinter      import Event, IntVar, Tk, Checkbutton
from .Framework_utils import gen_col_from_int

class CheckboxEvents(Enum):
    CB_CHECKED   = auto()
    CB_UNCHECKED = auto()
    CB_TOGGLED   = auto()

class ETKCheckbox(ETKBaseWidget):
    def __init__(self, myTk:Tk, txt:str="", pos_x:int=0, pos_y:int=0, width:int=80, height:int=17, fill:int=0xEEEEEE, text_col:int=0x0) -> None:
        self.__state = IntVar()
        self.__bg_col = gen_col_from_int(fill)
        self.__text_col =gen_col_from_int(text_col)
        self.object_id:Checkbutton = Checkbutton(myTk, text=txt, bg=self.__bg_col, fg=self.__text_col, variable=self.__state)
        super().__init__(vector2d(pos_x, pos_y), vector2d(width, height))
        self.__event_funcs:dict[CheckboxEvents, Callable[...,None]] = {}
        self.__event_trans:dict[CheckboxEvents, str] = {
            CheckboxEvents.CB_CHECKED:"<ButtonPressed>",
            CheckboxEvents.CB_UNCHECKED:"<ButtonPressed>",
            CheckboxEvents.CB_TOGGLED:"<ButtonPressed>"
        }
        self.__event_truth_funcs:dict[CheckboxEvents, Callable[..., None]] = {
            CheckboxEvents.CB_CHECKED:lambda event, object_id : object_id.cget("state") == "normal",
            CheckboxEvents.CB_UNCHECKED:lambda event, object_id : object_id.cget("state") == "active",
            CheckboxEvents.CB_TOGGLED:lambda event, object_id : object_id.cget("state") != "disabled"
        }

    @property
    def state(self) -> bool:
        return bool(self.__state.get())

    @state.setter
    def state(self, value: bool):
        self.__state.set(value)

    @property
    def text(self)->str:
        return self.object_id.cget("text")
    
    @text.setter
    def text(self, value:str):
        self.object_id.config(text=value)
    
    def add_event(self, event_type: BaseEvents, eventhandler: Callable[..., None], truth_func:Callable[..., None]|None=None):
        if type(event_type) == CheckboxEvents:
            super().add_event(event_type, eventhandler, self.__event_trans[event_type], self.__event_truth_funcs[event_type])
        elif type(event_type) == BaseEvents:
            super().add_event(event_type, eventhandler)
        elif type(event_type) == str:
            super().add_event(event_type, eventhandler, truth_func=truth_func)
        else:
            #Raise Error
            pass    
    
    def remove_event(self, event_type: BaseEvents, eventhandler:Callable[..., None]):
        if type(event_type) == CheckboxEvents:
            super().remove_event(event_type, eventhandler, self.__event_trans[event_type])
        elif type(event_type) == BaseEvents:
            super().remove_event(event_type, eventhandler)
        else:
            #Raise Error
            pass 

#event routing functions       
    def __event(self, event:Event):
        checkbox_state = not self.__state.get() #needs to be inverted, since state update happens after event call
        if self.__event_funcs.get(CheckboxEvents.CB_TOGGLED, None) != None and self.object_id["state"] == "normal":
            super()._handle_event(self.__event_funcs[CheckboxEvents.CB_TOGGLED],CheckboxEvents.CB_TOGGLED,event)
        if checkbox_state and self.__event_funcs.get(CheckboxEvents.CB_CHECKED, None) != None and self.object_id["state"] == "normal":
            super()._handle_event(self.__event_funcs[CheckboxEvents.CB_CHECKED],CheckboxEvents.CB_CHECKED,event)
        if not checkbox_state and self.__event_funcs.get(CheckboxEvents.CB_UNCHECKED, None) != None and self.object_id["state"] == "normal":
            super()._handle_event(self.__event_funcs[CheckboxEvents.CB_UNCHECKED],CheckboxEvents.CB_UNCHECKED,event)