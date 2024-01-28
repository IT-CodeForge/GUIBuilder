from os import devnull, environ
import sys
if environ.get("DEV") == None:
    # NOTE: Release: Disables print(), etc
    sys.stdout = sys.stderr = open(devnull, 'w')

from typing import Any
from os import path, mkdir
from sys import executable
import requests
import shutil
import eel
from tkinter import Tk, filedialog as fd

from MSGBox import MSGBox
from generator.TGW_generator import *
from intermediary.json import *
from intermediary.intermediary import *

"""
MIN & MAX_RELEASE:
MIN_RELEASE: release without browser -> browser will be downlaoded.
MAX_RELEASE: release with browser inside of exe

To enable MIN_RELEASE:
  - comment everything with "MIN_Release" behind the code line in.
  - comment everything with "MAX_RELEASE" behind the code line out.
  - delete .\\additional_files\\brave
"""


class WindowModes(Enum):
    default = None
    app = 1
    browser = 2


g_window_mode: WindowModes = WindowModes.app
g_dev_mode: bool


class Steuerung:

    __c_intermediary: Intermediary
    __c_generator: TGW_Generator
    __c_json: JSON
    __c_window_id: int
    c_file: str
    c_additional_files_path: str
    __c_save_path: str

    application_name = "GUI-Builder"
    protable_browser_dir_path = rf'{environ["appdata"]}\portable_brave_browser'
    portable_brower_exe_path = rf'{protable_browser_dir_path}\Brave.exe'
    protable_browser_download_url = "https://privat.kergerbw.de/public/Brave_Portable.zip"
    temp_folder_path = rf'{environ["TMP"]}\{application_name}'
    temp_portable_browser_zip_path = rf'{temp_folder_path}\Portable_Browser.zip'

    @classmethod
    def init(cls):
        cls.__c_intermediary = Intermediary()
        cls.__c_window_id = cls.__c_intermediary.createObject(
            ObjectEnum.WINDOW)

        cls.__c_generator = TGW_Generator()

        cls.__c_json = JSON(cls.__c_intermediary)

        cls.__c_save_path = f"{path.split(cls.c_file)[0]}"

        # if g_window_mode == WindowModes.app: # MIN_Release -> see note above
        # cls.__download_browser_if_not_installed() # MIN_Release -> see note above

        import os
        t_additional_files = f"{os.path.split(__file__)[0]}\\{cls.c_additional_files_path}"

        eel.init(f'{t_additional_files}\\gui')
        # eel.brw.set_path('chrome', cls.portable_brower_exe_path) # MIN_Release -> see note above
        # MAX_Release -> see note above
        eel.brw.set_path('chrome', f'{t_additional_files}\\brave\\brave.exe')
        if (not g_dev_mode and g_window_mode == WindowModes.default) or g_window_mode == WindowModes.app:
            # NOTE: Realease-Mode
            eel.start('main.html', cmdline_args=['--start-maximized'])
        else:
            # NOTE: Dev-Mode
            eel.start('main.html', mode="firefox")

    @classmethod
    def __resetData(cls, reset_path=True):
        cls.__c_intermediary = Intermediary()
        cls.__c_window_id = cls.__c_intermediary.createObject(
            ObjectEnum.WINDOW)

        cls.__c_generator = TGW_Generator()

        cls.__c_json = JSON(cls.__c_intermediary)

        if reset_path:
            cls.__c_save_path = f"{path.split(cls.c_file)[0]}"

    @classmethod
    def __download_browser_if_not_installed(cls):
        if not path.isdir(cls.protable_browser_dir_path):
            MSGBox.create_async_msg_box(f"{cls.application_name}: Browser Download",
                                        "Der Browser wird nun heruntergeladen!\nDies kann etwas dauern.", MSGBox.STYLES.OK)
            mkdir(cls.temp_folder_path)
            r = requests.get(cls.protable_browser_download_url, verify=False)
            with open(cls.temp_portable_browser_zip_path, "wb") as f:
                f.write(r.content)
            mkdir(cls.protable_browser_dir_path)
            shutil.unpack_archive(
                cls.temp_portable_browser_zip_path, cls.protable_browser_dir_path)
            shutil.rmtree(cls.temp_folder_path)

    @staticmethod
    def gui_init() -> dict[str, Any]:
        cls = Steuerung
        cls.__resetData()
        return cls.__convert_attribut_to_js_data(cls.__c_intermediary.getObject(cls.__c_window_id).getAttributesAsDictionary())
    eel.expose(gui_init.__func__)

    @staticmethod
    def __convert_attribut_to_js_data(p_attribut) -> dict[str, any]:
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
            t_return["event_double_pressed"] = p_attribut["eventDoublePressed"]

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
    def __convert_attribut_from_js_data(p_attribut) -> dict[str, any]:
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
            t_return["eventDoublePressed"] = p_attribut["event_double_pressed"]

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

    # Öffnet TKinter Fenster, um Filedialoge zu öffnen

    @classmethod
    def __get_load_file_path(cls) -> str:
        root = Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)
        t_initialdir_path = cls.__c_save_path
        file = fd.askopenfilename(
            filetypes=[("JSON", ".json")], initialdir=t_initialdir_path)
        if file != "":
            cls.__c_save_path = path.split(file)[0]
        return file

    @classmethod
    def __get_save_file_path(cls) -> str:
        root = Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)
        t_initialdir_path = cls.__c_save_path
        file = fd.asksaveasfilename(filetypes=[(
            "JSON", ".json")], initialdir=t_initialdir_path, defaultextension=".json")
        if file != "":
            cls.__c_save_path = path.split(file)[0]
        return file

    @classmethod
    def __get_dir_path(cls) -> str:
        root = Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)
        t_initialdir_path = cls.__c_save_path
        t_path = fd.askdirectory(initialdir=t_initialdir_path)
        if t_path != "":
            cls.__c_save_path = t_path
        return t_path

    # Läd alle GUI-Elemente vom File

    @staticmethod
    def load_gui_elements() -> list[dict[str, Any]]:
        cls = Steuerung
        t_path = cls.__get_load_file_path()
        if (t_path == ""):
            return None
        cls.__resetData(False)
        cls.__c_json.load(t_path)
        t_objekts = []
        # print("\n\n\n")
        for o in cls.__c_intermediary.getObjects():
            t_objekts.append(cls.__convert_attribut_to_js_data(
                o.getAttributesAsDictionary()))
            # print(o.getAttributesAsDictionary())
        # print(t_objekts)
        return t_objekts
    eel.expose(load_gui_elements.__func__)

    # Speichert EIN GUI-Element in den Zwischenspeicher
    @staticmethod
    def save_gui_element(p_attributes: dict[str, any]):
        cls = Steuerung
        # print(p_attributes)
        t_attributes = cls.__convert_attribut_from_js_data(p_attributes)
        # print(t_attributes)
        t_obj = cls.__c_intermediary.getObject(p_attributes["id"])
        for n, w in t_attributes.items():
            if n in ("id", "type"):
                continue
            t_obj.setAttribute(n, w)
    eel.expose(save_gui_element.__func__)

    # Speichert ALLE GUI-Elemente ins File
    @staticmethod
    def save():
        cls = Steuerung
        t_data = cls.__c_intermediary.getObjectsAsDictionaryList()
        # print(t_data)
        t_path = cls.__get_save_file_path()
        if (t_path == ""):
            return None
        # print(t_path)
        cls.__c_json.save(t_path)
    eel.expose(save.__func__)

    @staticmethod
    def export_to_cpp():
        cls = Steuerung
        t_data = cls.__c_intermediary.getObjectsAsDictionaryList()
        # print(t_data)
        t_path = cls.__get_dir_path()
        if (t_path == ""):
            return None
        # print(t_path)
        cls.__c_generator.write_files(t_path, t_data)
    eel.expose(export_to_cpp.__func__)

    @staticmethod
    def delete_element(p_id: int):
        cls = Steuerung
        cls.__c_intermediary.removeObject(p_id)
    eel.expose(delete_element.__func__)

    # Erstellt die Elemente

    @staticmethod
    def create_btn() -> dict[str, Any]:
        cls = Steuerung
        t_id = cls.__c_intermediary.createObject(ObjectEnum.BUTTON)
        t_data = cls.__convert_attribut_to_js_data(
            cls.__c_intermediary.getObject(t_id).getAttributesAsDictionary())
        # print(t_data)
        return t_data
    eel.expose(create_btn.__func__)

    @staticmethod
    def create_label() -> dict[str, Any]:
        cls = Steuerung
        t_id = cls.__c_intermediary.createObject(ObjectEnum.LABEL)
        t_data = cls.__convert_attribut_to_js_data(
            cls.__c_intermediary.getObject(t_id).getAttributesAsDictionary())
        # print(t_data)
        return t_data
    eel.expose(create_label.__func__)

    @staticmethod
    def create_edit() -> dict[str, Any]:
        cls = Steuerung
        t_id = cls.__c_intermediary.createObject(ObjectEnum.EDIT)
        t_data = cls.__convert_attribut_to_js_data(
            cls.__c_intermediary.getObject(t_id).getAttributesAsDictionary())
        # print(t_data)
        return t_data
    eel.expose(create_edit.__func__)

    @staticmethod
    def create_checkbox() -> dict[str, Any]:
        cls = Steuerung
        t_id = cls.__c_intermediary.createObject(ObjectEnum.CHECKBOX)
        t_data = cls.__convert_attribut_to_js_data(
            cls.__c_intermediary.getObject(t_id).getAttributesAsDictionary())
        # print(t_data)
        return t_data
    eel.expose(create_checkbox.__func__)

    @staticmethod
    def create_canvas() -> dict[str, Any]:
        cls = Steuerung
        t_id = cls.__c_intermediary.createObject(ObjectEnum.CANVAS)
        t_data = cls.__convert_attribut_to_js_data(
            cls.__c_intermediary.getObject(t_id).getAttributesAsDictionary())
        # print(t_data)
        return t_data
    eel.expose(create_canvas.__func__)

    @staticmethod
    def create_timer() -> dict[str, Any]:
        cls = Steuerung
        t_id = cls.__c_intermediary.createObject(ObjectEnum.TIMER)
        t_data = cls.__convert_attribut_to_js_data(
            cls.__c_intermediary.getObject(t_id).getAttributesAsDictionary())
        # print(t_data)
        return t_data
    eel.expose(create_timer.__func__)


if __name__ == "__main__":
    # Prüft ob es in VS-Code oder als Binary vorliegt.
    if environ.get("DEV") != None:
        Steuerung.c_file = path.abspath(__file__)
        Steuerung.c_additional_files_path = "..\\additional_files"
        g_dev_mode = True
    else:
        Steuerung.c_file = path.abspath(executable)
        Steuerung.c_additional_files_path = "additional_files"
        g_dev_mode = False

    Steuerung.init()
