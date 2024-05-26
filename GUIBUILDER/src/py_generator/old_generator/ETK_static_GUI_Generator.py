from typing import Any
from ETK_python_code_generator import ETK_python_code_generator
from ..intermediary_neu.objects.IBaseObject import IBaseObject
from ..intermediary_neu.objects.IButton import IButton
from ..intermediary_neu.objects.ICanvas import ICanvas
from ..intermediary_neu.objects.ICheckbox import ICheckbox
from ..intermediary_neu.objects.IEdit import IEdit
from ..intermediary_neu.objects.ILabel import ILabel
from ..intermediary_neu.objects.ITimer import ITimer
from ..intermediary_neu.objects.IWindow import IWindow

class ETK_static_GUI_Generator:
    def __init__(self) -> None:
        self.__my_generator = ETK_python_code_generator()
        self.__indent:str = ""
        self.__static_gui: str
        with open("./static_template.py", "r") as file:
            self.__static_gui = file.read()
    
    def write_file(self, objects: list[IBaseObject])->str:
        init_params: str = ""
        element_string: str = ""
        event_bind_string: str = ""
        event_funcs_string: str = ""

        for gui_object in objects:
            if type(gui_object) == IWindow:
                init_params = self.__generate_init_params(gui_object)
            else:
                self.__indent = "        "
                element_string += self.__generate_element(gui_object)
            event_bind_string += self.__generate_events(gui_object)
            self.__indent = "    "
            event_funcs_string += self.__generate_event_funcs(gui_object)

        self.__static_gui = self.__static_gui.replace("#tag:gui_params#", init_params)
        self.__static_gui = self.__static_gui.replace("#tag:generate_elements#", element_string)
        self.__static_gui = self.__static_gui.replace("#tag:bind_events#", event_bind_string)
        self.__static_gui = self.__static_gui.replace("#tag:event_funcs#", event_funcs_string)

        return self.__static_gui
    
    def __generate_element(self, gui_object: Any)->str:
        if type(gui_object) == IWindow:
            return ""
        parameters:str = "tk=self._tk_object"
        object_name: str = gui_object.name
        retval: str = object_name + ": ETK" + str(type(gui_object))[1:] + " = "
        if type(gui_object) in [IButton, ICheckbox, IEdit, ILabel, ICanvas]:
            parameters += ", pos=" + self.__generate_Vector2d_from_tuple(gui_object.pos)
            parameters += ", size=" + self.__generate_Vector2d_from_tuple(gui_object.size)
            parameters += ", background_color=" + self.__generate_color_from_tuple(gui_object.background_color)
            if type(gui_object) in [IButton, ICheckbox, IEdit, ILabel]:
                parameters += ", text_color=" + self.__generate_color_from_tuple(gui_object.text_color)
                parameters += ", text=" + gui_object.text
        if type(gui_object) == ITimer:
            parameters += ", interval=" + str(gui_object.interval)
            parameters += ", timer_func=" + object_name + "_timer_func"
        return self.__indent + retval + "ETK" + str(type(gui_object))[1:] + "(" + parameters + ")\r\n"
    
    def __generate_init_params(self, gui_object: IWindow)->str:
        parameters: str = ""
        parameters += ", size=" + self.__generate_Vector2d_from_tuple(gui_object.size)
        parameters += ", background_color=" + self.__generate_color_from_tuple(gui_object.background_color)
        parameters += ", caption=" + gui_object.title
        return parameters
    
    def __generate_events(self, gui_object: Any)->str:
        added_events: str = ""
        object_name: str = gui_object.name
        eventhandler: str = ""
        if type(gui_object) == ITimer:
            return ""
        if type(gui_object) == IWindow:
            #resize and paint event missing
            if gui_object.event_create:
                eventhandler = self.__generate_event_handler(object_name, "create")
                added_events += self.__indent + self.__generate_event_bind_func(object_name, "START", eventhandler) + "\n\r"
            if gui_object.event_destroy:
                eventhandler = self.__generate_event_handler(object_name, "destroy")
                added_events += self.__indent + self.__generate_event_bind_func(object_name, "EXIT", eventhandler) + "\n\r"
            if gui_object.event_mouse_click:
                eventhandler = self.__generate_event_handler(object_name, "mouse_click")
                added_events += self.__indent + self.__generate_base_event_bind_func(object_name, "MOUSE_DOWN", eventhandler) + "\n\r"
            if gui_object.event_mouse_move:
                eventhandler = self.__generate_event_handler(object_name, "mouse_move")
                added_events += self.__indent + self.__generate_base_event_bind_func(object_name, "MOUSE_MOVED", eventhandler) + "\n\r"
            return added_events
        if gui_object.event_hovered:
            eventhandler = self.__generate_event_handler(object_name, "hovered")
            added_events += self.__indent + self.__generate_base_event_bind_func(object_name, "ENTER", eventhandler) + "\n\r"
        if type(gui_object) == IEdit:
            if gui_object.event_changed:
                eventhandler = self.__generate_event_handler(object_name, "changed")
                added_events += self.__indent + self.__generate_event_bind_func(object_name, "CHANGED", eventhandler) + "\n\r"
        if type(gui_object) == ICheckbox:
            if gui_object.event_changed:
                eventhandler = self.__generate_event_handler(object_name, "changed")
                added_events += self.__indent + self.__generate_event_bind_func(object_name, "TOGGLED", eventhandler) + "\n\r"
        if type(gui_object) == IButton:
            #doubble pressed event missing
            if gui_object. event_pressed:
                eventhandler = self.__generate_event_handler(object_name, "pressed")
                added_events += self.__indent + self.__generate_event_bind_func(object_name, "PRESSED", eventhandler) + "\n\r"
        return added_events
        
    
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
    
    def __generate_event_handler(self, object_name:str, event_type: str):
        return "self._ev_" + event_type + "_" + object_name + "(self, params: tuple[BaseObject, Events, Event])"

    def __generate_event_bind_func(self, object_name: str, event_type: str, eventhandler: str)->str:
        return "self." + object_name + ".add_event(" + "ETK" + object_name + "." + event_type + ", " + eventhandler[:-2] + ")\r\n"
    
    def __generate_base_event_bind_func(self, object_name: str, event_type: str, eventhandler: str)->str:
        return "self." + object_name + ".add_event(" + "ETKEvents." + event_type + ", " + eventhandler[:-2] + ")\r\n"

    def __generate_Vector2d_from_tuple(self, input_tuple: tuple[int, int])->str:
        return "Vector2d(" + str(input_tuple[0]) + ", " + str(input_tuple[1]) + ")"
    
    def __generate_color_from_tuple(self, input_tuple: tuple[int,int,int])->str:
        return str((input_tuple[0] << 8) + (input_tuple[1] << 4) + input_tuple[0])

