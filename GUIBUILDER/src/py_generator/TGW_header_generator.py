from .BaseTGWGenerator import BaseTGWGenerator
from intermediary_neu.objects.IBaseObject import IBaseObject
from intermediary_neu.objects.ITimer import ITimer
from intermediary_neu.objects.ICanvas import ICanvas
from intermediary_neu.objects.IWindow import IWindow
from . import TGW_code_generator as tgw_gen

class TGW_header_generator(BaseTGWGenerator):
    def __init__(self) -> None:
        super().__init__()
    
    def generate_file(self, tgw_objects: tuple[IBaseObject, ...]) ->tuple[str, str]:
        attributes: str = self.__generate_attributes(tgw_objects)
        event_funcs: str = self.__generate_event_funcs(tgw_objects)
        return attributes, event_funcs
    
    @classmethod
    def __generate_attributes(cls, tgw_objects: tuple[IBaseObject, ...]) -> str:
        retval: str = ""
        for tgw_object in tgw_objects:
            if type(tgw_object) not in [IWindow, ICanvas]:
                retval += cls._INDENT + tgw_gen.TYPE_TRANS.get(type(tgw_object), "") + "* " + tgw_gen.get_object_name(tgw_object) + ";\n"
            if type(tgw_object) == ITimer:
                retval += cls._INDENT + "int " + tgw_gen.get_object_name(tgw_object) + "_id = " + str(tgw_object.id) + ";\n"
                retval += cls._INDENT + "bool " + tgw_gen.get_object_name(tgw_object) + "IsEnabled = " + str(tgw_object.enabled).lower() + ";\n"
            if type(tgw_object) == ICanvas:
                retval += cls._INDENT + "TGWCanvas* " + tgw_gen.get_object_name(tgw_object) + ";\n"
                retval += cls._INDENT + tgw_gen.TYPE_TRANS.get(type(tgw_object), "") + "* " + tgw_gen.get_object_name(tgw_object) + "_bitmap;\n"
        return retval
    
    @classmethod
    def __generate_event_funcs(cls, tgw_objects: tuple[IBaseObject, ...]) -> str:
        retval: str = cls._INDENT + "void on_construction();\n"
        event_dict: dict[str, list[tuple[IBaseObject, str]]] = cls._generate_event_dict(tgw_objects)
        for tgw_event in event_dict.keys():
            if tgw_event != "timer_funcs":
                retval += cls._INDENT + "void " + tgw_gen.generate_event_head_tgw(tgw_event) + ";\n"
            else:
                retval += cls._INDENT + "void eventTimer(int id);\n"
            for tgw_object, event_type in event_dict.get(tgw_event, []):
                if type(tgw_object) == ITimer:
                    retval += cls._INDENT + "void " + tgw_gen.get_event_func_own_name(event_type, tgw_object) + "();\n"
                    continue
                retval += cls._INDENT + "void " + tgw_gen.generate_event_head_own(event_type, tgw_object) + ";\n"
        return retval