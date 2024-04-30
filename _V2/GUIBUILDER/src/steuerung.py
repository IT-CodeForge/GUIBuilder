from os import path
from tkinter import Tk, filedialog as fd
from typing import Any
from intermediary_all import *
from ETK import *

class Steuerung:
    def __init__(self) -> None:
        self.__objects: dict[ETKBaseObject, IBaseObject] = {}
        self.__save_path: str = f"{path.split(__file__)[0]}"  # TODO: check if .exe
        self.__intermediary = Intermediary()
        self.__gui = GUI(self)

    def on_gui_init(self) -> None:
        # ElementAttributeGui to generic Attributename
        self.__EL_GUI_TO_GEN_ATTR: dict[ETKEdit | ETKCheckbox, str] = {self.__gui.attributes_element_name_var: "name", self.__gui.attributes_element_text_var: "text", self.__gui.attributes_element_pos_var_x: "pos_x", self.__gui.attributes_element_pos_var_y: "pos_y", self.__gui.attributes_element_size_var_x: "size_x", self.__gui.attributes_element_size_var_y: "size_y", self.__gui.attributes_element_text_color_var_r: "text_color_r", self.__gui.attributes_element_text_color_var_g: "text_color_g", self.__gui.attributes_element_text_color_var_b: "text_color_b", self.__gui.attributes_element_background_color_var_r: "background_color_r", self.__gui.attributes_element_background_color_var_g: "background_color_g", self.__gui.attributes_element_background_color_var_b: "background_color_b", self.__gui.attributes_element_interval_var: "interval", self.__gui.attributes_element_enabled_var: "enabled", self.__gui.attributes_element_checked_var: "checked", self.__gui.attributes_element_event_pressed_var: "event_pressed", self.__gui.attributes_element_event_double_pressed_var: "event_double_pressed", self.__gui.attributes_element_event_changed_var: "event_changed", self.__gui.attributes_element_event_hovered_var: "event_hovered"}
        self.__GEN_ATTR_TO_EL_GUI: dict[str, ETKEdit | ETKCheckbox] = {v: k for k, v in self.__EL_GUI_TO_GEN_ATTR.items()}

        # WindowAttributeGui to generic Attributename
        self.__WIN_GUI_TO_GEN_ATTR: dict[ETKEdit | ETKCheckbox, str] = {self.__gui.attributes_window_name_var: "name", self.__gui.attributes_window_title_var: "title", self.__gui.attributes_window_size_var_x: "size_x", self.__gui.attributes_window_size_var_y: "size_y", self.__gui.attributes_window_title_color_var_r: "title_color_r", self.__gui.attributes_window_title_color_var_g: "title_color_g", self.__gui.attributes_window_title_color_var_b: "title_color_b", self.__gui.attributes_window_background_color_var_r: "background_color_r", self.__gui.attributes_window_background_color_var_g: "background_color_g", self.__gui.attributes_window_background_color_var_b: "background_color_b", self.__gui.attributes_window_event_create_var: "event_create", self.__gui.attributes_window_event_destroy_var: "event_destroy", self.__gui.attributes_window_event_paint_var: "event_paint", self.__gui.attributes_window_event_resize_var: "event_resize", self.__gui.attributes_window_event_mouse_click_var: "event_mouse_click", self.__gui.attributes_window_event_mouse_move_var: "event_mouse_move"}
        self.__GEN_ATTR_TO_WIN_GUI: dict[str, ETKEdit | ETKCheckbox] = {v: k for k, v in self.__WIN_GUI_TO_GEN_ATTR.items()}

        # generic Attributename to ElementAttributeGuiContainer
        self.__GEN_ATTR_TO_EL_GUI_CONT: dict[str, ETKListingContainer] = {"name": self.__gui.attributes_element_name_container, "text": self.__gui.attributes_element_text_container, "pos": self.__gui.attributes_element_pos_container, "size": self.__gui.attributes_element_size_container, "text_color": self.__gui.attributes_element_text_color_container, "background_color": self.__gui.attributes_element_background_color_container, "interval": self.__gui.attributes_element_interval_container, "enabled": self.__gui.attributes_element_enabled_container, "checked": self.__gui.attributes_element_checked_container, "event_pressed": self.__gui.attributes_element_event_pressed_container, "event_double_pressed": self.__gui.attributes_element_event_double_pressed_container, "event_changed": self.__gui.attributes_element_event_changed_container, "event_hovered": self.__gui.attributes_element_event_hovered_container}

        # create window object
        object: IWindow = self.__intermediary.create_object(IWindow)

        self.__objects.update({self.__gui: object})

        self.__load_window_attributes_in_editor()
        self.__apply_window_attributes_to_gui()

    def create_new_element_event(self, caller: ETKBaseObject) -> ETKBaseObject:
        match caller:
            case self.__gui.menubar_button:
                return self.__create_new_element(IButton)
            case self.__gui.menubar_label:
                return self.__create_new_element(ILabel)
            case self.__gui.menubar_edit:
                return self.__create_new_element(IEdit)
            case self.__gui.menubar_checkbox:
                return self.__create_new_element(ICheckbox)
            case self.__gui.menubar_canvas:
                return self.__create_new_element(ICanvas)
            case self.__gui.menubar_timer:
                return self.__create_new_element(ITimer)
            case _:
                raise ValueError

    def __create_new_element(self, type: type[IBaseObject]) -> ETKBaseObject:
        object: Any = self.__intermediary.create_object(type)
        
        gui_element = self.__create_new_gui_element(type)

        self.__objects.update({gui_element: object})

        self.__apply_object_attributes_to_gui(object)

        return gui_element
    
    def __create_new_gui_element(self, type: type[IBaseObject]) -> ETKBaseObject:
        match type:
            case t if t == IButton:
                gui_element = self.__gui.create_new_element(ETKButton)
            case t if t == ICheckbox:
                gui_element = self.__gui.create_new_element(ETKCheckbox)
            case t if t in [ILabel, IEdit, ICanvas, ITimer]:
                gui_element = self.__gui.create_new_element(ETKLabel)
            case _:
                raise ValueError

        if type == ITimer:
            gui_element.text = "Timer"
        elif type == ICanvas:
            gui_element.text = "Canvas"

        return gui_element
    
    def __verify_element_pos_size(self, pos: tuple[int, int], size: tuple[int, int]) -> tuple[tuple[int, int], tuple[int, int]]:
        r_pos = list(pos)
        r_size = list(size)

        if r_pos[0] < 0:
            r_pos[0] = 0
        if r_pos[1] < 0:
            r_pos[1] = 0
        if r_size[0] <= 0:
            r_size[0] = 1
        if r_size[1] <= 0:
            r_size[1] = 1
        
        if r_size[0] > self.__gui.element_area.size.x:
            r_size[0] = self.__gui.element_area.size.x
        if r_size[1] > self.__gui.element_area.size.y:
            r_size[1] = self.__gui.element_area.size.y
        if r_pos[0] + r_size[0] > self.__gui.element_area.size.x:
            r_pos[0] = self.__gui.element_area.size.x - r_size[0]
        if r_pos[1] + r_size[1] > self.__gui.element_area.size.y:
            r_pos[1] = self.__gui.element_area.size.y - r_size[1]

        return (r_pos[0], r_pos[1]), (r_size[0], r_size[1])

    def __verify_window_size(self, size: tuple[int, int]) -> tuple[int, int]:
        r_size = list(size)

        space = [e.pos + e.size for e in self.__objects.keys() if e != self.__gui]
        space_x = [s.x for s in space] + [0]
        space_y = [s.y for s in space] + [0]

        min_x = max(space_x) if max(space_x) >= 100 else 100
        min_y = max(space_y) if max(space_y) >= 100 else 100
        
        if r_size[0] < min_x:
            r_size[0] = int(min_x)
        if r_size[1] < min_y:
            r_size[1] = int(min_y)
        if r_size[0] > self.__gui.main2.size.x:
            r_size[0] = self.__gui.main2.size.x - self.__gui.attributes.size.x
        if r_size[1] > self.__gui.main2.size.y:
            r_size[1] = self.__gui.main2.size.y

        return r_size[0], r_size[1]
    
    @staticmethod
    def __convert_to_int(st: Any, fallback: int = 0) -> int:
        try:
            ret = int(st)
        except ValueError:
            ret = fallback
        return ret
    
    def __get_attribute_value(self, attr_name: str, object: IBaseObject) -> str:
        try:
            if attr_name[-2:] == "_x":
                value = getattr(object, attr_name[:-2])[0]
            elif attr_name[-2:] == "_y":
                value = getattr(object, attr_name[:-2])[1]
            elif attr_name[-2:] == "_r":
                value = getattr(object, attr_name[:-2])[0]
            elif attr_name[-2:] == "_g":
                value = getattr(object, attr_name[:-2])[1]
            elif attr_name[-2:] == "_b":
                value = getattr(object, attr_name[:-2])[2]
            else:
                value = getattr(object, attr_name)
        except AttributeError:
            value = "-"
        return str(value)

    def __load_attributes_in_editor(self, element: ETKBaseObject, translation: dict[ETKEdit | ETKCheckbox, str]) -> None:
        object = self.__objects[element]
        for o, a in translation.items():
            value = self.__get_attribute_value(a, object)
            if type(o) == ETKEdit:
                o.text = str(value)
            elif type(o) == ETKCheckbox:
                if value == "True":
                    o.state = True
                else:
                    o.state = False
            else:
                raise RuntimeError

    def __load_window_attributes_in_editor(self) -> None:
        self.__load_attributes_in_editor(self.__gui, self.__WIN_GUI_TO_GEN_ATTR)
    
    def __load_element_attributes_in_editor(self, element: ETKBaseObject) -> None:
        self.__load_attributes_in_editor(element, self.__EL_GUI_TO_GEN_ATTR)
        object = self.__objects[element]
        for a in ["text", "text_color", "background_color", "interval", "enabled", "checked", "event_pressed", "event_double_pressed", "event_changed", "event_hovered"]:
            if hasattr(object, a):
                self.__GEN_ATTR_TO_EL_GUI_CONT[a].visibility = True
            else:
                self.__GEN_ATTR_TO_EL_GUI_CONT[a].visibility = False
    
    def __apply_window_attributes_to_gui(self) -> None:
        object = self.__objects[self.__gui]
        if type(object) != IWindow:
            raise RuntimeError
        self.__gui.element_area.size = vector2d(object.size[0], object.size[1])
        self.__gui.element_area.background_color = object.background_color[0] << 16 | object.background_color[1] << 8 | object.background_color[2]
    
    def __apply_object_attributes_to_gui(self, object: IBaseObjectWidget):
        gui_element = {o: g for g, o in self.__objects.items()}[object]
        gui_element.pos = vector2d(object.pos[0], object.pos[1])
        gui_element.size = vector2d(object.size[0], object.size[1])
        if isinstance(object, IBaseObjectWidgetVisible) and isinstance(gui_element, ETKBaseWidget):
            gui_element.background_color = object.background_color[0] << 16 | object.background_color[1] << 8 | object.background_color[2]
        if isinstance(object, IBaseObjectWidgetText) and isinstance(gui_element, ETKBaseTkWidgetText):
            gui_element.text = object.text
            gui_element.text_color = object.text_color[0] << 16 | object.text_color[1] << 8 | object.text_color[2]

    def __set_attribute_event(self, caller: ETKEdit | ETKCheckbox, object: IBaseObject, translation_dict: dict[ETKEdit | ETKCheckbox, str]):
        if type(caller) == ETKEdit:
            value = caller.text
        elif type(caller) == ETKCheckbox:
            value = caller.state
        else:
            raise TypeError

        attr_name = translation_dict[caller]

        if attr_name[-2:] == "_x":
            attr_name = attr_name[:-2]
            value = (self.__convert_to_int(value), getattr(object, attr_name)[1])
        elif attr_name[-2:] == "_y":
            attr_name = attr_name[:-2]
            value = (getattr(object, attr_name)[0], self.__convert_to_int(value))
        elif attr_name[-2:] == "_r":
            attr_name = attr_name[:-2]
            ob_data = getattr(object, attr_name)
            value = (self.__convert_to_int(value), ob_data[1], ob_data[2])
        elif attr_name[-2:] == "_g":
            attr_name = attr_name[:-2]
            ob_data = getattr(object, attr_name)
            value = (ob_data[0], self.__convert_to_int(value), ob_data[2])
        elif attr_name[-2:] == "_b":
            attr_name = attr_name[:-2]
            ob_data = getattr(object, attr_name)
            value = (ob_data[0], ob_data[1], self.__convert_to_int(value))
        elif attr_name in ["interval"]:
            value = self.__convert_to_int(value, 100)
        
        setattr(object, attr_name, value)

    def set_element_attribute_event(self, caller: ETKEdit | ETKCheckbox) -> None:        
        if self.__gui.active_attributes_element == None:
            raise RuntimeError
        
        object = self.__objects[self.__gui.active_attributes_element]
        self.__set_attribute_event(caller, object, self.__EL_GUI_TO_GEN_ATTR)
        
        if isinstance(object, IBaseObjectWidget):
            pos = object.pos
            size = object.size
            pos, size = self.__verify_element_pos_size(pos, size)
            object.pos = pos
            object.size = size
            self.__GEN_ATTR_TO_EL_GUI["pos_x"].text = str(pos[0])
            self.__GEN_ATTR_TO_EL_GUI["pos_y"].text = str(pos[1])
            self.__GEN_ATTR_TO_EL_GUI["size_x"].text = str(size[0])
            self.__GEN_ATTR_TO_EL_GUI["size_y"].text = str(size[1])
        
        if not isinstance(object, IBaseObjectWidget):
            raise RuntimeError
        self.__apply_object_attributes_to_gui(object)

    def update_element_pos_event(self, element: ETKBaseObject):
        object = self.__objects[element]
        if not isinstance(object, IBaseObjectWidget):
            raise RuntimeError
        object.pos = (int(element.pos.x), int(element.pos.y))
        self.__GEN_ATTR_TO_EL_GUI["pos_x"].text = str(int(element.pos.x))
        self.__GEN_ATTR_TO_EL_GUI["pos_y"].text = str(int(element.pos.y))
        
        

    def set_window_attribute_event(self, caller: ETKEdit | ETKCheckbox) -> None:
        object = self.__objects[self.__gui]
        self.__set_attribute_event(caller, object, self.__WIN_GUI_TO_GEN_ATTR)

        size = object.size
        size = self.__verify_window_size(size)
        object.size = size
        self.__GEN_ATTR_TO_WIN_GUI["size_x"].text = str(size[0])
        self.__GEN_ATTR_TO_WIN_GUI["size_y"].text = str(size[1])

        self.__apply_window_attributes_to_gui()

    def delete_element(self, element: ETKBaseObject):
        self.__intermediary.delete_object(self.__objects[element])
        self.__objects.pop(element)
        element.visibility = False  # NOTE
        self.__gui.attributes_element_inner.visibility = False

    def update_element_attributes_gui(self, element: ETKBaseObject):
        if self.__gui.active_attributes_element == element:
            return
        self.__gui.active_attributes_element = element

        self.__load_element_attributes_in_editor(element)

        if not self.__gui.attributes_element_inner.visibility:
            self.__gui.attributes_element_inner.visibility = True

    def __get_load_file_path(self) -> str:
        root = Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)  # type:ignore
        t_initialdir_path = self.__save_path
        file = fd.askopenfilename(
            filetypes=[("JSON", ".json")], initialdir=t_initialdir_path)
        if file != "":
            self.__save_path = path.split(file)[0]
        return file

    def __get_save_file_path(self) -> str:
        root = Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)  # type:ignore
        t_initialdir_path = self.__save_path
        file: str = fd.asksaveasfilename(filetypes=[("JSON", ".json")], initialdir=t_initialdir_path, defaultextension=".json")
        if file != "":
            self.__save_path = path.split(file)[0]
        return file  # type:ignore

    def __get_dir_path(self) -> str:
        root = Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)  # type:ignore
        t_initialdir_path = self.__save_path
        t_path = fd.askdirectory(initialdir=t_initialdir_path)
        if t_path != "":
            self.__save_path = t_path
        return t_path  # type:ignore

    def save_elements_to_file(self) -> None:
        path = self.__get_save_file_path()
        if path == "":
            return
        self.__intermediary.save_to_file(path)

    def load_elements_from_file(self) -> None:
        path = self.__get_load_file_path()
        if path == "":
            return
        
        for e in self.__objects.keys():
            if e == self.__gui:
                continue
            e.visibility = False  # NOTE
        self.__objects = {}
        
        self.__intermediary = Intermediary()
        self.__intermediary.load_from_file(path)

        for e in self.__intermediary.objects:
            if type(e) == IWindow:
                self.__objects.update({self.__gui: e})
                continue
            self.__objects.update({self.__create_new_gui_element(type(e)): e})
            

        self.__load_window_attributes_in_editor()
        self.__apply_window_attributes_to_gui()

        for e, o in self.__objects.items():
            if e == self.__gui:
                continue
            if not isinstance(o, IBaseObjectWidget):
                raise RuntimeError
            self.__load_element_attributes_in_editor(e)
            self.__apply_object_attributes_to_gui(o)

    def run(self) -> None:
        self.__gui.run()

# fmt: off
from gui import GUI
# fmt: on