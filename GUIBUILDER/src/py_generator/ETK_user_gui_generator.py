from intermediary_neu.objects.IBaseObject import IBaseObject
from intermediary_neu.objects.IButton import IButton
from intermediary_neu.objects.ICanvas import ICanvas
from intermediary_neu.objects.ICheckbox import ICheckbox
from intermediary_neu.objects.IEdit import IEdit
from intermediary_neu.objects.ILabel import ILabel
from intermediary_neu.objects.ITimer import ITimer
from intermediary_neu.objects.IWindow import IWindow
from ast import Module, stmt, FunctionDef, ClassDef, Pass, parse
from astor import to_source  # type:ignore
from typing import Optional, Callable, Any
import os
from . import ast_generator as ast_gen

class ETK_user_gui_generator:
    def __init__(self) -> None:
        self.__event_trans: dict[str, dict[type, str]] = {
            "event_create": {IWindow: "START"},
            "event_destroy": {IWindow: "EXIT"},
            "event_mouse_click": {IBaseObject: "MOUSE_DOWN"},
            "event_mouse_move": {IBaseObject: "MOUSE_MOVED"},
            "event_hovered": {IBaseObject: "ENTER"},
            "event_changed": {ICheckbox: "TOGGLED", IEdit: "CHANGED"},
            "event_pressed": {IButton: "PRESSED"}
        }
        self.__generator_trans: dict[type, Callable[[Any], stmt]] = {
            IButton: ast_gen.button,
            ICanvas: ast_gen.canvas,
            ICheckbox: ast_gen.checkbox,
            IEdit: ast_gen.edit,
            ILabel: ast_gen.label
        }

    def generate_file(self, etk_objects: tuple[IBaseObject, ...], old_file:Optional[str]) -> tuple[str, str]:
        template: Module
        with open(self.__join_relative_path("./templates/generator/UserGUI.txt"), "r") as f:
            template = parse(f.read())

        ast_old_file: Optional[Module] = None
        if old_file != None:
            ast_old_file = parse(old_file)
            for ast_object  in ast_old_file.body:
                if not (type(ast_object) == ClassDef and ast_object.name == "UserGUI"):
                    continue
                for class_object in ast_object.body:
                    if not (type(class_object) == FunctionDef and class_object.name == "_on_init"):
                        continue
                    for ast_object2 in template.body:
                        if type(ast_object2) == ClassDef:
                            ast_object2.body[0].body = class_object.body # type:ignore
                            break
                    else:
                        raise ValueError("Somebody deleted the UserGui class")
                    break
                break
        
        my_event_list: list[tuple[IBaseObject, Optional[str],
                                  str]] = self.__generate_event_list(etk_objects)
        
        previous_functions: dict[str, list[stmt]] = self.__generate_previous_funcs_dict(ast_old_file)
        
        my_event_funcs, removed_events = self.__generate_event_funcs(my_event_list, previous_functions)

        for ast_object in template.body:
            if type(ast_object) == ClassDef and ast_object.name == "UserGUI":
                ast_object.body += my_event_funcs
                break
        else:
            raise ValueError("Somebody deleted the UserGui class")

        ast_removed_events = self.__removed_events_dict_to_ast(removed_events, ast_old_file)

        code: str = to_source(template)
        return code, to_source(ast_removed_events)
    
    def __generate_event_list(self, etk_objects: tuple[IBaseObject, ...]) -> list[tuple[IBaseObject, Optional[str], str]]:
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
                    etk_events = self.__event_trans.get(attribute)
                    # get the correct representation of the event in the ETK Framework
                    if etk_events == None:
                        continue
                    my_etk_event: Optional[str] = None
                    for etk_event in etk_events:
                        if etk_event == IBaseObject:
                            my_etk_event = etk_events.get(IBaseObject)
                        if etk_event == type(etk_object):
                            my_etk_event = etk_events.get(type(etk_object))
                    if my_etk_event == None:
                        continue
                    # add all the necessary information to the return list
                    retval.append(
                        (etk_object, my_etk_event, intermediary_event))

        return retval
    
    def __generate_event_funcs(self, event_list: list[tuple[IBaseObject, Optional[str], str]], previous_events: dict[str, list[stmt]]) -> tuple[list[stmt], dict[str, list[stmt]]]:
        retval: list[stmt] = []
        for etk_object, _, intermediary_event_type in event_list:
            my_function: FunctionDef = ast_gen.generate_event_definition( # type:ignore
                etk_object, intermediary_event_type)
            for previous_event in previous_events.keys():
                if self.__compare_event_funcs(my_function.name, intermediary_event_type, previous_event):
                    my_function.body = previous_events.pop(previous_event, [Pass()])
                    break
            retval.append(my_function)
        return retval, previous_events
    
    def __compare_event_funcs(self, generated_func_name: str, generated_intermediary_event: str, read_func_name: str) -> bool:
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

    def __generate_previous_funcs_dict(self, ast_old_file: Optional[Module]) -> dict[str, list[stmt]]:
        retval: dict[str, list[stmt]] = {}
        if ast_old_file == None:
            return retval
        for ast_object in ast_old_file.body:
            if type(ast_object) == ClassDef and ast_object.name == "UserGUI":
                for class_object in ast_object.body:
                    if type(class_object) == FunctionDef:
                        if class_object.name == "_on_init":
                            continue
                        if len(class_object.body) == 0:
                            continue
                        if len(class_object.body) == 1 and type(class_object.body[0]) == Pass:
                            continue
                        retval[class_object.name] = class_object.body
                return retval
        else:
            raise ValueError("Somebody deleted the UserGui class")
    
    def __removed_events_dict_to_ast(self, removed_events: dict[str, list[stmt]], ast_old_file: Optional[Module]) -> Module:
        retval: Module = Module()
        retval.body = []
        if ast_old_file == None:
            return retval
        for ast_object in ast_old_file.body:
            if type(ast_object) == ClassDef and ast_object.name == "UserGUI":
                for class_object in ast_object.body:
                    if type(class_object) == FunctionDef and class_object.name in removed_events.keys():
                        retval.body.append(class_object)
                return retval
        else:
            raise ValueError("Somebody deleted the UserGui class")
        
    
    def __join_relative_path(self, relative_path: str) -> str:
        return os.path.abspath(os.path.join(os.path.split(__file__)[0], relative_path))