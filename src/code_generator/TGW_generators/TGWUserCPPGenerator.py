from .BaseTGWGenerator import BaseTGWGenerator
from intermediary.objects.IBaseObject import IBaseObject
from intermediary.objects.ICanvas import ICanvas
from intermediary.objects.IWindow import IWindow
from . import TGWCodeGenerator as tgw_gen
from ..ErrorMSGS import ParsingError
from typing import Optional

class ReturnTypeError(ParsingError):
    def __init__(self, func_name: str) -> None:
        err_en: str = f"Could not parse the method \"{func_name}\" of the file \"UserGUI.cpp\" (could not find the returntype of the method)"
        err_dt: str = f"Konnte die Methode \"{func_name}\" der Datei \"UserGUI.cpp\" nicht parsen (Der rückgabetyp dieser Methode, konnte nicht gefunden werden)"
        super().__init__(err_dt, err_en)

class FunctionEndNotFound(ParsingError):
    def __init__(self, func_name: str) -> None:
        err_en: str = "Could not parse the method \"" + func_name + "\" of the file \"UserGUI.cpp\" (could not interpret the placement of curly-brackets (\"{\", \"}\") corectly)"
        err_dt: str = f"Konnte die Methode \"" + func_name + "\" der Datei \"UserGUI.cpp\" nicht parsen (konnte die platzierung der geschweiften Klammern (\"{\", \"}\") nicht richtig interpretieren)"
        super().__init__(err_dt, err_en)

"""
this generates the User cpp file, the file where the user of the GUI-Builder can edit the code
"""

