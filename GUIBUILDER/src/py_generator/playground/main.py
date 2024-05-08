# Namesyntax: id_name_eventtype

import os
import ast
import astor #type: ignore

if __name__ == "__main__":
    myfile: str
    mypath = os.path.join(os.path.split(__file__)[0], "code1.py")
    with open(mypath, "r") as f:
        myfile = f.read()
    
    ast_module: ast.Module = ast.parse(myfile)

    for e in ast_module.body:
        if type(e) == ast.ClassDef:
            if e.name == "Test":
                cls = e
                break
    else:
        raise ValueError("No class found")
    
    funcs_with_content: dict[str, list[ast.stmt]] = {e.name: e.body for e in cls.body if type(e) == ast.FunctionDef}
        

    mypath = os.path.join(os.path.split(__file__)[0], "ast_list.txt")

    ast_list: str = ast.dump(ast_module, indent=4)

    with open(mypath, "w") as f:
        f.write(ast_list)
    
    new_code: str = astor.to_source(ast_module) #type: ignore

    mypath = os.path.join(os.path.split(__file__)[0], "code2.py")

    with open(mypath, "w") as f:
        f.write(new_code)