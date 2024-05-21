from .BaseTGWGenerator import BaseTGWGenerator
from intermediary_neu.objects.IBaseObject import IBaseObject
from intermediary_neu.objects.IButton import IButton
from intermediary_neu.objects.ICanvas import ICanvas
from intermediary_neu.objects.ICheckbox import ICheckbox
from intermediary_neu.objects.IEdit import IEdit
from intermediary_neu.objects.ILabel import ILabel
from intermediary_neu.objects.ITimer import ITimer
from intermediary_neu.objects.IWindow import IWindow
from . import TGW_code_generator  as tgw_gen
from typing import Callable, Any

class TGW_system_generator(BaseTGWGenerator):
    __GENERATOR_TRANS: dict[type, Callable[[Any], str]] = {
        IButton: tgw_gen.button,
        ICanvas: tgw_gen.canvas,
        ICheckbox: tgw_gen.checkbox,
        IEdit: tgw_gen.edit,
        ILabel: tgw_gen.label
    }

    def __init__(self) -> None:
        super().__init__()
    
    def generate_file(self, tgw_objects: tuple[IBaseObject, ...])-> tuple[str, str, str]:
        gui_params: str = ""
        for tgw_object in tgw_objects:
            if type(tgw_object) == IWindow:
                gui_params = tgw_gen.window_params(tgw_object)
        constructor_definition: str = ""
        for tgw_object in tgw_objects:
            constructor_definition += self._INDENT + self.__GENERATOR_TRANS.get(type(tgw_object), lambda obj : "")(tgw_object)
            if type(tgw_object) == ICanvas:
                constructor_definition += self._INDENT + tgw_gen.get_object_name(tgw_object) + " = " + tgw_gen.get_object_name(tgw_object) + "_bitmap->canvas"
        constructor_definition += self._INDENT + "on_construction();\r\n"
        event_funcs: str = self.__generate_event_funcs_definition(tgw_objects)
        return gui_params, constructor_definition, event_funcs
    
    @classmethod
    def __generate_event_funcs_definition(cls, tgw_objects: tuple[IBaseObject, ...]) -> str:
        retval: str = ""
        event_dict: dict[str, list[tuple[IBaseObject, str]]] = cls._generate_event_dict(tgw_objects)
        for tgw_event in event_dict.keys():
            if tgw_event != "timer_funcs":
                retval += cls._INDENT + "void GUI::" + tgw_gen.generate_event_head_tgw(tgw_event, event_dict[tgw_event][0][0]) + ";\r\n"
            else:
                retval += cls._INDENT + "void GUI::eventTimer(int id);\r\n"
            retval += "{\r\n"
            for tgw_object, event_type in event_dict.get(tgw_event, []):
                retval += cls.__generate_event_bind(tgw_object, event_type)
            retval += "}\r\n\r\n"
        return retval
    
    @classmethod
    def __generate_event_bind(cls, tgw_object: IBaseObject, event_type: str)-> str:
        retval: str = ""
        content: str = tgw_gen.generate_event_head_own(event_type, tgw_object).replace("int ", "").replace("HDC ", "").replace("TGWindow* ", "")
        if type(tgw_object) == IWindow:
            retval += cls._INDENT + content + ";\r\n"
        else:
            condition: str = ""
            if type(tgw_object) == ITimer:
                condition = f"id == {tgw_gen.get_object_name(tgw_object)}id && {tgw_gen.get_object_name(tgw_object)}IsEnabled == true"
            elif type(tgw_object) == ICheckbox:
                condition = f"eineCheckBox == this->{tgw_gen.get_object_name(tgw_object)}"
            elif type(tgw_object) in [IEdit, IButton]:
                condition = f"ein{str(type(tgw_object))[1:]} == this->{tgw_gen.get_object_name(tgw_object)}"
            retval = tgw_gen.generate_if_clause(condition, content, cls._INDENT, 1)
        return retval
    
