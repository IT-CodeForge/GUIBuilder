from typing import Callable

class ETKNoTKEventBase:
    def __init__(self) -> None:
        self._event_lib:dict[str,list] = {}

    def add_event(self, event_type, eventhandler:Callable[...,None], truth_func:Callable[..., None]|None=None):
        if event_type not in self._event_lib:
            self._event_lib[event_type] = []
        if truth_func == None:
            truth_func = lambda event, object_id:True
        self._event_lib[event_type].append([eventhandler, truth_func])

    def remove_event(self, event_type, eventhandler:Callable[..., None]):
        if event_type in self._event_lib.keys():
            for event in self._event_lib[event_type]:
                if event[0] == eventhandler:
                    self._event_lib[event_type].remove(event)
        
    def _eventhandler(self, event_type):
        if event_type not in self._event_lib.keys():
            return
        for eventhandler in self._event_lib[event_type]:
            if not eventhandler[1](None, self):
                continue
            try:
                params = {
                    "object_id":self,
                    "event_type":event_type
                }
                eventhandler[0](params)
            except:
                pass
            try:
                eventhandler[0]()
            except:
                pass