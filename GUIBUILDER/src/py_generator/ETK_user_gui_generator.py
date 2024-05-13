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
from .BaseETKGenerator import BaseETKGenerator

class ETK_user_gui_generator:
    def __init__(self) -> None:
        super().__init__()

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
                                  str]] = self._generate_event_list(etk_objects)
        
        previous_functions: dict[str, list[stmt]] = self.__generate_previous_funcs_dict(ast_old_file)
        
        my_event_funcs, removed_events = self._generate_event_funcs(my_event_list, previous_functions)

        for ast_object in template.body:
            if type(ast_object) == ClassDef and ast_object.name == "UserGUI":
                ast_object.body += my_event_funcs
                break
        else:
            raise ValueError("Somebody deleted the UserGui class")

        ast_removed_events = self.__removed_events_dict_to_ast(removed_events, ast_old_file)

        code: str = to_source(template)
        return code, to_source(ast_removed_events)

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