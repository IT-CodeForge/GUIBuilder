from typing import Optional

__VALID_FUNC_NAME_CHARACTER: list[str] = [
        "_", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
        "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
        "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
        ]
def __remainig_funcs_to_string(remaining_funcs: list[tuple[int, str]], old_file: str)-> str:
    retval: str = ""
    for index, _ in remaining_funcs:
        start_of_function: int = index - 1
        status: str = "NotFound"
        while status != "Finished":
            character: str = old_file[start_of_function]
            if status == "NotFound" and character in __VALID_FUNC_NAME_CHARACTER:
                status = "Found"
            if status == "Found" and character not in __VALID_FUNC_NAME_CHARACTER:
                status = "Finished"
                continue
            if start_of_function < 0:
                raise ValueError("Unable to find return type of function")
            start_of_function -= 1
        end_of_function: int = __find_func_end(__find_next(old_file, tuple("{"), index)[1], old_file)
        print(start_of_function)
        print(end_of_function)
        retval += old_file[start_of_function + 1:end_of_function + 1] + "\n\n"
    return retval


def __find_func_end(start_index: int, file: str) -> int:
    end_index = start_index
    counter = 1
    if file[start_index] != "{":
        raise ValueError("wrong index was supplied")
    while counter != 0:
        next_key, new_index = __find_next(file, ("{", "}", "\"", "//", "/*"), end_index + 1)
        end_index = new_index
        if next_key == "{":
            counter += 1
        elif next_key == "}":
            counter -= 1
        elif next_key == "\"":
            end_of_cpp_str: int = __find_next(file, tuple("\""), end_index + 1)[1]
            end_index = end_of_cpp_str
        elif next_key == "//":
            end_of_cpp_comment: int = __find_next(file, tuple("\n"), end_index + 1)[1]
            end_index = end_of_cpp_comment
        elif next_key == "/*":
            end_of_cpp_comment: int = __find_next(file, tuple("*/"), end_index + 1)[1]
            end_index = end_of_cpp_comment
    return end_index

def __find_next(st: str, searches: tuple[str, ...], start: int = 0, end: Optional[int] = None):
    if end is None:
        end = len(st)
    erg: dict[str, int] = {}
    for s in searches:
        erg[s] = st.find(s, start, end)
    erg = {k: v for k, v in erg.items() if v != -1}
    return min(erg.items(), key=lambda v: v[1])

if __name__ == "__main__":
    file = '#include "mmm"\n\nvoid GUI::temp()\n{\n}\n'
    print(file[5])
    print(__remainig_funcs_to_string([(file.find("GUI::"), "temp")], file))
