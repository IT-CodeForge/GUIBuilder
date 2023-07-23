from os import devnull
import sys
# sys.stdout = sys.stderr = open(devnull, 'w')  # NOTE: Release: Disables print(), etc

from typing import Any
from os import environ, path
from sys import executable
import eel
from tkinter import Tk, filedialog as fd

from generator.generator import *
from intermediary.json import *
from intermediary.intermediary import *


class Steuerung:

    c_intermediary: Intermediary
    c_generator: Generator
    c_json: JSON
    c_window_id: int
    file: str
    additional_files_path: str

    @classmethod
    def init(cls):
        cls.c_intermediary = Intermediary()
        cls.c_window_id = cls.c_intermediary.createObject(ObjectEnum.WINDOW)

        cls.c_generator = Generator()

        cls.c_json = JSON(cls.c_intermediary)

        import os
        t_additional_files = f"{os.path.split(__file__)[0]}\\{cls.additional_files_path}"

        eel.init(f'{t_additional_files}\\gui')
        eel.brw.set_path('chrome', f'{t_additional_files}\\brave\\brave.exe')
        # eel.start('main.html', cmdline_args=['--start-maximized']) #NOTE: Realease-Mode
        eel.start('main.html', mode="firefox")  # NOTE: Dev-Mode

    @classmethod
    def resetData(cls):
        cls.c_intermediary = Intermediary()
        cls.c__window_id = cls.c_intermediary.createObject(ObjectEnum.WINDOW)

        cls.c_generator = Generator()

        cls.c_json = JSON(cls.c_intermediary)

    @staticmethod
    def gui_init() -> dict[str, Any]:
        cls = Steuerung
        cls.resetData()
        return cls.convert_attribut_to_js_data(cls.c_intermediary.getObject(cls.c__window_id).getAttributesAsDictionary())
    eel.expose(gui_init.__func__)

    @staticmethod
    def convert_attribut_to_js_data(p_attribut) -> dict[str, any]:
        t_type = p_attribut["type"]
        t_return = {}
        t_return["id"] = p_attribut["id"]
        t_return["type"] = p_attribut["type"]
        t_return["name"] = p_attribut["name"]

        if t_type in ("window", "button", "label", "edit", "checkbox"):
            t_return["text"] = p_attribut["text"]
            t_return["text_color"] = hex(p_attribut["textColor"][0]).ljust(4, "0")[
                2:] + hex(p_attribut["textColor"][1]).ljust(4, "0")[2:] + hex(p_attribut["textColor"][2]).ljust(4, "0")[2:]

        if t_type in ("window", "button", "label", "edit", "checkbox", "canvas", "timer"):
            t_return["size_x"] = p_attribut["size"][0]
            t_return["size_y"] = p_attribut["size"][1]

        if t_type in ("window", "button", "label", "edit", "checkbox", "canvas"):
            t_return["background_color"] = hex(p_attribut["backgroundColor"][0]).ljust(4, "0")[
                2:] + hex(p_attribut["backgroundColor"][1]).ljust(4, "0")[2:] + hex(p_attribut["backgroundColor"][2]).ljust(4, "0")[2:]

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
            t_return["event_destroy"] = p_attribut["eventDestroy"]
            t_return["event_paint"] = p_attribut["eventPaint"]
            t_return["event_resize"] = p_attribut["eventResize"]
            t_return["event_mouse_click"] = p_attribut["eventMouseClick"]
            t_return["event_mouse_move"] = p_attribut["eventMouseMove"]

        return t_return

    @staticmethod
    def convert_attribut_from_js_data(p_attribut) -> dict[str, any]:
        t_type = p_attribut["type"]
        t_return = {}
        t_return["id"] = p_attribut["id"]
        t_return["type"] = p_attribut["type"]
        t_return["name"] = p_attribut["name"]

        if t_type in ("window", "button", "label", "edit", "checkbox"):
            t_return["text"] = p_attribut["text"]
            t_return["textColor"] = (int(p_attribut["text_color"][0:2], 16), int(
                p_attribut["text_color"][2:4], 16), int(p_attribut["text_color"][4:6], 16))

        if t_type in ("window", "button", "label", "edit", "checkbox", "canvas", "timer"):
            t_return["size"] = (p_attribut["size_x"], p_attribut["size_y"])

        if t_type in ("window", "button", "label", "edit", "checkbox", "canvas"):
            t_return["backgroundColor"] = (int(p_attribut["background_color"][0:2], 16), int(
                p_attribut["background_color"][2:4], 16), int(p_attribut["background_color"][4:6], 16))

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
            t_return["eventDestroy"] = p_attribut["event_destroy"]
            t_return["eventPaint"] = p_attribut["event_paint"]
            t_return["eventResize"] = p_attribut["event_resize"]
            t_return["eventMouseClick"] = p_attribut["event_mouse_click"]
            t_return["eventMouseMove"] = p_attribut["event_mouse_move"]

        return t_return

    @staticmethod
    def get_load_file_path() -> str:
        root = Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)
        file = fd.askopenfilename(filetypes=[("JSON", ".json")])
        return file

    @staticmethod
    def get_save_file_path() -> str:
        root = Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)
        file = fd.asksaveasfilename(filetypes=[("JSON", ".json")])
        return file

    @classmethod
    def get_dir_path(cls) -> str:
        root = Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)
        t_initialdir_path = f"{path.split(cls.file)[0]}"
        t_path = fd.askdirectory(initialdir=t_initialdir_path)
        return t_path

    @staticmethod
    def load_gui_elements() -> list[dict[str, Any]]:
        cls = Steuerung
        t_path = cls.get_dir_path()
        if (t_path == ""):
            return None
        cls.c_json.load(t_path)
        t_objekts = []
        for o in cls.c_intermediary.getObjects():
            t_objekts.append(cls.convert_attribut_to_js_data(
                o.getAttributesAsDictionary()))
        # print(t_objekts)
        return t_objekts
    eel.expose(load_gui_elements.__func__)

    @staticmethod
    def save_gui_element(p_attributes: dict[str, any]):
        cls = Steuerung
        # print(p_attributes)
        t_attributes = cls.convert_attribut_from_js_data(p_attributes)
        # print(t_attributes)
        t_obj = cls.c_intermediary.getObject(p_attributes["id"])
        for n, w in t_attributes.items():
            if n in ("id", "type"):
                continue
            t_obj.setAttribute(n, w)
    eel.expose(save_gui_element.__func__)

    @staticmethod
    def save():
        cls = Steuerung
        t_data = cls.c_intermediary.getObjectsAsDictionaryList()
        # print(t_data)
        t_path = cls.get_dir_path()
        if (t_path == ""):
            return None
        # print(t_path)
        cls.c_generator.write_files(t_path, t_data)  # NOTE
        cls.c_json.save(t_path)
    eel.expose(save.__func__)

    @staticmethod
    def delete_element(p_id: int):
        cls = Steuerung
        cls.c_intermediary.removeObject(p_id)
    eel.expose(delete_element.__func__)

    @staticmethod
    def create_btn() -> dict[str, Any]:
        cls = Steuerung
        t_id = cls.c_intermediary.createObject(ObjectEnum.BUTTON)
        t_data = cls.convert_attribut_to_js_data(
            cls.c_intermediary.getObject(t_id).getAttributesAsDictionary())
        # print(t_data)
        return t_data
    eel.expose(create_btn.__func__)

    @staticmethod
    def create_label() -> dict[str, Any]:
        cls = Steuerung
        t_id = cls.c_intermediary.createObject(ObjectEnum.LABEL)
        t_data = cls.convert_attribut_to_js_data(
            cls.c_intermediary.getObject(t_id).getAttributesAsDictionary())
        # print(t_data)
        return t_data
    eel.expose(create_label.__func__)

    @staticmethod
    def create_edit() -> dict[str, Any]:
        cls = Steuerung
        t_id = cls.c_intermediary.createObject(ObjectEnum.EDIT)
        t_data = cls.convert_attribut_to_js_data(
            cls.c_intermediary.getObject(t_id).getAttributesAsDictionary())
        # print(t_data)
        return t_data
    eel.expose(create_edit.__func__)

    @staticmethod
    def create_checkbox() -> dict[str, Any]:
        cls = Steuerung
        t_id = cls.c_intermediary.createObject(ObjectEnum.CHECKBOX)
        t_data = cls.convert_attribut_to_js_data(
            cls.c_intermediary.getObject(t_id).getAttributesAsDictionary())
        # print(t_data)
        return t_data
    eel.expose(create_checkbox.__func__)

    @staticmethod
    def create_canvas() -> dict[str, Any]:
        cls = Steuerung
        t_id = cls.c_intermediary.createObject(ObjectEnum.CANVAS)
        t_data = cls.convert_attribut_to_js_data(
            cls.c_intermediary.getObject(t_id).getAttributesAsDictionary())
        # print(t_data)
        return t_data
    eel.expose(create_canvas.__func__)

    @staticmethod
    def create_timer() -> dict[str, Any]:
        cls = Steuerung
        t_id = cls.c_intermediary.createObject(ObjectEnum.TIMER)
        t_data = cls.convert_attribut_to_js_data(
            cls.c_intermediary.getObject(t_id).getAttributesAsDictionary())
        # print(t_data)
        return t_data
    eel.expose(create_timer.__func__)


if __name__ == "__main__":
    if environ.get("DEV") != None:
        Steuerung.file = path.abspath(__file__)
        Steuerung.additional_files_path = "..\\additional_files"
    else:
        Steuerung.file = path.abspath(executable)
        Steuerung.additional_files_path = "additional_files"

    Steuerung.init()