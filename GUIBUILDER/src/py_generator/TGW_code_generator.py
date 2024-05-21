from typing import Callable
from intermediary_neu.objects.IBaseObjectWidgetVisible import IBaseObjectWidgetVisible
from intermediary_neu.objects.IBaseObjectWidgetText import IBaseObjectWidgetText
from intermediary_neu.objects.IBaseObject import IBaseObject
from intermediary_neu.objects.IButton import IButton
from intermediary_neu.objects.ICanvas import ICanvas
from intermediary_neu.objects.ICheckbox import ICheckbox
from intermediary_neu.objects.IEdit import IEdit
from intermediary_neu.objects.ILabel import ILabel
from intermediary_neu.objects.ITimer import ITimer
from intermediary_neu.objects.IWindow import IWindow

TYPE_TRANS: dict[type, str] = {
    IButton: "TGWButton",
    ICanvas: "TGWBitmapWindow",
    ICheckbox: "TGWCheckbox",
    IEdit: "TGWEdit",
    ILabel: "TGWEdit",
    ITimer: "TGWTimer"
}

__TGW_EVENT_FUNC_NAMES: dict[str, str | tuple[str, str]] = {
    "event_pressed":"eventButton(TGWButton* einButton, int event)",
    "event_double_pressed":"eventButton(TGWButton* einButton, int event)",
    "event_changed":("eventCheckBox(TGWCheckBox* eineCheckBox, int isChecked_1_0)", "eventEditChanged(TGWEdit* einEdit)"),
    "event_create":"eventShow()",
    "event_destroy":"", #not found in old generator
    "event_paint":"eventPaint(HDC hDeviceContext)",
    "event_resize":"eventResize()",
    "event_mouse_click":"eventMouseClick(int posX, int posY, TGWindow* affectedWindow)",
    "event_mouse_move":"eventMouseMove(int posX, int posY)"
}

__EVENT_FUNCS_HEAD_OWN_PARAMS: dict[str, str | tuple[str, str]] = {
    "event_pressed":"",
    "event_double_pressed":"",
    "event_changed":("int isChecked_1_0", ""),
    "event_create":"",
    "event_destroy":"", #not found in old generator
    "event_paint":"HDC hDeviceContext",
    "event_resize":"",
    "event_mouse_click":"int posX, int posY, TGWindow* affectedWindow",
    "event_mouse_move":"int posX, int posY"
}

# region utils

get_object_name: Callable[[IBaseObject], str] = lambda obj : f"e{obj.id}_{obj.name}"

get_event_func_own_name: Callable[[str, IBaseObject], str] = lambda event, obj : f"{get_object_name(obj)}_{event}"

__col_arr_to_col: Callable[[tuple[int, int, int]], int] = lambda arr: arr[0] << 16 | arr[1] << 8 | arr[2]

def string_times_n(string: str, n: int)-> str:
    retval = string
    for _ in range(n - 1):
        retval += string
    return retval

# endregion

# region generate attributes
__visible_object: Callable[[IBaseObjectWidgetVisible], str] = lambda obj : f"{obj.pos[0]}, {obj.pos[1]}, {obj.size[0]}, {obj.size[1]}"

__text_object: Callable[[IBaseObjectWidgetText], str] = lambda obj: f'"{obj.text}"'

button: Callable[[IButton], str] = lambda obj: f"{get_object_name(obj)} = new {TYPE_TRANS.get(IButton)}(this, {__visible_object(obj)}, {__text_object(obj)})"
checkbox: Callable[[ICheckbox], str] = lambda obj: f"{get_object_name(obj)} = new {TYPE_TRANS.get(ICheckbox)}(this, {__visible_object(obj)}, {__text_object(obj)}, false)"
label: Callable[[ILabel], str] = lambda obj: f"{get_object_name(obj)} = new {TYPE_TRANS.get(ILabel)}(this, {__visible_object(obj)}, {__text_object(obj)}, false, false)"
edit: Callable[[IEdit], str] = lambda obj: f"{get_object_name(obj)} = new {TYPE_TRANS.get(IEdit)}(this, {__visible_object(obj)}, {__text_object(obj)}, {str(obj.multiple_lines).lower()}, true)"

canvas: Callable[[ICanvas], str] = lambda obj: f"{get_object_name(obj)}_bitmap = new {TYPE_TRANS.get(ICanvas)}(this, {__visible_object(obj)})"
timer: Callable[[ITimer], str] = lambda obj: f"{get_object_name(obj)} = new {TYPE_TRANS.get(ITimer)}(this, {obj.interval}, &{get_object_name(obj)}_id)"

window_params: Callable[[IWindow], str] = lambda obj : f'10, 10, {obj.size[0]}, {obj.size[1]}, "{obj.name}", {__col_arr_to_col(obj.background_color)}'

# endregion

# region funcs heads

def generate_event_head_own(event: str, obj: IBaseObject) ->str:
    return f"{get_event_func_own_name(event, obj)}({__EVENT_FUNCS_HEAD_OWN_PARAMS.get(event)})"

def generate_event_head_tgw(event: str, obj: IBaseObject) ->str:
    if type(obj) == IEdit:
        return __TGW_EVENT_FUNC_NAMES.get('event_changed', ('',''))[0]
    if type(obj) == ICheckbox:
        return __TGW_EVENT_FUNC_NAMES.get('event_changed', ('',''))[1]
    
    return f"{__TGW_EVENT_FUNC_NAMES.get(event)}"

def generate_if_clause(condition: str, content: str, indent: str, starting_indent_level: int) -> str:
    retval: str = ""
    retval += f"{string_times_n(indent, starting_indent_level)}if({condition})\r\n"
    retval += string_times_n(indent, starting_indent_level) + "{\n\r"
    for line in content.splitlines():
        retval += string_times_n(indent, starting_indent_level + 1) + line
    retval += string_times_n(indent, starting_indent_level) + "}\n\r"
    return retval

# endregion