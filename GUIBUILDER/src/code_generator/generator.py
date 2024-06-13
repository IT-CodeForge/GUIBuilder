from intermediary_neu.objects.IBaseObject import IBaseObject
from .BaseGenerator import BaseGenerator
import os
from enum import Enum, auto
from typing import Optional
from .ETKSystemGUIGenerator import ETKSystemGUIGenerator
from .ETKUserGUIGenerator import ETKUserGUIGenerator
from .TGWSystemHeaderGenerator import TGWSystemHeaderGenerator
from .TGWSystemCPPGenerator import TGWSystemCPPGenerator
from .TGWUserHeaderGenerator import TGWUserHeaderGenerator
from .TGWUserCPPGenerator import TGWUserCPPGenerator
from autopep8 import fix_code # type:ignore

class UserError(Exception):
    def __init__(self, err_dt: str, err_en: str) -> None:
        self.err_dt = err_dt
        self.err_en = err_en
        super().__init__(self.err_en)

class ParsingError(UserError):
    def __init__(self, err_dt: str, err_en: str) -> None:
        super().__init__(err_dt, err_en)

class RegionMarkerIncompleteError(ParsingError):
    def __init__(self) -> None:
        err_en: str = "The \"generated code\" region was incomplete, this means, that either the head marker \"# region generated code\" was manipulated, or not enough \"# regionend\" markers were found"
        err_dt: str = "Die \"generated code\" Region ist unvollständig, dass bedeutet, dass entweder der Kopf-Marker \"# region generated code\" manipuliert wurde, oder es nicht genügend \"# regionend\" Marker gibt"
        super().__init__(err_dt, err_en)

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
    __SYSTEM_HEADER_GUI_GEN_TGW = TGWSystemHeaderGenerator()
    __SYSTEM_CPP_GUI_GEN_TGW = TGWSystemCPPGenerator()
    __USER_HEADER_GUI_GEN_TGW = TGWUserHeaderGenerator()
    __USER_CPP_GUI_GEN_TGW = TGWUserCPPGenerator()

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
                    raise RegionMarkerIncompleteError           
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
# region TGW
# region user header
            old_user_header_gui: Optional[str] = None
            if os.path.exists(cls._join_paths(path, cls.__USER_GUI_HEADER_NAME_TGW)):
                old_user_header_gui = cls._read_file(cls._join_paths(path, cls.__USER_GUI_HEADER_NAME_TGW))
            
            if old_user_header_gui != None:
                user_header_gui_region_start: int = old_user_header_gui.find("#pragma region generated code")
                if user_header_gui_region_start == -1:
                    raise RegionMarkerIncompleteError           
                user_header_gui_region_end = cls.__find_region_end_cpp(old_user_header_gui, user_header_gui_region_start)
            
            user_header_gui: str = cls.__USER_HEADER_GUI_GEN_TGW.generate_file(intermediary_objects)
            
            if old_user_header_gui is None:
                user_template: str = cls._read_file(cls._join_relative_path("./templates/TGWwrite/UserHeaderGUI.txt"))
                user_header_gui = user_template.replace("#tag:generated_code#\n", user_header_gui)
                cls.__write_file(cls._join_paths(path, cls.__USER_GUI_HEADER_NAME_TGW), user_header_gui)
            else:
                old_user_header_gui = old_user_header_gui.replace(old_user_header_gui[user_header_gui_region_start:user_header_gui_region_end],"#pragma region generated code\n\n" + user_header_gui) # type:ignore
                cls.__write_file(cls._join_paths(path, cls.__USER_GUI_HEADER_NAME_TGW), old_user_header_gui)
# endregion
# region user cpp
            old_user_cpp_gui: Optional[str] = None
            if os.path.exists(cls._join_paths(path, cls.__USER_GUI_CPP_NAME_TGW)):
                old_user_cpp_gui = cls._read_file(cls._join_paths(path, cls.__USER_GUI_CPP_NAME_TGW))
            
            read_user_cpp_gui: Optional[str] = None
            if old_user_cpp_gui != None:
                user_cpp_gui_region_start: int = old_user_cpp_gui.find("#pragma region generated code")
                if user_cpp_gui_region_start == -1:
                    raise RegionMarkerIncompleteError           
                user_cpp_gui_region_end = cls.__find_region_end_cpp(old_user_cpp_gui, user_cpp_gui_region_start)

                read_user_cpp_gui = old_user_cpp_gui[user_cpp_gui_region_start:user_cpp_gui_region_end]
            
            user_cpp_gui, removed_events = cls.__USER_CPP_GUI_GEN_TGW.generate_file(intermediary_objects, read_user_cpp_gui)

            if old_user_cpp_gui is None:
                user_template: str = cls._read_file(cls._join_relative_path("./templates/TGWwrite/UserCPPGUI.txt"))
                user_cpp_gui = user_template.replace("#tag:generated_code#\n", user_cpp_gui)
                cls.__write_file(cls._join_paths(path, cls.__USER_GUI_CPP_NAME_TGW), user_cpp_gui)
            else:
                old_user_cpp_gui = old_user_cpp_gui.replace(old_user_cpp_gui[user_cpp_gui_region_start:user_cpp_gui_region_end],"#pragma region generated code\n\n" + user_cpp_gui) # type:ignore
                cls.__write_file(cls._join_paths(path, cls.__USER_GUI_CPP_NAME_TGW), old_user_cpp_gui)
# region removed events            
            if removed_events != "":
                old_removed_events: str = ""
                if os.path.exists(cls._join_paths(path, cls.__REMOVED_EVENTS_TGW)):
                    old_removed_events = cls._read_file(cls._join_paths(path, cls.__REMOVED_EVENTS_TGW))
                
                all_removed_events: str = old_removed_events

                all_removed_events += "\n" + removed_events
                fix_code(all_removed_events)
                cls.__write_file(cls._join_paths(path, cls.__REMOVED_EVENTS_TGW), all_removed_events)
# endregion
# endregion            
# region system cpp
            system_cpp_template: str = cls._read_file(cls._join_relative_path("./templates/TGWwrite/SystemCPPGUI.txt"))

            system_cpp_gui_params, system_cpp_gui_constructor, system_cpp_gui_event_binds = cls.__SYSTEM_CPP_GUI_GEN_TGW.generate_file(intermediary_objects)

            system_cpp_gui: str = system_cpp_template.replace("#tag:main_window_params#", system_cpp_gui_params).replace("#tag:constructor_definition#", system_cpp_gui_constructor).replace("#tag:event_funcs_definition#", system_cpp_gui_event_binds)
            cls.__write_file(cls._join_paths(path, cls.__SYSTEM_GUI_CPP_NAME_TGW), system_cpp_gui)
# endregion
# region system header
            system_header_template: str = cls._read_file(cls._join_relative_path("./templates/TGWwrite/SystemHeaderGUI.txt"))

            system_header_gui_attributes, system_header_gui_func_declarations = cls.__SYSTEM_HEADER_GUI_GEN_TGW.generate_file(intermediary_objects)

            system_header_gui: str = system_header_template.replace("#tag:attributes#", system_header_gui_attributes).replace("#tag:function_declarations#", system_header_gui_func_declarations)
            cls.__write_file(cls._join_paths(path, cls.__SYSTEM_GUI_HEADER_NAME_TGW), system_header_gui)
# endregion
# endregion
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
                raise RegionMarkerIncompleteError
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
                raise RegionMarkerIncompleteError
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