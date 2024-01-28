from enum import Enum
from typing import Any
from ctypes import windll
import multiprocessing
import threading

class MSGBox:
    __threads: list[Any] = []

    class RETURN_VALUES(Enum):
        OK = 1
        CANCEL = 2
        ABORT = 3
        RETRY = 4
        IGNORE = 5
        YES = 6
        NO = 7
        TRY_AGAIN = 10
        CONTINUE = 11
    
    class STYLES(Enum):
        OK = 0
        OK_CANCEL = 1
        ABORT_RETRY_IGNORE = 2
        YES_NO_CANCEL = 3
        YES_NO = 4
        RETRY_CANCEL = 5
        CANCEL_TRY_AGAIN_CONTINUE = 6
    
    def __init__(self):
        raise SyntaxError("static class")

    @staticmethod
    def create_msg_box(p_title: str, p_text: str, p_style: STYLES) -> RETURN_VALUES:
        return windll.user32.MessageBoxW(None, p_text, p_title, 0x00040000 | p_style.value)
    
    @classmethod
    def __create_async_msg_box(cls, p_title: str, p_text: str, p_style: STYLES):
        cls.__threads.append(threading.current_thread())
        p = multiprocessing.Process(target=cls.create_msg_box, args=(p_title, p_text, p_style))
        p.start()
        p.join()
        cls.__threads.remove(threading.current_thread())
    
    @classmethod
    def create_async_msg_box(cls, p_title: str, p_text: str, p_style: STYLES):
        t = threading.Thread(target=cls.__create_async_msg_box, args=(p_title, p_text, p_style))
        t.start()

    @classmethod
    def join_threads(cls):
        for t in cls.__threads:
            t.join()