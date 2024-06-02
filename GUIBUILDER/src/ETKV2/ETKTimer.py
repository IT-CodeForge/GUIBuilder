from tkinter import Tk
from typing import Any, Callable

from .ETKMainWindow import ETKMain


class ETKTimer:
    def __init__(self, main: ETKMain, interval_in_ms: int, timer_function: Callable[[], None], running: bool = True, **kwargs: Any) -> None:
        self.__my_Tk: Tk = main.root_tk_object
        self.__scheduler = main.scheduler
        self.__timer_function: Callable[[], None] = timer_function
        self.interval_in_ms: int = interval_in_ms
        self.__is_running = running
        if running:
            self.__my_Tk.after(self.interval_in_ms, self.__trigger)

    # region Properties

    @property
    def running(self) -> bool:
        return self.__is_running

    @running.setter
    def running(self, value: bool) -> None:
        self.__is_running = value
        if value:
            self.__trigger()

    # endregion
    # region Methods

    def __trigger(self) -> None:
        if self.__is_running:
            self.__scheduler.schedule_event(self.__timer_function, tuple())
            self.__my_Tk.after(self.interval_in_ms, self.__trigger)

    # endregion
