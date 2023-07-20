from email import generator
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

@eel.expose
def gui_init() -> int:
    return g_window_id



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
    #g_json.load(p_path) #NOTE
    t_objekts = g_intermediary.getObjectsAsDictionaryList()
    print(t_objekts)
    return t_objekts

@eel.expose
def save_gui_element(p_id: int, p_name: str, p_text: str, p_pos: tuple[int, int], p_size: tuple[int, int], p_bg_col: tuple[int, int, int], p_text_col: tuple[int, int, int], p_event_pressed: bool, p_event_hovered: bool, p_event_changed: bool):
    print(p_id, p_name, p_text, p_pos, p_size,p_bg_col, p_text_col, p_event_pressed, p_event_hovered, p_event_changed)
    t_obj = g_intermediary.getObject(p_id)
    t_obj.setAttribute("name", p_name)
    t_obj.setAttribute("text", p_text)
    t_obj.setAttribute("position", p_pos)
    t_obj.setAttribute("size", p_size)
    t_obj.setAttribute("backgroundColor", p_bg_col)
    t_obj.setAttribute("textColor", p_text_col)
    t_obj.setAttribute("eventPressed", p_event_pressed)
    t_obj.setAttribute("eventHovered", p_event_hovered)
    t_obj.setAttribute("eventChanged", p_event_changed)

@eel.expose
def save():
    t_data = g_intermediary.getObjectsAsDictionaryList()
    #print(t_data)
    t_path = get_dir_path()
    print(t_path)
    g_generator.write_files(t_path, t_data) #NOTE
    #g_json.save(t_path) #NOTE



@eel.expose
def delete_element(p_id: int):
    g_intermediary.removeObject(p_id)

@eel.expose
def create_btn() -> int:
    t_id = g_intermediary.createObject(ObjectEnum.BUTTON)
    return g_intermediary.getObject(t_id).getAttributesAsDictionary()



@eel.expose
def temptest():
    pass

if __name__ == "__main__":
    init()