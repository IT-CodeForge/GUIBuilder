from threading import Thread
import time
from typing import Any, Callable
from .SubclassableEnum import SubclassableEnum


class ETKScheduledActions(SubclassableEnum):
    pass


class ETKScheduler:
    def __init__(self) -> None:
        self.__exit = False
        self.__scheduled_events: list[tuple[Callable[..., Any], tuple[Any, ...], dict[str, Any]]] = []
        self.__scheduled_event_actions: list[tuple[Callable[..., Any], tuple[Any, ...], dict[str, Any]]] = []
        self.__thread = Thread(target=self.__handler)
        self.__thread.start()

    def schedule_event_action(self, callback: Callable[..., Any], *args: Any, **kwargs: Any):
        self.__scheduled_event_actions.append((callback, args, kwargs))

    def schedule_event(self, ev_callback: Callable[..., Any], *args: Any, **kwargs: Any):
        self.__scheduled_events.append((ev_callback, args, kwargs))

    def exit(self) -> None:
        self.__exit = True
        self.__thread.join()

    def __handler(self):
        while not self.__exit:
            begin_ns = time.time_ns()

            if len(self.__scheduled_event_actions) != 0:
                raise ValueError

            for c1, a1, kwa1 in self.__scheduled_events[:]:
                self.__scheduled_events.pop(0)
                c1(*a1, **kwa1)
                for c2, a2, kwa2 in self.__scheduled_event_actions[:]:
                    self.__scheduled_event_actions.pop(0)
                    c2(*a2, **kwa2)

            sleep_duration = 0.1
            duration = (time.time_ns() - begin_ns) / 10**9
            duration = sleep_duration if duration > sleep_duration else duration
            time.sleep(sleep_duration - duration)
