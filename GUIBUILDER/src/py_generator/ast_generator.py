from ast import FunctionDef, Expr, Call, Constant, arguments, Name, arg, keyword, Subscript, Load, Tuple
from typing import Optional, Any

def generate_event_definition(event_func_name: str) -> FunctionDef:
    my_elts: list[Name] = [Name(id="ETKBaseOblect", ctx=Load()), Name(id="ETKEvents", ctx=Load()), Name(id="Any", ctx=Load())]
    my_subscript: Subscript = Subscript(value=Name(id="tuple", ctx=Load()), slice=Tuple(elts=my_elts), ctx=Load())
    my_arg: arg = arg(arg="params", annotation=my_subscript)
    arg_list: list[arg] = [my_arg]
    ast_arguments = arguments(args=arg_list)
    return FunctionDef(name=event_func_name, args=ast_arguments)

def generate_function_call() -> Expr:
    pass

#WIP
def generate_keyword_list(func_arguments: tuple[tuple[str, Any]]) -> list[keyword]:
    pass