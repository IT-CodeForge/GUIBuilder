from ..intermediary_neu.objects.IBaseObject import IBaseObject
import os
from enum import Enum, auto
from typing import Optional

class SupportedFrameworks(Enum):
    ETK = auto()
    TGW = auto()

class generator:
    def __init__(self) -> None:
        self.__user_gui_name_etk: str = "UserGUI.py"
        self.__system_gui_name_etk: str = "SystemGUI.py"
        pass

    def write_files(self, path: str, etk_objects:tuple[IBaseObject], framework: SupportedFrameworks):
        if framework == SupportedFrameworks.ETK:
            old_user_gui: Optional[str] = None
            if os.path.exists(self.join_paths(path, self.__user_gui_name_etk)):
                old_user_gui = self.read_file(self.join_paths(path, self.__user_gui_name_etk))
            
        elif framework == SupportedFrameworks.TGW:
            pass
        else:
            raise ValueError(f"Selected framework ({framework.name}) is not supported")

    def read_file(self, path: str) -> str:
        retval: str = ""
        with open(path, "r") as f:
            retval = f.read()
        return retval
    
    def write_file(self, path: str, data: str):
        with open(path, "w") as f:
            f.write(data)
    
    def join_paths(self, starting_path: str, following_path: str) -> str:
        return os.path.join(starting_path, following_path)
    def join_relative_path(self, relative_path: str) -> str:
        return os.path.join(os.path.split(__file__)[0], relative_path)