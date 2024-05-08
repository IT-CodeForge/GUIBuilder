import os.path
from ..intermediary_neu.objects.IBaseObject import IBaseObject
from .ETK_static_GUI_Generator import ETK_static_GUI_Generator
from typing import Any

class ETK_Generator:
    def __init__(self) -> None:
        self.__static_GUI: str = "GUI.py"
        self.__user_GUI: str = "User_GUI.py"

        self.__type_translation: dict[str, str] = {
            "button": "ETKButton",
            "window": "ETKMainWindow",
            "timer": "ETKTimer",
            "label": "ETKLabel",
            "edit": "ETKEdit",
            "checkbox": "ETKCheckBox",
            "timer": "ETKTimer",
            "canvas": "ETKCanvas"}
        
        self.__static_GUI_generator = ETK_static_GUI_Generator()
        pass

    def write_files(self, path: str, objects: list[IBaseObject]):
        self.__write_data(path + self.__static_GUI, self.__static_GUI_generator.write_file(objects))

    def __write_data(self, file: str, data: str):
        with open(file, "w") as f:
            f.write(data)
    
    def __write_lines(self, file: str, lines: list[str]):
        with open(file, "w") as f:
            f.writelines(lines)

if __name__ == "__main__":
    #code which tests evry functionality
    myGenerator: ETK_Generator = ETK_Generator()
    objects = [{"type": "window", "position": [10,10], "size": [1024,512], "text": "Hallo", "backgroundColor": [12,23,34], "eventMouseMove": True},
               {"type": "button", "name": "einButton", "position": [10,10], "size": [128,32], "text": "Knopf", "eventPressed": True, "eventChanged": False},
               {"type": "checkbox", "name": "meineCheckbox", "position": [10,52], "size": [128,32], "text": "ich bin eine Checkbox", "eventChanged": True, "checked": False},
               {"id": 0, "type": "timer", "name": "einTimer", "interval": 1000, "enabled": True},
               {"type": "canvas", "name": "einCanvas", "position": [148,10], "size": [138,138], "backgroundColor": [255,0,0]},
               {"type": "label", "name": "einLabel", "position": [10, 94], "size": [12, 128], "text": "Ich bin ein label"},
               {"type": "edit", "name": "einEdit", "position": [148, 94], "size": [12, 128], "text": "Ich bin ein edit", "multipleLines": True, "eventChanged": True}]
    #myGenerator.write_files("", objects)