class TGWUserCPPGenerator(BaseTGWGenerator):
    __VALID_FUNC_NAME_CHARACTER: list[str] = [
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
        "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
        "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
        "_", "1", "2", "3", "4", "5", "6", "7", "8", "9"
        ]
    def __init__(self) -> None:
        super().__init__()
    
    @classmethod
    def generate_file(cls, tgw_objects: tuple[IBaseObject, ...], old_file:Optional[str]) -> tuple[str, str]:
        """
        this returns two strings.
        the first string gets put inside the "generated code" region of the UserGUI (if it exists the existing file else the template by replacing #tag:generated_code#)
        the second string has the functions that got deleted while generating (events that got removed) !this only detects functions of the GUI class (only functions beginning with UserGUI::) other functions are not detected
        """
        retval: str = cls.__generate_includes(tgw_objects)
        event_dict: dict[str, list[tuple[IBaseObject, str]]] = cls._generate_event_dict(tgw_objects)
        old_functions: tuple[tuple[int, str], ...] = ()
        if old_file is None:
            pass
        else:
            old_functions = cls.__find_functions(old_file)
        retval += "\n"
        tempval, remaining_funcs = cls.__generate_user_func_definition(event_dict, list(old_functions), "" if old_file is None else old_file)
        retval += tempval
        deleted_funcs: str = cls.__remainig_funcs_to_string(remaining_funcs, "" if old_file is None else old_file)
        return retval, deleted_funcs
    
    @classmethod
    def __remainig_funcs_to_string(cls, remaining_funcs: list[tuple[int, str]], old_file: str)-> str:
        """
        extracts the functions which weren't regenerated (i.e. removed) and adds the to a string
        """
        retval: str = ""
        for index, name in remaining_funcs:
            start_of_function: int = index - 6
            status = "NotFound"
            while True:
                character: str = old_file[start_of_function]
                if status == "NotFound" and character in cls.__VALID_FUNC_NAME_CHARACTER:
                    status = "Found"
                if status == "Found" and character not in cls.__VALID_FUNC_NAME_CHARACTER:
                    break
                if start_of_function < 0:
                    raise ReturnTypeError(name)
                start_of_function -= 1
            try:
                end_of_function: int = cls.__find_func_end(cls.__find_next(old_file, tuple("{"), index)[1], old_file)
            except:
                raise FunctionEndNotFound(name)
            retval += old_file[start_of_function + 1:end_of_function + 1] + "\n\n"
        return retval
    
    @staticmethod
    def __generate_includes(tgw_objects: tuple[IBaseObject, ...])-> str:
        """
        generates all the necessary includes
        """
        retval: str = '#include "UserGUI.h"\n'
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
        """
        finds the functions in the oldfile that was provided and returns a tuplpe, which contains the name af the function and the index in the oldfile
        """
        temp_index: int = 0
        retval: list[tuple[int, str]] = []
        while True:
            try:
                func_candidate_index: int = file.find("UserGUI::", temp_index)
                if func_candidate_index == -1:
                    raise ValueError
                temp_index = func_candidate_index + 5
                my_char = file[func_candidate_index]
                while my_char != "(":
                    my_char = file[temp_index]
                    temp_index += 1
                    if my_char not in cls.__VALID_FUNC_NAME_CHARACTER:
                        continue
                return_tuple: tuple[int, str] = (func_candidate_index + 5, file[func_candidate_index + len("UserGUI::"):temp_index - 1])
                retval.append(return_tuple)
            except:
                return tuple(retval)
    
    @classmethod
    def __generate_user_func_definition(cls, event_dict: dict[str, list[tuple[IBaseObject, str]]], old_functions: list[tuple[int, str]], old_file: str)-> tuple[str, list[tuple[int, str]]]:
        """
        generates all the functions the user can manipulate, if it found an old version in the oldfile
        (meaning same id and event type(name doesn't need to match since user can change name)) it copies the contents af the old event
        """
        retval: str = ""
        for tgw_event in event_dict.keys():
            for user_event, event_type in event_dict.get(tgw_event, []):
                retval += "void UserGUI::" + tgw_gen.generate_event_head_own(event_type, user_event)
                retval += "\n{"
                for list_index, (file_index, name) in enumerate(old_functions):
                    if name.startswith(f"e{user_event.id}_") and name.endswith(f"_{event_type}"):
                        func_definition_start: int = old_file.find("{", file_index) + 1
                        try:
                            func_definition_end: int = cls.__find_func_end(func_definition_start - 1, old_file)
                        except:
                            raise FunctionEndNotFound(name)
                        retval += old_file[func_definition_start:func_definition_end]
                        old_functions.pop(list_index)
                        break
                else:
                    retval += "\n"
                retval += "}\n\n"
        return retval, old_functions

    @classmethod
    def __find_func_end(cls, start_index: int, file: str) -> int:
        """
        given the index of the start of a function (meaning the index of the first "{") it return the index of the end of the function
        it considers invalid "{", "}" which might be located in strings or comments
        """
        end_index = start_index
        counter = 1
        if file[start_index] != "{":
            raise ValueError
        while counter != 0:
            next_key, new_index = cls.__find_next(file, ("{", "}", "\"", "//", "/*"), end_index + 1)
            end_index = new_index
            if next_key == "{":
                counter += 1
            elif next_key == "}":
                counter -= 1
            elif next_key == "\"":
                end_of_cpp_str: int = file.find("\"", end_index + 1)
                if end_of_cpp_str == -1:
                    raise ValueError
                end_index = end_of_cpp_str
            elif next_key == "//":
                end_of_cpp_comment: int = file.find("\n", end_index + 1)
                if end_of_cpp_comment == -1:
                    raise ValueError
                end_index = end_of_cpp_comment
            elif next_key == "/*":
                end_of_cpp_comment: int = file.find("*/", end_index + 1)
                if end_of_cpp_comment == -1:
                    raise ValueError
                end_index = end_of_cpp_comment
        return end_index
    
    @staticmethod
    def __find_next(st: str, searches: tuple[str, ...], start: int = 0, end: Optional[int] = None):
        """
        finds the next occurrence from a list of strings inside the mainstring
        """
        if end is None:
            end = len(st)
        erg: dict[str, int] = {}
        for s in searches:
            erg[s] = st.find(s, start, end)
        erg = {k: v for k, v in erg.items() if v != -1}
        return min(erg.items(), key=lambda v: v[1])