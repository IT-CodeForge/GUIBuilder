from intermediary_neu.objects.IBaseObject import IBaseObject
from .BaseGenerator import BaseGenerator
import os
from enum import Enum, auto
from typing import Optional
from .ETKSystemGUIGenerator import ETKSystemGUIGenerator
from .ETKUserGUIGenerator import ETKUserGUIGenerator
from .TGWSystemHeaderGenerator import TGWHeaderGenerator
from .TGWSystemCPPGenerator import TGWSystemCPPGenerator
from .TGWUserCPPGenerator import TGWUserCPPGenerator
from autopep8 import fix_code # type:ignore

class SupportedFrameworks(Enum):
    ETK = auto()
    TGW = auto()

class Generator(BaseGenerator):
    __REMOVED_EVENTS_ETK: str = "RemovedEvents.txt"
    __USER_GUI_NAME_ETK: str = "UserGUI.py"
    __SYSTEM_GUI_NAME_ETK: str = "SystemGUI.py"
    __REMOVED_EVENTS_TGW: str = "RemovedEvents.txt"
    __USER_GUI_CPP_NAME_TGW: str = "UserGUI.cpp"
    __USER_GUI_HEADER_NAME_TGW: str = "UserGUI.h"
    __SYSTEM_GUI_CPP_NAME_TGW: str = "SystemGUI.cpp"
    __SYSTEM_GUI_HEADER_NAME_TGW: str = "SystemGUI.h"
    __SYSTEM_GUI_GEN_ETK = ETKSystemGUIGenerator()
    __USER_GUI_GEN_ETK = ETKUserGUIGenerator()
    __HEADER_GUI_GEN_TGW = TGWHeaderGenerator()
    __SYSTEM_GUI_GEN_TGW = TGWSystemCPPGenerator()
    __USER_GUI_GEN_TGW = TGWUserCPPGenerator()

    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def write_files(cls, path: str, intermediary_objects:tuple[IBaseObject, ...], framework: SupportedFrameworks):
        if framework == SupportedFrameworks.ETK:
            old_user_gui: Optional[str] = None
            if os.path.exists(cls._join_paths(path, cls.__USER_GUI_NAME_ETK)):
                old_user_gui = cls._read_file(cls._join_paths(path, cls.__USER_GUI_NAME_ETK))
            
            read_user_gui: Optional[str] = None
            if old_user_gui != None:
                user_gui_region_start: int = old_user_gui.find("# region generated code")
                if user_gui_region_start == -1:
                    user_gui_region_start: int = old_user_gui.find("#region generated code")
                if user_gui_region_start == -1:
                    raise ValueError("Region for generated Code is not defined")            
                user_gui_region_end = cls.__find_region_end_python(old_user_gui, user_gui_region_start)

                read_user_gui = old_user_gui[user_gui_region_start:user_gui_region_end]
            
            system_gui: str = cls.__SYSTEM_GUI_GEN_ETK.generate_file(intermediary_objects)

            user_gui, removed_events = cls.__USER_GUI_GEN_ETK.generate_file(intermediary_objects, read_user_gui)

            if old_user_gui is None:
                user_template: str = cls._read_file(cls._join_relative_path("./templates/ETKwrite/UserGUI.txt"))
                user_gui = user_template.replace("#tag:generated_code#", user_gui)
                fix_code(user_gui)
                cls.__write_file(cls._join_paths(path, cls.__USER_GUI_NAME_ETK), user_gui)
            else:
                old_user_gui = old_user_gui.replace(old_user_gui[user_gui_region_start:user_gui_region_end],"# region generated code\n\n" + user_gui + "\n") # type:ignore
                fix_code(old_user_gui)
                cls.__write_file(cls._join_paths(path, cls.__USER_GUI_NAME_ETK), old_user_gui)

            if removed_events != "":
                old_removed_events: str = ""
                if os.path.exists(cls._join_paths(path, cls.__REMOVED_EVENTS_ETK)):
                    old_removed_events = cls._read_file(cls._join_paths(path, cls.__REMOVED_EVENTS_ETK))
            
                all_removed_events: str = old_removed_events

                all_removed_events += "\n" + removed_events
                fix_code(all_removed_events)
                cls.__write_file(cls._join_paths(path, cls.__REMOVED_EVENTS_ETK), all_removed_events)
            
            system_template: str = cls._read_file(cls._join_relative_path("./templates/ETKwrite/SystemGUI.txt"))
            system_gui = system_template.replace("#tag:generated_code#", system_gui)
            fix_code(system_gui)
            cls.__write_file(cls._join_paths(path, cls.__SYSTEM_GUI_NAME_ETK), system_gui)
            
        elif framework == SupportedFrameworks.TGW:
            old_user_gui: Optional[str] = None
            if os.path.exists(cls._join_paths(path, cls.__USER_GUI_CPP_NAME_TGW)):
                old_user_gui = cls._read_file(cls._join_paths(path, cls.__USER_GUI_CPP_NAME_TGW))
            
            read_user_gui: Optional[str] = None
            if old_user_gui != None:
                user_gui_region_start: int = old_user_gui.find("#pragma region generated code")
                if user_gui_region_start == -1:
                    raise ValueError("Region for generated Code is not defined")            
                user_gui_region_end = cls.__find_region_end_cpp(old_user_gui, user_gui_region_start)

                read_user_gui = old_user_gui[user_gui_region_start:user_gui_region_end]
            
            user_gui, removed_events = cls.__USER_GUI_GEN_TGW.generate_file(intermediary_objects, read_user_gui)

            system_gui_params, system_gui_constructor, system_gui_event_binds = cls.__SYSTEM_GUI_GEN_TGW.generate_file(intermediary_objects)

            header_gui_attributes, header_gui_func_declarations = cls.__HEADER_GUI_GEN_TGW.generate_file(intermediary_objects)

            if old_user_gui is None:
                user_template: str = cls._read_file(cls._join_relative_path("./templates/TGWwrite/UserCPPGUI.txt"))
                user_gui = user_template.replace("#tag:generated_code#\n", user_gui)
                cls.__write_file(cls._join_paths(path, cls.__USER_GUI_CPP_NAME_TGW), user_gui)
            else:
                old_user_gui = old_user_gui.replace(old_user_gui[user_gui_region_start:user_gui_region_end],"#pragma region generated code\n\n" + user_gui) # type:ignore
                cls.__write_file(cls._join_paths(path, cls.__USER_GUI_CPP_NAME_TGW), old_user_gui)
            
            if removed_events != "":
                old_removed_events: str = ""
                if os.path.exists(cls._join_paths(path, cls.__REMOVED_EVENTS_TGW)):
                    old_removed_events = cls._read_file(cls._join_paths(path, cls.__REMOVED_EVENTS_TGW))
                
                all_removed_events: str = old_removed_events

                all_removed_events += "\n" + removed_events
                fix_code(all_removed_events)
                cls.__write_file(cls._join_paths(path, cls.__REMOVED_EVENTS_TGW), all_removed_events)
            
            system_template: str = cls._read_file(cls._join_relative_path("./templates/TGWwrite/SystemCPPGUI.txt"))
            system_gui: str = system_template.replace("#tag:main_window_params#", system_gui_params).replace("#tag:constructor_definition#", system_gui_constructor).replace("#tag:event_funcs_definition#", system_gui_event_binds)
            cls.__write_file(cls._join_paths(path, cls.__SYSTEM_GUI_CPP_NAME_TGW), system_gui)

            header_template: str = cls._read_file(cls._join_relative_path("./templates/TGWwrite/SystemHeaderGUI.txt"))
            header_gui: str = header_template.replace("#tag:attributes#", header_gui_attributes).replace("#tag:function_declarations#", header_gui_func_declarations)
            cls.__write_file(cls._join_paths(path, cls.__SYSTEM_GUI_HEADER_NAME_TGW), header_gui)
        else:
            raise ValueError(f"Selected framework ({framework.name}) is not supported")
    
    @staticmethod
    def __find_next(st: str, searches: tuple[str, ...], start: int = 0, end: Optional[int] = None):
        if end is None:
            end = len(st)
        erg: dict[str, int] = {}
        for s in searches:
            erg[s] = st.find(s, start, end)
        erg = {k: v for k, v in erg.items() if v != -1}
        return min(erg.items(), key=lambda v: v[1])


    @classmethod
    def __find_region_end_python(cls, st: str, start: int) -> int:
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
    
    @classmethod
    def __find_region_end_cpp(cls, st: str, start: int) -> int:
        index = start
        indent = 0
        while True:
            try:
                v, i = cls.__find_next(st, ("#pragma region", "#pragma endregion"), index)
            except ValueError:
                raise ValueError("regionend not found")
            if v == "#pragma region":
                indent += 1
            elif v == "#pragma endregion":
                indent -= 1
            if indent == 0:
                return i
            index = i+1 
    
    @staticmethod
    def __write_file(path: str, data: str):
        with open(path, "w") as f:
            f.write(data)