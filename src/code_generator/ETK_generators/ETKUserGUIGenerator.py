from intermediary.objects.IBaseObject import IBaseObject
from ast import Module, stmt, FunctionDef, ClassDef, Pass, parse
from astor import to_source  # type:ignore
from typing import Optional
from .BaseETKGenerator import BaseETKGenerator
from ..ErrorMSGS import ParsingError

class PythonSyntaxError(ParsingError):
    def __init__(self) -> None:
        err_en: str = "The python code inside of the old \"UserGUI.py\" file, had a Syntax Error and could not be parsed (fix all Errors, to be able to export again)"
        err_dt: str = "Der Pythoncode aus der alten \"UserGUI.py\" Datei, hat Syntaxfehler und konnte aus diesem Grund nicht geparsed werden (behebe alle Fehler damit du wieder Exportieren kannst)"
        super().__init__(err_dt, err_en)

class UserGUINotFoundError(ParsingError):
    def __init__(self) -> None:
        err_en: str = "The UserGUI class was not found in the old \"UserGUI.py\" file"
        err_dt: str = "Die UserGUI Klasse wurde nicht in der alten \"UserGUI.py\" Datei gefunden"
        super().__init__(err_dt, err_en)

class ETKUserGUIGenerator(BaseETKGenerator):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def generate_file(cls, etk_objects: tuple[IBaseObject, ...], old_file:Optional[str]) -> tuple[str, str]:
        template: Module
        template = parse(cls._read_file(cls._join_relative_path("./templates/ETKgenerator/UserGUI.txt")))

        ast_old_file: Optional[Module] = None
        if old_file != None:
            try:
                ast_old_file = parse(old_file)
            except:
                raise PythonSyntaxError
        
        my_event_list: list[tuple[IBaseObject, Optional[str],
                                  str]] = cls._generate_event_list(etk_objects)
        
        previous_functions: dict[str, list[stmt]] = cls.__generate_previous_funcs_dict(ast_old_file)
        
        my_event_funcs, removed_events = cls._generate_event_funcs(my_event_list, previous_functions)

        for ast_object in template.body:
            if type(ast_object) == ClassDef and ast_object.name == "UserGUI":
                ast_object.body = my_event_funcs
                break
        else:
            raise UserGUINotFoundError

        ast_removed_events = cls.__removed_events_dict_to_ast(removed_events, ast_old_file)

        code: str = to_source(template)
        return code, to_source(ast_removed_events)

    @staticmethod
    def __generate_previous_funcs_dict(ast_old_file: Optional[Module]) -> dict[str, list[stmt]]:
        retval: dict[str, list[stmt]] = {}
        if ast_old_file is None:
            return retval
        for ast_object in ast_old_file.body:
            if type(ast_object) == ClassDef and ast_object.name == "UserGUI":
                for class_object in ast_object.body:
                    if type(class_object) == FunctionDef:
                        if class_object.name == "_on_init":
                            continue
                        if len(class_object.body) == 0:
                            continue
                        if len(class_object.body) == 1 and type(class_object.body[0]) == Pass:
                            continue
                        retval[class_object.name] = class_object.body
                return retval
        else:
            raise UserGUINotFoundError
    
    @staticmethod
    def __removed_events_dict_to_ast(removed_events: dict[str, list[stmt]], ast_old_file: Optional[Module]) -> Module:
        retval: Module = Module([], [])
        retval.body = []
        if ast_old_file is None:
            return retval
        for ast_object in ast_old_file.body:
            if type(ast_object) == ClassDef and ast_object.name == "UserGUI":
                for class_object in ast_object.body:
                    if type(class_object) == FunctionDef and class_object.name in removed_events.keys():
                        retval.body.append(class_object)
                return retval
        else:
            raise UserGUINotFoundError