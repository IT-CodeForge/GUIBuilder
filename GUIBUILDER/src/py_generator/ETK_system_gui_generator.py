from intermediary_neu.objects.IBaseObject import IBaseObject
from intermediary_neu.objects.IButton import IButton
from intermediary_neu.objects.ICanvas import ICanvas
from intermediary_neu.objects.ICheckbox import ICheckbox
from intermediary_neu.objects.IEdit import IEdit
from intermediary_neu.objects.ILabel import ILabel
from intermediary_neu.objects.ITimer import ITimer
from intermediary_neu.objects.IWindow import IWindow
from ast import Module, stmt, FunctionDef, Name, Load, parse
from astor import to_source  # type:ignore
from typing import Optional, Callable, Any
import os
from . import ast_generator as ast_gen


class ETK_system_gui_generator:
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

    def generate_file(self, etk_objects: tuple[IBaseObject, ...]) -> str:
        template: Module
        with open(self.__join_relative_path("./templates/generator/SystemGUI.txt"), "r") as f:
            template = parse(f.read())

        my_class_body: list[stmt] = template.body[0].body  # type:ignore

        my_event_list: list[tuple[IBaseObject, Optional[str],
                                  str]] = self.__generate_event_list(etk_objects)

        for ast_object in my_class_body:  # type:ignore
            if type(ast_object) == FunctionDef:  # type:ignore
                if ast_object.name == "__init__":
                    ast_object.body = [self.__generate_init_body(etk_objects)]
                if ast_object.name == "_add_elements":
                    ast_object.body = self.__generate_attribute_creation(
                        etk_objects) + self.__generate_event_binds(my_event_list)

        my_class_body += self.__generate_event_funcs(my_event_list) # type:ignore

        template.body[0].body = my_class_body  # type:ignore

        code: str = to_source(template)

        return code

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
                    if not attributes.get(attribute, False):
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

    def __generate_init_body(self, etk_objects: tuple[IBaseObject, ...]) -> stmt:
        for etk_object in etk_objects:
            if type(etk_object) == IWindow:
                return ast_gen.generate_gui_init(etk_object)
        raise ValueError("List of baseobjects, doesn't contain Mainwindow")

    def __generate_event_funcs(self, event_list: list[tuple[IBaseObject, Optional[str], str]]) -> list[stmt]:
        retval: list[stmt] = []
        for etk_object, _, intermediary_event_type in event_list:
            my_function: FunctionDef = ast_gen.generate_event_definition( # type:ignore
                etk_object, intermediary_event_type)
            my_function.decorator_list = [ 
                Name(id='abstractmethod', ctx=Load())]  
            retval.append(my_function)
        return retval

    def __generate_attribute_creation(self, etk_objects: tuple[IBaseObject, ...]) -> list[stmt]:
        retval: list[stmt] = []
        for etk_object in etk_objects:
            if type(etk_object) == IWindow:
                continue
            if type(etk_object) == ITimer:
                retval.append(ast_gen.timer(etk_object, "event_timer"))
                continue
            my_func = self.__generator_trans.get(type(etk_object))
            if my_func == None:
                continue
            retval.append(my_func(etk_object))
        return retval

    def __generate_event_binds(self, event_list: list[tuple[IBaseObject, Optional[str], str]]) -> list[stmt]:
        retval: list[stmt] = []
        for etk_object, etk_event_typ, intermediary_event_type in event_list:
            etk_event_enum: str = ""
            if IBaseObject in self.__event_trans.get(intermediary_event_type, {}).keys():
                etk_event_enum = "Base"
            elif self.__event_trans.get(intermediary_event_type, {}) != {}:
                etk_event_enum = str(type(etk_object).__name__)[1:]
            else:
                raise ValueError("incompatible event list")
            if etk_event_typ == None:
                continue
            etk_event_typ = "ETK" + etk_event_enum + "Events." + etk_event_typ
            retval.append(ast_gen.generate_event_bind(
                etk_object, etk_event_typ, intermediary_event_type))
        return retval

    def __join_relative_path(self, relative_path: str) -> str:
        return os.path.join(os.path.split(__file__)[0], relative_path)
