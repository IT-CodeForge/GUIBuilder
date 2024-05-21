from .BaseTGWGenerator import BaseTGWGenerator
from intermediary_neu.objects.IBaseObject import IBaseObject
from intermediary_neu.objects.ICanvas import ICanvas
from intermediary_neu.objects.IWindow import IWindow
from . import TGW_code_generator as tgw_gen
from typing import Optional

class TGW_user_generator(BaseTGWGenerator):
    __VALID_FUNC_NAME_CHARACTER: list[str] = [
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
        "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
        "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
        "_", "1", "2", "3", "4", "5", "6", "7", "8", "9"
        ]
    def __init__(self) -> None:
        super().__init__()
    
    def generate_file(self, tgw_objects: tuple[IBaseObject, ...], old_file:Optional[str]) -> tuple[str, str]:
        retval: str = self.__generate_includes(tgw_objects)
        event_dict: dict[str, list[tuple[IBaseObject, str]]] = self._generate_event_dict(tgw_objects)
        old_functions: tuple[tuple[int, str], ...] = ()
        if old_file == None:
            pass
        else:
            old_functions = self.__find_functions(old_file)
        retval += "\n"
        tempval, remaining_funcs = self.__generate_user_func_definition(event_dict, list(old_functions), "" if old_file == None else old_file)
        retval += tempval
        deleted_funcs: str = self.__remainig_funcs_to_string(remaining_funcs, "" if old_file == None else old_file)
        return retval, deleted_funcs
    
    @classmethod
    def __remainig_funcs_to_string(cls, remaining_funcs: list[tuple[int, str]], old_file: str)-> str:
        retval: str = ""
        for index, _ in remaining_funcs:
            start_of_function: int = index - 1
            status = "NotFound"
            while True:
                character: str = old_file[start_of_function]
                if status == "NotFound" and character in cls.__VALID_FUNC_NAME_CHARACTER:
                    status = "Found"
                if status == "Found" and character not in cls.__VALID_FUNC_NAME_CHARACTER:
                    break
                if start_of_function < 0:
                    raise ValueError("Unable to find return type of function")
                start_of_function -= 1
            end_of_function: int = cls.__find_func_end(cls.__find_next(old_file, tuple("{"), index)[1], old_file)
            retval += old_file[start_of_function + 1:end_of_function + 1] + "\n\n"
        return retval
    
    @staticmethod
    def __generate_includes(tgw_objects: tuple[IBaseObject, ...])-> str:
        retval: str = '#include "GUI.h"\n'
        for tgw_object in tgw_objects:
            if type(tgw_object) == IWindow:
                continue
            include: str = ""
            if type(tgw_object) == ICanvas:
                include = '#include "TGWCanvas.h"\n'
            else:
                include = f'#include "{tgw_gen.TYPE_TRANS.get(type(tgw_object), "")}.h"\n'
            if retval.find(include) == -1:
                retval += include
        return retval
    
    @classmethod
    def __find_functions(cls, file: str)-> tuple[tuple[int, str], ...]:
        temp_index: int = 0
        retval: list[tuple[int, str]] = []
        while True:
            try:
                func_candidate_index: int = file.find("GUI::", temp_index)
                if func_candidate_index == -1:
                    raise ValueError
                temp_index = func_candidate_index + 5
                my_char = file[func_candidate_index]
                while my_char != "(":
                    my_char = file[temp_index]
                    temp_index += 1
                    if my_char not in cls.__VALID_FUNC_NAME_CHARACTER:
                        continue
                return_tuple: tuple[int, str] = (func_candidate_index + 5, file[func_candidate_index + 5:temp_index - 1])
                retval.append(return_tuple)
            except:
                return tuple(retval)
    
    @classmethod #TODO: handle on construction
    def __generate_user_func_definition(cls, event_dict: dict[str, list[tuple[IBaseObject, str]]], old_functions: list[tuple[int, str]], old_file: str)-> tuple[str, list[tuple[int, str]]]:
        retval: str = "void GUI::on_construction()\n{\n"
        if "on_construction" in [oldfunc[1] for oldfunc in old_functions]:
            for file_index, name in old_functions:
                if name == "on_construction":
                    func_definition_start: int = old_file.find("{", file_index) + 1
                    func_definition_end: int = cls.__find_func_end(func_definition_start - 1, old_file)
                    retval += old_file[func_definition_start:func_definition_end]
                    old_functions.pop(file_index)
        retval += "}\n\n"
        for tgw_event in event_dict.keys():
            for user_event, event_type in event_dict.get(tgw_event, []):
                retval += "void GUI::" + tgw_gen.generate_event_head_own(event_type, user_event)
                retval += "\n{\n"
                for list_index, (file_index, name) in enumerate(old_functions):
                    if name.startswith(f"e{user_event.id}_") and name.endswith(f"_{event_type}"):
                        func_definition_start: int = old_file.find("{", file_index) + 1
                        func_definition_end: int = cls.__find_func_end(func_definition_start - 1, old_file)
                        retval += old_file[func_definition_start + 1:func_definition_end]
                        old_functions.pop(list_index)
                        break
                retval += "}\n"
        return retval, old_functions

    @classmethod
    def __find_func_end(cls, start_index: int, file: str) -> int:
        end_index = start_index
        counter = 1
        if file[start_index] != "{":
            raise ValueError("wrong index was supplied")
        while counter != 0:
            next_key, new_index = cls.__find_next(file, ("{", "}", "\"", "//", "/*"), end_index + 1)
            end_index = new_index
            if next_key == "{":
                counter += 1
            elif next_key == "}":
                counter -= 1
            elif next_key == "\"":
                end_of_cpp_str: int = file.find("\"", end_index + 1)
                end_index = end_of_cpp_str
            elif next_key == "//":
                end_of_cpp_comment: int = file.find("\n", end_index + 1)
                end_index = end_of_cpp_comment
            elif next_key == "/*":
                end_of_cpp_comment: int = file.find("*/", end_index + 1)
                end_index = end_of_cpp_comment
        return end_index
    
    @staticmethod
    def __find_next(st: str, searches: tuple[str, ...], start: int = 0, end: Optional[int] = None):
        if end == None:
            end = len(st)
        erg: dict[str, int] = {}
        for s in searches:
            erg[s] = st.find(s, start, end)
        erg = {k: v for k, v in erg.items() if v != -1}
        return min(erg.items(), key=lambda v: v[1])