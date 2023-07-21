from typing import Any

import eel
from tkinter import Tk, filedialog as fd
from intermediary.intermediary import *
from intermediary.json import *
from generator.generator import *

g_intermediary: Intermediary
g_generator: Generator
g_json: JSON
g_window_id: int

def init():
    global g_intermediary
    g_intermediary = Intermediary()
    global g_window_id
    g_window_id = g_intermediary.createObject(ObjectEnum.WINDOW)

    global g_generator
    g_generator = Generator()

    global g_json
    g_json = JSON(g_intermediary)

    eel.init('additional_files\\gui')
    eel.brw.set_path('chrome', '.\\additional_files\\brave\\brave.exe')
    eel.start('main.html', size=(320, 120), mode="firefox") #NOTE

def resetData():
    global g_intermediary
    g_intermediary = Intermediary()
    global g_window_id
    g_window_id = g_intermediary.createObject(ObjectEnum.WINDOW)

    global g_generator
    g_generator = Generator()

    global g_json
    g_json = JSON(g_intermediary)

@eel.expose
def gui_init() -> dict[str, Any]:
    resetData()
    return convert_attribut_to_js_data(g_intermediary.getObject(g_window_id).getAttributesAsDictionary())



def convert_attribut_to_js_data(p_attribut) -> dict[str, any]:
    t_type = p_attribut["type"]
    t_return = {}
    t_return["id"] = p_attribut["id"]
    t_return["type"] = p_attribut["type"]
    t_return["name"] = p_attribut["name"]

    if t_type in ("window", "button", "label", "edit", "checkbox"):
        t_return["text"] = p_attribut["text"]
        t_return["text_color"] = hex(p_attribut["textColor"][0]).ljust(4, "0")[2:] + hex(p_attribut["textColor"][1]).ljust(4, "0")[2:] + hex(p_attribut["textColor"][2]).ljust(4, "0")[2:]

    if t_type in ("window", "button", "label", "edit", "checkbox", "canvas", "timer"):
        t_return["size_x"] = p_attribut["size"][0]
        t_return["size_y"] = p_attribut["size"][1]
    
    if t_type in ("window", "button", "label", "edit", "checkbox", "canvas"):
        t_return["background_color"] = hex(p_attribut["backgroundColor"][0]).ljust(4, "0")[2:] + hex(p_attribut["backgroundColor"][1]).ljust(4, "0")[2:] + hex(p_attribut["backgroundColor"][2]).ljust(4, "0")[2:]
    
    if t_type in ("button", "label", "edit", "checkbox", "canvas", "timer"):
        t_return["pos_x"] = p_attribut["position"][0]
        t_return["pos_y"] = p_attribut["position"][1]

    if t_type in ("button", "label", "edit", "checkbox", "canvas"):
        t_return["event_hovered"] = p_attribut["eventHovered"]

    if t_type in ("button"):
        t_return["event_pressed"] = p_attribut["eventPressed"]
    
    if t_type in ("edit", "checkbox"):
        t_return["event_changed"] = p_attribut["eventChanged"]

    if t_type == "edit":
        t_return["multiple_lines"] = p_attribut["multipleLines"]
    
    if t_type == "checkbox":
        t_return["checked"] = p_attribut["checked"]
    
    if t_type == "timer":
        t_return["enabled"] = p_attribut["enabled"]
        t_return["interval"] = p_attribut["interval"]
    
    if t_type == "window":
        t_return["event_create"] = p_attribut["eventCreate"]
        t_return["event_paint"] = p_attribut["eventPaint"]
        t_return["event_resize"] = p_attribut["eventResize"]
        t_return["event_mouse_click"] = p_attribut["eventMouseClick"]
        t_return["event_mouse_move"] = p_attribut["eventMouseMove"]
    
    return t_return

