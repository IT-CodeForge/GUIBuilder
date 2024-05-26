from intermediary_neu.objects.IBaseObject import IBaseObject
from intermediary_neu.objects.IButton import IButton
from intermediary_neu.objects.ICanvas import ICanvas
from intermediary_neu.objects.ICheckbox import ICheckbox
from intermediary_neu.objects.IEdit import IEdit
from intermediary_neu.objects.ILabel import ILabel
from intermediary_neu.objects.ITimer import ITimer
from intermediary_neu.objects.IWindow import IWindow
from ast import ClassDef, Module, stmt, FunctionDef, parse
from astor import to_source  # type:ignore
from typing import Optional, Callable, Any
from . import ast_generator as ast_gen
from .BaseETKGenerator import BaseETKGenerator


class ETK_system_gui_generator(BaseETKGenerator):
    __GENERATOR_TRANS: dict[type, Callable[[Any], stmt]] = {
        IButton: ast_gen.button,
        ICanvas: ast_gen.canvas,
        ICheckbox: ast_gen.checkbox,
        IEdit: ast_gen.edit,
        ILabel: ast_gen.label
    }
    
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def generate_file(cls, etk_objects: tuple[IBaseObject, ...]) -> str:
        template: Module
        template = parse(cls._read_file(cls._join_relative_path("./templates/ETKgenerator/SystemGUI.txt")))
        
        for e in template.body:
            if type(e) == ClassDef and e.name == "SystemGUI":
                template_class = e

        my_class_body: list[stmt] = template_class.body  # type:ignore

        my_event_list: list[tuple[IBaseObject, Optional[str],
                                  str]] = cls._generate_event_list(etk_objects)

        for ast_object in my_class_body:  # type:ignore
            if type(ast_object) == FunctionDef:  # type:ignore
                if ast_object.name == "__init__":
                    ast_object.body = [cls.__generate_init_body(etk_objects)]
                if ast_object.name == "_add_elements":
                    ast_object.body = cls.__generate_attribute_creation(
                        etk_objects) + cls.__generate_event_binds(my_event_list)

        my_class_body += cls._generate_event_funcs(my_event_list)[0] 

        template_class.body = my_class_body  # type:ignore

        code: str = to_source(template)

        return code

    @staticmethod
    def __generate_init_body(etk_objects: tuple[IBaseObject, ...]) -> stmt:
        for etk_object in etk_objects:
            if type(etk_object) == IWindow:
                return ast_gen.generate_gui_init(etk_object)
        raise ValueError("List of baseobjects, doesn't contain Mainwindow")

    @classmethod
    def __generate_attribute_creation(cls, etk_objects: tuple[IBaseObject, ...]) -> list[stmt]:
        retval: list[stmt] = []
        for etk_object in etk_objects:
            if type(etk_object) == IWindow:
                continue
            if type(etk_object) == ITimer:
                retval.append(ast_gen.timer(etk_object, "event_timer"))
                continue
            my_func = cls.__GENERATOR_TRANS.get(type(etk_object))
            if my_func is None:
                continue
            retval.append(my_func(etk_object))
        return retval

    @classmethod
    def __generate_event_binds(cls, event_list: list[tuple[IBaseObject, Optional[str], str]]) -> list[stmt]:
        retval: list[stmt] = []
        for etk_object, etk_event_typ, intermediary_event_type in event_list:
            if etk_event_typ is None:
                continue
            etk_event_typ = "ETK" + str(type(etk_object).__name__)[1:] + "Events." + etk_event_typ
            retval.append(ast_gen.generate_event_bind(
                etk_object, etk_event_typ, intermediary_event_type))
        return retval