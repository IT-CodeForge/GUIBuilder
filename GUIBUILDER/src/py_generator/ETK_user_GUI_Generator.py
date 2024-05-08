from typing import Optional,Any
from ..intermediary_neu.objects.IBaseObject import IBaseObject
from ..intermediary_neu.objects.IButton import IButton
from ..intermediary_neu.objects.ICanvas import ICanvas
from ..intermediary_neu.objects.ICheckbox import ICheckbox
from ..intermediary_neu.objects.IEdit import IEdit
from ..intermediary_neu.objects.ILabel import ILabel
from ..intermediary_neu.objects.ITimer import ITimer
from ..intermediary_neu.objects.IWindow import IWindow

class ETK_user_GUI_Generator:
    def __init__(self) -> None:
        self.__indent: str = "    "
        self.__user_gui: list[str] = []
        with open("./static_template.py", "r") as file:
            self.__user_gui = file.readlines()
        pass


#use template and add all the user inputs to sid template (oldfile should instead be list of lines)
    def write_file(self, objects: list[IBaseObject], old_file: list[str]):
        event_func_list: list[str] = []
        for gui_object in objects:
            event_func_list += self.__generate_event_funcs(gui_object)
            pass

        function_indeces: list[int] = []
        for event_func in event_func_list:
            for index, line in enumerate(old_file):
                if line.startswith(event_func):
                    function_indeces.append(index)
                    pass
                pass
            pass

        function_ends: list[int] = []
        for index in function_indeces:
            function_ends.append(self.__find_end_of_func(index, old_file))
        #imports, old_file = self.__refresh_imports(old_file)
        #old_file = self.__readd_essentials(old_file)

        #return imports + "\r\n" + old_file
        return
    
    #new generate event funcs
    def __generate_event_funcs(self, gui_object: IBaseObject)->list[str]:
        retlist: list[str] = []
        for key in gui_object.ATTRIBUTES:
            if key.startswith("event_") and gui_object.__getattribute__(key):
                func: str = self.__generate_event_handler(gui_object.name, key.removeprefix("event_"))
                retlist.append(func)
        return retlist
    
    def __find_end_of_func(self, func_index: int, file: list[str])->int:
        file_from_func_on = file[func_index + 1:]
        for index, line in enumerate(file_from_func_on):
            if not line.startswith("        "):
                return func_index + index
        return len(file) - 1

    """
    def __generate_event_funcs(self, gui_object: Any)->str:
        object_name: str = gui_object.name
        eventhandler: str = ""
        if type(gui_object) == ITimer:
            return ""
        if type(gui_object) == IWindow:
            #resize and paint event missing
            if gui_object.event_create:
                eventhandler += self.__indent + self.__generate_event_handler(object_name, "create") + "\n\r" + self.__indent + "   pass"
            if gui_object.event_destroy:
                eventhandler += self.__indent + self.__generate_event_handler(object_name, "destroy") + "\n\r" + self.__indent + "   pass"
            if gui_object.event_mouse_click:
                eventhandler += self.__indent + self.__generate_event_handler(object_name, "mouse_click") + "\n\r" + self.__indent + "   pass"
            if gui_object.event_mouse_move:
                eventhandler += self.__indent + self.__generate_event_handler(object_name, "mouse_move") + "\n\r" + self.__indent + "   pass"
            return eventhandler
        if gui_object.event_hovered:
            eventhandler += self.__generate_event_handler(object_name, "hovered") + "\n\r" + self.__indent + "   pass"
        if type(gui_object) == IEdit:
            if gui_object.event_changed:
                eventhandler += self.__indent + self.__generate_event_handler(object_name, "changed") + "\n\r" + self.__indent + "   pass"
        if type(gui_object) == ICheckbox:
            if gui_object.event_changed:
                eventhandler += self.__indent + self.__generate_event_handler(object_name, "changed") + "\n\r" + self.__indent + "   pass"
        if type(gui_object) == IButton:
            #doubble pressed event missing
            if gui_object. event_pressed:
                eventhandler += self.__indent + self.__generate_event_handler(object_name, "pressed") + "\n\r" + self.__indent + "   pass"
        return eventhandler
    """
    def __generate_event_handler(self, object_name:str, event_type: str):
        return "    self._ev_" + event_type + "_" + object_name + "(self, params: tuple[BaseObject, Events, Event])"

#maybe not needed
    def __readd_essentials(self, file: str)->str:
        if file.find("class GUI(static_GUI):") == -1 or file.find("def _on_init(self)->None:") == -1:
            file = """
class GUI(static_GUI):
    def _on_init(self)->None:
        pass"""
        return file

    def __refresh_imports(self, file: str)->tuple[str, str]:
        while file.find("from") != -1:
            string_holder: str = file[file.find("from"):]
            file = file[file.find("from") + string_holder.find("\n"):]
        imports: str = "from static_GUI import static_GUI\r\n" + "from ETK import *\r\n"
        return (imports, file)