#ValueError, wenn liste nicht Korrekt
#NOTE: multipleLines für Edit Existiert im ETK_framework nicht
#NOTE: Button, hat kein Doublepressed Event
#NOTE: Window hat kein paint event
#NOTE: Window hat kein resize Event

if __name__ == "__main__":
    #code which tests every functionality
    myGenerator: ETK_static_GUI_Generator = ETK_static_GUI_Generator()
    objects = [{"type": "window", "position": [10,10], "size": [1024,512], "text": "Hallo", "backgroundColor": [12,23,34], "eventMouseMove": True},
               {"type": "button", "name": "einButton", "position": [10,10], "size": [128,32], "text": "Knopf", "eventPressed": True, "eventChanged": False},
               {"type": "checkbox", "name": "meineCheckbox", "position": [10,52], "size": [128,32], "text": "ich bin eine Checkbox", "eventChanged": True, "checked": False},
               {"id": 0, "type": "timer", "name": "einTimer", "interval": 1000, "enabled": True},
               {"type": "canvas", "name": "einCanvas", "position": [148,10], "size": [138,138], "backgroundColor": [255,0,0]},
               {"type": "label", "name": "einLabel", "position": [10, 94], "size": [12, 128], "text": "Ich bin ein label"},
               {"type": "edit", "name": "einEdit", "position": [148, 94], "size": [12, 128], "text": "Ich bin ein edit", "multipleLines": True, "eventChanged": True}]
    #myGenerator.write_file(objects)