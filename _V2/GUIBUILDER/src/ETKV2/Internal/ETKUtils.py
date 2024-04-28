from typing import Optional


def gen_col_from_int(col: Optional[int]) -> str:
    if col == None:
        return ""
    hold_str = hex(col)[2:]
    if len(hold_str) < 6:
        hold_str = "0"*(6-len(hold_str)) + hold_str
    return "#" + hold_str
