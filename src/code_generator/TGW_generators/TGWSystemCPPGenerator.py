from .BaseTGWGenerator import BaseTGWGenerator
from intermediary.objects.IBaseObject import IBaseObject
from intermediary.objects.IButton import IButton
from intermediary.objects.ICanvas import ICanvas
from intermediary.objects.ICheckbox import ICheckbox
from intermediary.objects.IEdit import IEdit
from intermediary.objects.ILabel import ILabel
from intermediary.objects.ITimer import ITimer
from intermediary.objects.IWindow import IWindow
from . import TGWCodeGenerator  as tgw_gen
from typing import Callable, Any

"""
the SystemGUI generator generates a cpp file which links the default tgw-events to the GUI-Builder events
and the definition of the Constructor (to generate the GUI-elements)
"""

class TGWSystemCPPGenerator(BaseTGWGenerator):
    __GENERATOR_TRANS: dict[type, Callable[[Any], str]] = {
        IButton: tgw_gen.button,
        ICanvas: tgw_gen.canvas,
        ICheckbox: tgw_gen.checkbox,
        IEdit: tgw_gen.edit,
        ILabel: tgw_gen.label,
        ITimer: tgw_gen.timer
    }

    def __init__(self) -> None:
        super().__init__()
    
    @classmethod
    def generate_file(cls, tgw_objects: tuple[IBaseObject, ...])-> tuple[str, str, str]:
        """
        this returns three strings.
        the first string replaces the #tag:main_window_params#in the SystemGUI template
        the second string replaces the #tag:constructor_definition# in the SystemGUI template
        the third string replaces the #tag:event_funcs_definition# in the SystemGUI template
        """
        gui_params: str = ""
        for tgw_object in tgw_objects: #searches for the Window in the list and use it to generate the GUI params
            if type(tgw_object) == IWindow:
                gui_params = tgw_gen.window_params(tgw_object)
        constructor_definition: str = ""
        for tgw_object in tgw_objects: #goes over all objects and generates the assignement of values for every object where this is necessary (keep in mind the Timer attributes are assigned in the header)
            if type(tgw_object) == IWindow:
                continue
            constructor_definition += cls._INDENT + cls.__GENERATOR_TRANS.get(type(tgw_object), lambda obj : "")(tgw_object) + ";\n" #the "lmabda obj : """ is necessery since strict typeng gets upset because it doesn't know that the tgw-objects can only be of the types that are specified in the dict hence it says None types are not callable
            if type(tgw_object) == ICanvas:
                constructor_definition += cls._INDENT + tgw_gen.get_object_name(tgw_object) + " = " + tgw_gen.get_object_name(tgw_object) + "_bitmap->canvas;\n"
        event_funcs: str = cls.__generate_event_funcs_definition(tgw_objects)
        return gui_params, constructor_definition, event_funcs
    
    @classmethod
    def __generate_event_funcs_definition(cls, tgw_objects: tuple[IBaseObject, ...]) -> str:
        """
        generates the function definitions.
        Here they are needed, to connect the the TGW functions with the custom generated ones
        (e.g. we have a button called "btn" with the id 2, and we want a pressed event so this generates:
        void SystemGUI::eventButton(TGWButton* einButton, int event)
        {
          if(einButton == this->e2_btn)
          {
            e2_btn_event_pressed();
          }
        }
        )
        """
        retval: str = ""
        event_dict: dict[str, list[tuple[IBaseObject, str]]] = cls._generate_event_dict(tgw_objects)
        for tgw_event in event_dict.keys():
            if tgw_event != "timer_funcs":
                retval += "void SystemGUI::" + tgw_gen.generate_event_head_tgw(tgw_event) + "\n"
            else:
                retval += "void SystemGUI::eventTimer(int id)\n"
            retval += "{\n"
            for tgw_object, event_type in event_dict.get(tgw_event, []):
                retval += cls.__generate_event_bind(tgw_object, event_type)
            retval += "}\n\n"
        return retval
    
    @classmethod
    def __generate_event_bind(cls, tgw_object: IBaseObject, event_type: str)-> str:
        """
        this generates the code insed of the curly brackets of the TGW-event functions (in the previous example it would be the if-clause)
        """
        retval: str = ""
        content: str = tgw_gen.generate_event_head_own(event_type, tgw_object).replace("int ", "").replace("HDC ", "").replace("TGWindow* ", "") + ";\n"
        if type(tgw_object) == IWindow:
            retval += cls._INDENT + content
        else:
            condition: str = ""
            if type(tgw_object) == ITimer:
                condition = f"id == {tgw_gen.get_object_name(tgw_object)}_id && {tgw_gen.get_object_name(tgw_object)}IsEnabled == true"
            elif type(tgw_object) == ICheckbox:
                condition = f"eineCheckBox == this->{tgw_gen.get_object_name(tgw_object)}"
            elif type(tgw_object) in [IEdit, IButton]:
                condition = f"ein{type(tgw_object).__name__[1:]} == this->{tgw_gen.get_object_name(tgw_object)}"
            if type(tgw_object) == IButton and event_type == "button_double_pressed":
                condition += " && event == 1"
            retval = tgw_gen.generate_if_clause(condition, content, cls._INDENT, 1)
        return retval
    
