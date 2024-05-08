from typing import Any, Optional

class ETK_python_code_generator:
    def __init__(self) -> None:
        pass

    def generate_function_head(self, indent: str, name: str, parameters: tuple[tuple[str, type, Any]], return_type: type)->str:
        retval = indent + "def " + name + "("
        for parameter in parameters:
            retval += parameter[0] + ": " + str(parameter[1])
            if parameter[2] != None:
                retval += "=" + str(parameter[2])
            retval += ", "
        if retval[-2:] == ", ":
            retval = retval[:-2]
        return  retval + ")->" + str(return_type) + ":\r\n"
    
    def generate_function_call(self, indent: str, name: str, parameters: tuple[str, Any])->str:
        retval = indent + name + "("
        for parameter in parameters:
            retval += parameter[0] + "=" + str(parameter[1])
            retval += ", "
        if retval[-2:] == ", ":
            retval = retval[:-2]
        return retval + ")"
    
    def generate_class_head(self, name: str, parent_class: Optional[str])->str:
        return "class " + name + ("" if parent_class == None else ("(" + parent_class + ")")) + ":\r\n"