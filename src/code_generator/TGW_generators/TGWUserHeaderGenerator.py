from .BaseTGWGenerator import BaseTGWGenerator
from intermediary.objects.IBaseObject import IBaseObject
from intermediary.objects.ITimer import ITimer
from . import TGWCodeGenerator as tgw_gen

class TGWUserHeaderGenerator(BaseTGWGenerator):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def generate_file(cls, tgw_objects: tuple[IBaseObject, ...]) ->str:
        template: str = cls._read_file(cls._join_relative_path("./templates/TGWgenerator/UserHeaderGUI.txt"))
        retval = template.replace("#tag:function_declarations#", cls.__generate_event_funcs(tgw_objects))
        return retval
    
    @classmethod
    def __generate_event_funcs(cls, tgw_objects: tuple[IBaseObject, ...]) -> str:
        """
        generates the declarations of the event functions.
        this means, it generates all of the standard TGWEvent Functions, that get called by the framework
        and the functions the get called by the system GUI to make the more user friendly
        (which means to get the "pressed" event from a certain button, you dont need to check the ID given by the tgw event function but instead get a different function for every button)
        """
        retval: str = ""
        event_dict: dict[str, list[tuple[IBaseObject, str]]] = cls._generate_event_dict(tgw_objects)
        for tgw_event in event_dict.keys():
            for tgw_object, event_type in event_dict.get(tgw_event, []):
                if type(tgw_object) == ITimer:
                    retval += cls._INDENT + "void " + tgw_gen.get_event_func_own_name(event_type, tgw_object) + "();\n"
                else:
                    retval += cls._INDENT + "void " + tgw_gen.generate_event_head_own(event_type, tgw_object) + ";\n"
        return retval