def convert_attribut_from_js_data(p_attribut) -> dict[str, any]:
    t_type = p_attribut["type"]
    t_return = {}
    t_return["id"] = p_attribut["id"]
    t_return["type"] = p_attribut["type"]
    t_return["name"] = p_attribut["name"]
    
    if t_type in ("window", "button", "label", "edit", "checkbox"):
        t_return["text"] = p_attribut["text"]
        t_return["textColor"] = (int(p_attribut["text_color"][0:2], 16), int(p_attribut["text_color"][2:4], 16), int(p_attribut["text_color"][4:6], 16))

    if t_type in ("window", "button", "label", "edit", "checkbox", "canvas", "timer"):
        t_return["size"] = (p_attribut["size_x"], p_attribut["size_y"])

    if t_type in ("window", "button", "label", "edit", "checkbox", "canvas"):
        t_return["backgroundColor"] = (int(p_attribut["background_color"][0:2], 16), int(p_attribut["background_color"][2:4], 16), int(p_attribut["background_color"][4:6], 16))

    if t_type in ("button", "label", "edit", "checkbox", "canvas", "timer"):
        t_return["position"] = (p_attribut["pos_x"], p_attribut["pos_y"])
        
    if t_type in ("button", "label", "edit", "checkbox", "canvas"):
        t_return["eventHovered"] = p_attribut["event_hovered"]

    if t_type in ("button"):
        t_return["eventPressed"] = p_attribut["event_pressed"]
    
    if t_type in ("edit", "checkbox"):
        t_return["eventChanged"] = p_attribut["event_changed"]

    if t_type == "edit":
        t_return["multipleLines"] = p_attribut["multiple_lines"]
    
    if t_type == "checkbox":
        t_return["checked"] = p_attribut["checked"]
    
    if t_type == "timer":
        t_return["enabled"] = p_attribut["enabled"]
        t_return["interval"] = p_attribut["interval"]

    if t_type == "window":
        t_return["eventCreate"] = p_attribut["event_create"]
        t_return["eventPaint"] = p_attribut["event_paint"]
        t_return["eventResize"] = p_attribut["event_resize"]
        t_return["eventMouseClick"] = p_attribut["event_mouse_click"]
        t_return["eventMouseMove"] = p_attribut["event_mouse_move"]
    
    return t_return

def get_load_file_path() -> str:
    root = Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    file = fd.askopenfilename(filetypes=[("JSON", ".json")])
    return file

def get_save_file_path() -> str:
    root = Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    file = fd.asksaveasfilename(filetypes=[("JSON", ".json")])
    return file

def get_dir_path() -> str:
    root = Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    path = fd.askdirectory()
    return path


@eel.expose
def load_gui_elements() -> list[dict[str, Any]]:
    t_path = get_dir_path()
    g_json.load(t_path)
    t_objekts = []
    for o in g_intermediary.getObjects():
        t_objekts.append(convert_attribut_to_js_data(o.getAttributesAsDictionary()))
    #print(t_objekts)
    return t_objekts

@eel.expose
def save_gui_element(p_attributes: dict[str, any]):
    #print(p_attributes)
    t_attributes = convert_attribut_from_js_data(p_attributes)
    #print(t_attributes)
    t_obj = g_intermediary.getObject(p_attributes["id"])
    for n, w in t_attributes.items():
        if n in("id", "type"):
            continue
        t_obj.setAttribute(n, w)

@eel.expose
def save():
    t_data = g_intermediary.getObjectsAsDictionaryList()
    #print(t_data)
    t_path = get_dir_path()
    #print(t_path)
    #g_generator.write_files(t_path, t_data) #NOTE
    g_json.save(t_path)



@eel.expose
def delete_element(p_id: int):
    g_intermediary.removeObject(p_id)

@eel.expose
def create_btn() -> dict[str, Any]:
    t_id = g_intermediary.createObject(ObjectEnum.BUTTON)
    t_data = convert_attribut_to_js_data(g_intermediary.getObject(t_id).getAttributesAsDictionary())
    #print(t_data)
    return t_data

@eel.expose
def create_label() -> dict[str, Any]:
    t_id = g_intermediary.createObject(ObjectEnum.LABEL)
    t_data = convert_attribut_to_js_data(g_intermediary.getObject(t_id).getAttributesAsDictionary())
    #print(t_data)
    return t_data

@eel.expose
def create_edit() -> dict[str, Any]:
    t_id = g_intermediary.createObject(ObjectEnum.EDIT)
    t_data = convert_attribut_to_js_data(g_intermediary.getObject(t_id).getAttributesAsDictionary())
    #print(t_data)
    return t_data

@eel.expose
def create_checkbox() -> dict[str, Any]:
    t_id = g_intermediary.createObject(ObjectEnum.CHECKBOX)
    t_data = convert_attribut_to_js_data(g_intermediary.getObject(t_id).getAttributesAsDictionary())
    #print(t_data)
    return t_data

@eel.expose
def create_canvas() -> dict[str, Any]:
    t_id = g_intermediary.createObject(ObjectEnum.CANVAS)
    t_data = convert_attribut_to_js_data(g_intermediary.getObject(t_id).getAttributesAsDictionary())
    #print(t_data)
    return t_data

@eel.expose
def create_timer() -> dict[str, Any]:
    t_id = g_intermediary.createObject(ObjectEnum.TIMER)
    t_data = convert_attribut_to_js_data(g_intermediary.getObject(t_id).getAttributesAsDictionary())
    #print(t_data)
    return t_data



@eel.expose
def temptest():
    pass

if __name__ == "__main__":
    init()