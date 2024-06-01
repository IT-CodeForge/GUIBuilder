from threading import Thread
import time
import traceback
from typing import Any, Callable


class ETKScheduler:
    def __init__(self) -> None:
        self.__exit = False
        self.__scheduled_events: list[tuple[Callable[..., Any], tuple[Any, ...]]] = []
        self.__scheduled_event_actions: list[tuple[Callable[..., Any], tuple[Any, ...], dict[str, Any]]] = []
        self.__thread = Thread(target=self.__handler)
        self.__thread.start()

    def schedule_event_action(self, callback: Callable[..., Any], *args: Any, **kwargs: Any):
        self.__scheduled_event_actions.append((callback, args, kwargs))

    def schedule_event(self, ev_callback: Callable[..., Any], event_data: tuple[Any, ...]):
        self.__scheduled_events.append((ev_callback, event_data))

    def exit(self) -> None:
        self.__exit = True
        self.__thread.join()
    

    def __exec_event_callback(self, callback_function: Callable[..., Any], event_data: tuple[Any, ...]) -> None:
        err_1 = ""
        try:
            callback_function(event_data)
            return
        except TypeError as ex:
            err_1 = traceback.format_exc()
            if str(ex).find("positional argument") == -1:
                raise ex
        try:
            callback_function()
        except TypeError as ex:
            if str(ex).find("positional argument") == -1:
                raise ex
            ret_val = callback_function.__code__.co_varnames
            name = callback_function.__name__  # type:ignore
            print(err_1)
            print(traceback.format_exc())
            raise TypeError(
                f"invalid parametercount for event function ({name}) (can only be 0, 1 (self, cls, etc not included)), parameter: {ret_val}")

    def __handler(self):
        while not self.__exit:
            begin_ns = time.time_ns()

            if len(self.__scheduled_event_actions) != 0:
                raise ValueError

            for c1, data in self.__scheduled_events[:]:
                self.__scheduled_events.pop(0)
                self.__exec_event_callback(c1, data)
                for c2, a2, kwa2 in self.__scheduled_event_actions[:]:
                    self.__scheduled_event_actions.pop(0)
                    c2(*a2, **kwa2)

            sleep_duration = 0.1
            duration = (time.time_ns() - begin_ns) / 10**9
            duration = sleep_duration if duration > sleep_duration else duration
            time.sleep(sleep_duration - duration)
