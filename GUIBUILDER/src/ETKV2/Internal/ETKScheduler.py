import sys
from threading import Thread, current_thread
import threading
import time
from tkinter import Tk
from typing import Any, Callable

from .ETKUtils import exec_event_callback


class ETKScheduler:
    def __init__(self, tk: Tk, disabled: bool) -> None:
        self.__exit = False
        self.__disabled = disabled
        self._blocked = False
        self.__tk = tk
        self.__scheduled_events: list[tuple[Callable[..., Any], tuple[Any, ...]]] = []
        self.__scheduled_event_actions: dict[Callable[..., Any], tuple[tuple[Any, ...], dict[str, Any]]] = {}
        self.__thread = Thread(target=self.__handler)
        if not self.__disabled:
            self.__thread.start()

    def schedule_event_action(self, callback: Callable[..., Any], *args: Any, **kwargs: Any):
        if (current_thread() != self.__thread and not self._blocked) or self.__disabled:
            callback(*args, **kwargs)
            return
        self.__scheduled_event_actions.update({callback: (args, kwargs)})

    def schedule_event(self, ev_callback: Callable[..., Any], event_data: tuple[Any, ...]):
        if self.__disabled:
            exec_event_callback(ev_callback, event_data)
            return
        self.__scheduled_events.append((ev_callback, event_data))

    def exit(self) -> None:
        self.__exit = True
        if not self.__thread.is_alive():
            sys.exit()

    def handle_event_actions(self):
        while len(self.__scheduled_event_actions.keys()) != 0 and not self.__exit:
            c2 = tuple(self.__scheduled_event_actions.keys())[0]
            a2, kwa2 = self.__scheduled_event_actions[c2]
            del self.__scheduled_event_actions[c2]
            c2(*a2, **kwa2)

    def __handler(self):
        while not self.__exit and threading.main_thread().is_alive():
            begin_ns = time.time_ns()

            if len(self.__scheduled_event_actions.keys()) != 0:
                raise RuntimeError

            while len(self.__scheduled_events) > 0 and not self.__exit:
                c1, data = self.__scheduled_events[0]
                self.__scheduled_events.pop(0)
                exec_event_callback(c1, data)
            self.handle_event_actions()

            sleep_duration = 0.1
            duration = (time.time_ns() - begin_ns) / 10**9
            duration = sleep_duration if duration > sleep_duration else duration
            time.sleep(sleep_duration - duration)
        if threading.main_thread().is_alive():
            self.__tk.after(0, sys.exit)
            sys.exit()
