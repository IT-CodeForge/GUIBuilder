from tkinter import Tk

class BTimer:
    def __init__(self, my_Tk:Tk, interval_in_ms:int, timer_function) -> None:
        self.__my_Tk = my_Tk
        self.__timer_func = timer_function
        self.__sleep_time = int(interval_in_ms)
        self.__is_running = True
        self.__my_Tk.after(self.__sleep_time, self.trigger)
    
    @property
    def interval(self)->int:
        return self.__sleep_time
    
    @interval.setter
    def interval(self, value:int):
        self.__sleep_time = int(value)
    
    def stop(self):
        self.__is_running = False
    
    def start(self):
        self.__is_running = True
        self.trigger()

    def trigger(self):
        self.__timer_func()
        if self.__is_running:
            self.__my_Tk.after(self.__sleep_time, self.trigger)
