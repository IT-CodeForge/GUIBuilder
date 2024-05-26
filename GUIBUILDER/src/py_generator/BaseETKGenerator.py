from intermediary_neu.objects.IBaseObject import IBaseObject
from intermediary_neu.objects.IButton import IButton
from intermediary_neu.objects.ICheckbox import ICheckbox
from intermediary_neu.objects.IEdit import IEdit
from intermediary_neu.objects.ITimer import ITimer
from intermediary_neu.objects.IWindow import IWindow
#ILabe and ICanvas not needed, since they don't have events
from typing import Optional
from .BaseGenerator import BaseGenerator
from ast import stmt, Pass, FunctionDef
from . import ast_generator as ast_gen

class BaseETKGenerator(BaseGenerator):
    _EVENT_TRANS: dict[str, dict[type, str]] = {
        "event_create": {IWindow: "START"},
        "event_destroy": {IWindow: "EXIT"},
        "event_mouse_click": {IBaseObject: "MOUSE_DOWN"},
        "event_mouse_move": {IBaseObject: "MOUSE_MOVED"},
        "event_hovered": {IBaseObject: "ENTER"},
        "event_changed": {ICheckbox: "TOGGLED", IEdit: "CHANGED"},
        "event_pressed": {IButton: "PRESSED"}
    }

    def __init__(self) -> None:        
        super().__init__()
    
    @classmethod
    def _generate_event_list(cls, etk_objects: tuple[IBaseObject, ...]) -> list[tuple[IBaseObject, Optional[str], str]]:
        retval: list[tuple[IBaseObject, Optional[str], str]] = []
        # go throug every object
        for etk_object in etk_objects:
            if type(etk_object) == ITimer:
                retval.append((etk_object, None, "event_timer"))
            attributes = etk_object.ATTRIBUTES
            # go through the attributes of every object
            for attribute in attributes:
                # check if the attribut is an event
                if attribute.startswith("event_"):
                    # if the event is inactive skip said event
                    if not getattr(etk_object, attribute):
                        continue
                    intermediary_event = attribute
                    etk_events = cls._EVENT_TRANS.get(attribute)
                    # get the correct representation of the event in the ETK Framework
                    if etk_events is None:
                        continue
                    my_etk_event: Optional[str] = None
                    for etk_event in etk_events:
                        if etk_event == IBaseObject:
                            my_etk_event = etk_events.get(IBaseObject)
                        if etk_event == type(etk_object):
                            my_etk_event = etk_events.get(type(etk_object))
                    if my_etk_event is None:
                        continue
                    # add all the necessary information to the return list
                    retval.append(
                        (etk_object, my_etk_event, intermediary_event))

        return retval

    @classmethod
    def _generate_event_funcs(cls, event_list: list[tuple[IBaseObject, Optional[str], str]], previous_events: Optional[dict[str, list[stmt]]] = None) -> tuple[list[stmt], dict[str, list[stmt]]]:
        if previous_events is None:
            previous_events = {}
        retval: list[stmt] = []
        for etk_object, _, intermediary_event_type in event_list:
            my_function: FunctionDef = ast_gen.generate_event_definition( # type:ignore
                etk_object, intermediary_event_type)
            for previous_event in previous_events.keys():
                if cls.__compare_event_funcs(my_function.name, intermediary_event_type, previous_event):
                    my_function.body = previous_events.pop(previous_event, [Pass()])
                    break
            retval.append(my_function)
        return retval, previous_events
    
    @staticmethod
    def __compare_event_funcs(generated_func_name: str, generated_intermediary_event: str, read_func_name: str) -> bool:
        if generated_func_name[0] != "e":
            raise ValueError("the event function was not generated correctly, missing e in the beginning")
        if read_func_name[0] != "e" or read_func_name.count("_") < 2:
            return False
        generated_func_id: int = int(generated_func_name[1:generated_func_name.find("_")])
        read_func_id: int = int(read_func_name[1:read_func_name.find("_")])
        if generated_func_id == read_func_id and read_func_name.endswith(generated_intermediary_event):
            return True
        else:
            return False