from ast import stmt, parse
from typing import Callable
from intermediary.objects.IBaseObjectWidgetVisible import IBaseObjectWidgetVisible
from intermediary.objects.IBaseObjectWidgetText import IBaseObjectWidgetText
from intermediary.objects.IBaseObject import IBaseObject
from intermediary.objects.IButton import IButton
from intermediary.objects.ICanvas import ICanvas
from intermediary.objects.ICheckbox import ICheckbox
from intermediary.objects.IEdit import IEdit
from intermediary.objects.ILabel import ILabel
from intermediary.objects.ITimer import ITimer
from intermediary.objects.IWindow import IWindow


# region utils
__col_arr_to_col: Callable[[tuple[int, int, int]], int] = lambda arr: arr[0] << 16 | arr[1] << 8 | arr[2]

__arr_to_vec: Callable[[tuple[int, int]], str] = lambda arr: f"Vector2d({arr[0]}, {arr[1]})"

__event_func_name: Callable[[IBaseObject, str], str] = lambda obj, intermediary_event_type: f"e{obj.id}_{obj.name}_{intermediary_event_type}"
# endregion

# region generate stuff
__visible_object: Callable[[IBaseObjectWidgetVisible], str] = lambda obj: f"pos={__arr_to_vec(obj.pos)}, size={__arr_to_vec(obj.size)}, background_color={__col_arr_to_col(obj.background_color)}"

__text_object: Callable[[IBaseObjectWidgetText], str] = lambda obj: f"text='{obj.text}', text_color={__col_arr_to_col(obj.text_color)}"

button: Callable[[IButton], stmt]     = lambda obj: parse(f"self.e{obj.id}_{obj.name} = ETKButton(main=self._main, {__text_object(obj)}, {__visible_object(obj)})").body[0]
checkbox: Callable[[ICheckbox], stmt] = lambda obj: parse(f"self.e{obj.id}_{obj.name} = ETKCheckbox(main=self._main, {__text_object(obj)}, {__visible_object(obj)})").body[0]
label: Callable[[ILabel], stmt]       = lambda obj: parse(f"self.e{obj.id}_{obj.name} = ETKLabel(main=self._main, {__text_object(obj)}, {__visible_object(obj)})").body[0]
edit: Callable[[IEdit], stmt]         = lambda obj: parse(f"self.e{obj.id}_{obj.name} = ETKEdit(main=self._main, {__text_object(obj)}, {__visible_object(obj)})").body[0]

canvas: Callable[[ICanvas], stmt] = lambda obj: parse(f"self.e{obj.id}_{obj.name} = ETKCanvas(main=self._main, {__visible_object(obj)})").body[0]
timer: Callable[[ITimer, str], stmt] = lambda obj, intermediary_event_type: parse(f"self.e{obj.id}_{obj.name} = ETKTimer(main=self._main, interval_in_ms={obj.interval}, timer_function=self.{__event_func_name(obj, intermediary_event_type)})").body[0]


def generate_event_definition(obj: IBaseObject, intermediary_event_type: str) -> stmt:
    params = "self"
    if type(obj) != ITimer:
        params += ", params: ETKEventData"
    return parse(f"def {__event_func_name(obj, intermediary_event_type)}({params}):\n   pass").body[0]

generate_gui_init:Callable[[IWindow], stmt] = lambda window: parse(f"super().__init__(size={__arr_to_vec(window.size)}, caption='{window.title}', background_color={__col_arr_to_col(window.background_color)})").body[0]


def generate_event_bind(obj: IBaseObject, etk_event_type: str, intermediary_event_type: str) -> stmt:
    if type(obj) == IWindow:
        return parse(f"self.add_event({etk_event_type}, self.{__event_func_name(obj, intermediary_event_type)})").body[0]
    else:
        return parse(f"self.e{obj.id}_{obj.name}.add_event({etk_event_type}, self.{__event_func_name(obj, intermediary_event_type)})").body[0]

# endregion