from .BaseGenerator import BaseGenerator
from intermediary_neu.objects.IBaseObject import IBaseObject
from intermediary_neu.objects.ICheckbox import ICheckbox
from intermediary_neu.objects.ITimer import ITimer
from intermediary_neu.objects.IEdit import IEdit

class BaseTGWGenerator(BaseGenerator):
    _INDENT = "  "
    __EVENT_TRANS: dict[str, str] = {
        "event_pressed":"eventButton",
        "event_double_pressed":"eventButton",
        #"event_changed":("eventCheckBox", "eventEditChanged"), only here in spirit
        "event_create":"eventShow",
        "event_destroy":"", #not found in old generator
        "event_paint":"eventPaint",
        "event_resize":"eventResize",
        "event_mouse_click":"eventMouseClick",
        "event_mouse_move":"eventMouseMove"
    }
    def __init__(self) -> None:
        super().__init__()
    
    @classmethod
    def _generate_event_dict(cls, tgw_objects: tuple[IBaseObject, ...])-> dict[str, list[tuple[IBaseObject, str]]]:
        retval: dict[str, list[tuple[IBaseObject, str]]] = {}
        for tgw_object in tgw_objects:
            if type(tgw_object) == ITimer:
                retval["timer_funcs"] = retval.get("timer_funcs", []) + [(tgw_object, "event_timer")]
                continue
            for attribute in tgw_object.ATTRIBUTES:
                if attribute.startswith("event_"):
                    if not getattr(tgw_object, attribute):
                        continue
                    if type(tgw_object) == ICheckbox:
                        retval["eventCheckBox"] = retval.get("eventCheckBox", []) + [(tgw_object, attribute)]
                        continue
                    if type(tgw_object) == IEdit:
                        retval["eventEditChanged"] = retval.get("eventEditChanged", []) + [(tgw_object, attribute)]
                        continue
                    retval[cls.__EVENT_TRANS.get(attribute, "")] = retval.get(cls.__EVENT_TRANS.get(attribute, ""), []) + [(tgw_object, attribute)]
        return retval