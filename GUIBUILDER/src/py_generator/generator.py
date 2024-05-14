from intermediary_neu.objects.IBaseObject import IBaseObject
from .BaseGenerator import BaseGenerator
import os
from enum import Enum, auto
from typing import Optional
from .ETK_system_gui_generator import ETK_system_gui_generator
from .ETK_user_gui_generator import ETK_user_gui_generator
from autopep8 import fix_code # type:ignore

class SupportedFrameworks(Enum):
    ETK = auto()
    TGW = auto()

class generator(BaseGenerator):
    __REMOVED_EVENTS_ETK: str = "RemovedEvents.txt"
    __USER_GUI_NAME_ETK: str = "UserGUI.py"
    __SYSTEM_GUI_NAME_ETK: str = "SystemGUI.py"

    def __init__(self) -> None:
        self.__SYSTEM_GUI_GEN_ETK = ETK_system_gui_generator()
        self.__USER_GUI_GEN_ETK = ETK_user_gui_generator()
        super().__init__()

    def write_files(self, path: str, etk_objects:tuple[IBaseObject, ...], framework: SupportedFrameworks):
        if framework == SupportedFrameworks.ETK:
            old_user_gui: Optional[str] = None
            if os.path.exists(self._join_paths(path, self.__USER_GUI_NAME_ETK)):
                old_user_gui = self._read_file(self._join_paths(path, self.__USER_GUI_NAME_ETK))
            
            generated_user_gui: Optional[str] = None
            if old_user_gui != None:
                user_gui_region_start: int = old_user_gui.find("# region generated code")
                if user_gui_region_start == -1:
                    user_gui_region_start: int = old_user_gui.find("#region generated code")
                if user_gui_region_start == -1:
                    raise ValueError("Region for generated Code is not defined")            
                user_gui_region_end = self.__find_region_end(old_user_gui, user_gui_region_start)

                generated_user_gui = old_user_gui[user_gui_region_start:user_gui_region_end]
            
            system_gui: str = self.__SYSTEM_GUI_GEN_ETK.generate_file(etk_objects)

            user_gui, removed_events = self.__USER_GUI_GEN_ETK.generate_file(etk_objects, generated_user_gui)

            if old_user_gui == None:
                user_template: str = self._read_file(self._join_relative_path("./templates/write/UserGUI.txt"))
                user_gui = user_template.replace("#tag:generated_code#", user_gui)
                fix_code(user_gui)
                self.__write_file(self._join_paths(path, self.__USER_GUI_NAME_ETK), user_gui)
            else:
                old_user_gui = old_user_gui.replace(old_user_gui[user_gui_region_start:user_gui_region_end],"# region generated code\n\n" + user_gui + "\n") # type:ignore
                fix_code(old_user_gui)
                self.__write_file(self._join_paths(path, self.__USER_GUI_NAME_ETK), old_user_gui)

            if removed_events != "":
                old_removed_events: str = ""
                if os.path.exists(self._join_paths(path, self.__REMOVED_EVENTS_ETK)):
                    old_removed_events = self._read_file(self._join_paths(path, self.__REMOVED_EVENTS_ETK))
            
                all_removed_events: str = old_removed_events

                all_removed_events += "\n" + removed_events
                fix_code(all_removed_events)
                self.__write_file(self._join_paths(path, self.__REMOVED_EVENTS_ETK), all_removed_events)
            
            system_template: str = self._read_file(self._join_relative_path("./templates/write/SystemGUI.txt"))
            system_gui = system_template.replace("#tag:generated_code#", system_gui)
            fix_code(system_gui)
            self.__write_file(self._join_paths(path, self.__SYSTEM_GUI_NAME_ETK), system_gui)
            
        elif framework == SupportedFrameworks.TGW:
            pass
        else:
            raise ValueError(f"Selected framework ({framework.name}) is not supported")
    
    @staticmethod
    def __find_next(st: str, searches: tuple[str, ...], start: int = 0, end: Optional[int] = None):
        if end == None:
            end = len(st)
        erg: dict[str, int] = {}
        for s in searches:
            erg[s] = st.find(s, start, end)
        erg = {k: v for k, v in erg.items() if v != -1}
        return min(erg.items(), key=lambda v: v[1])


    @classmethod
    def __find_region_end(cls, st: str, start: int) -> int:
        index = start
        indent = 0
        while True:
            try:
                v, i = cls.__find_next(st, ("# region", "#region", "# endregion", "#endregion"), index)
            except ValueError:
                raise ValueError("regionend not found")
            if v in ["# region", "#region"]:
                indent += 1
            elif v in ["# endregion", "#endregion"]:
                indent -= 1
            if indent == 0:
                return i
            index = i+1 
    
    @staticmethod
    def __write_file(path: str, data: str):
        with open(path, "w") as f:
            f.write(data)