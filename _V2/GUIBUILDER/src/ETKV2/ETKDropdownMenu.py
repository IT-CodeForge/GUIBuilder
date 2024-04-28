from ETKV2.vector2d import vector2d
from .Internal.ETKBaseTkWidgetDisableable import ETKBaseTkWidgetDisableable
from .Internal.ETKBaseObject import ETKEvents
from enum import auto
from tkinter import OptionMenu, StringVar, Tk

class ETKDropdownMenuEvents(ETKEvents):
    CHANGED = ("<Custom>",auto())

class ETKDropdownMenu(ETKBaseTkWidgetDisableable):
    def __init__(self, tk: Tk, options:list[str], start_value: str = "", pos: vector2d = vector2d(0, 0), size: vector2d = vector2d(70, 18), background_color: int = 0xEEEEEE) -> None:
        self.__selected = StringVar(value=start_value)
        self.__selected.trace("w", self.__clicked_changed) #type:ignore
        self._tk_object = OptionMenu(tk, self.__selected, *options)
        ETKBaseTkWidgetDisableable.__init__(self, pos, size, background_color)
        self._event_lib.update({e: [] for e in ETKDropdownMenuEvents})
    
    @property
    def selected(self)->str:
        """READ-Only"""
        return self.__selected.get()
    
    def __clicked_changed(self)->None:
        self._handle_event(ETKDropdownMenuEvents.CHANGED)