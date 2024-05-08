from typing import Callable
from vector2d import vector2d

from objects.IButton import IButton
from ast import * #type:ignore
import astor #type:ignore


def col_arr_to_col(arr: tuple[int, int, int]) -> int:
    return arr[0] << 16 | arr[1] << 8 | arr[2]

def arr_to_vec(arr: tuple[int, int]) -> str:
    return f"vector2d({arr[0]}, {arr[1]})"

button: Callable[[IButton], str] = lambda obj: f'self.element = ETKButton(self._tk_object, "{obj.text}", {arr_to_vec(obj.pos)}, {arr_to_vec(obj.size)}, {col_arr_to_col(obj.background_color)}, {col_arr_to_col(obj.text_color)})'

c = button(IButton(0))
print(c)
a = parse(c)
print(dump(a, indent=2))
