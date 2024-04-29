from typing import Any
from intermediary_all import *
from ETK import *

class Steuerung:
    def __init__(self) -> None:
        self.__objects: dict[ETKBaseObject, IBaseObject] = {}
        self.__intermediary = Intermediary()
        self.__gui = GUI(self)
    
    def on_gui_init(self) -> None:
        #create window object
        object: IWindow = self.__intermediary.create_object(IWindow)

        self.__gui.element_area.size = vector2d(object.size[0], object.size[1])
        self.__gui.element_area.background_color = object.background_color[0] << 16 | object.background_color[1] << 8 | object.background_color[2]

        self.__objects.update({self.__gui: object})

        #init window attributes
        self.__gui.attributes_window_id_var.text = str(object.id)
        self.__gui.attributes_window_name_var.text = object.name
        self.__gui.attributes_window_title_var.text = object.title
        self.__gui.attributes_window_size_var_x.text = str(object.size[0])
        self.__gui.attributes_window_size_var_y.text = str(object.size[1])
        self.__gui.attributes_window_title_color_var_r.text = str(object.title_color[0])
        self.__gui.attributes_window_title_color_var_g.text = str(object.title_color[1])
        self.__gui.attributes_window_title_color_var_b.text = str(object.title_color[2])
        self.__gui.attributes_window_background_color_var_r.text = str(object.background_color[0])
        self.__gui.attributes_window_background_color_var_g.text = str(object.background_color[1])
        self.__gui.attributes_window_background_color_var_b.text = str(object.background_color[2])
        self.__gui.attributes_window_event_create_var.state = object.event_create
        self.__gui.attributes_window_event_destroy_var.state = object.event_destroy
        self.__gui.attributes_window_event_paint_var.state = object.event_paint
        self.__gui.attributes_window_event_resize_var.state = object.event_resize
        self.__gui.attributes_window_event_mouse_click_var.state = object.event_mouse_click
        self.__gui.attributes_window_event_mouse_move_var.state = object.event_mouse_move


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
        match type:
            case t if t == IButton:
                gui_element = self.__gui.create_new_element(ETKButton)
            case t if t == ICheckbox:
                gui_element = self.__gui.create_new_element(ETKCheckbox)
            case t if t in [ILabel, IEdit, ICanvas, ITimer]:
                gui_element = self.__gui.create_new_element(ETKLabel)
            case _:
                raise ValueError
        
        print(object)
        
        if type == ITimer:
            gui_element.text = "Timer"
        elif type == ICanvas:
            gui_element.text = "Canvas"
        else:
            gui_element.text = object.text
            gui_element.text_color = object.text_color[0] << 16 | object.text_color[1] << 8 | object.text_color[2]
        
        gui_element.size = vector2d(object.size[0], object.size[1])

        if type != ITimer:
            gui_element.background_color = object.background_color[0] << 16 | object.background_color[1] << 8 | object.background_color[2]
        
        self.__objects.update({gui_element: object})

        return gui_element
    
    def update_element_attributes_gui(self, element: ETKBaseObject):
        object: Any = self.__objects[element]

        self.__gui.attributes_element_id_var.text = str(object.id)
        self.__gui.attributes_element_name_var.text = object.name
        self.__gui.attributes_element_text_var.text = object.text
        self.__gui.attributes_element_pos_var_x.text = str(object.pos[0])
        self.__gui.attributes_element_pos_var_y.text = str(object.pos[1])
        self.__gui.attributes_element_size_var_x.text = str(object.size[0])
        self.__gui.attributes_element_size_var_y.text = str(object.size[1])
        self.__gui.attributes_element_text_color_var_r.text = str(object.text_color[0])
        self.__gui.attributes_element_text_color_var_g.text = str(object.text_color[1])
        self.__gui.attributes_element_text_color_var_b.text = str(object.text_color[2])
        self.__gui.attributes_element_background_color_var_r.text = str(object.background_color[0])
        self.__gui.attributes_element_background_color_var_g.text = str(object.background_color[1])
        self.__gui.attributes_element_background_color_var_b.text = str(object.background_color[2])

        if type(object) in [IEdit, ICheckbox]:
            self.__gui.attributes_element_event_changed_container.visibility = True
            self.__gui.attributes_element_event_changed_var.state = object.changed
        else:
            self.__gui.attributes_element_event_changed_container.visibility = False
        if type(object) == IButton:
            self.__gui.attributes_element_event_pressed_container.visibility = True
            self.__gui.attributes_element_event_pressed_var.state = object.event_pressed
            self.__gui.attributes_element_event_double_pressed_container.visibility = True
            self.__gui.attributes_element_event_double_pressed_var.state = object.event_double_pressed
        else:
            self.__gui.attributes_element_event_pressed_container.visibility = False
            self.__gui.attributes_element_event_double_pressed_container.visibility = False
        self.__gui.attributes_element_event_hovered_var.state = object.event_hovered

        if not self.__gui.attributes_element_inner.visibility:
            self.__gui.attributes_element_inner.visibility = True

    def run(self) -> None:
        self.__gui.run()

from gui import GUI