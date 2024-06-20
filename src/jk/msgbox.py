# V1.4
from __future__ import annotations
from enum import Enum
from typing import Final, Literal, overload
from ctypes import windll
from threading import Thread
import time


class RETURN_VALUES(Enum):
    OK: Final = 1
    CANCEL: Final = 2
    ABORT: Final = 3
    RETRY: Final = 4
    IGNORE: Final = 5
    YES: Final = 6
    NO: Final = 7
    TRY_AGAIN: Final = 10
    CONTINUE: Final = 11


class BUTTON_STYLES(Enum):
    OK: Final = 0
    OK_CANCEL: Final = 1
    ABORT_RETRY_IGNORE: Final = 2
    YES_NO_CANCEL: Final = 3
    YES_NO: Final = 4
    RETRY_CANCEL: Final = 5
    CANCEL_TRY_AGAIN_CONTINUE: Final = 6


class ICON_STYLES(Enum):
    NONE: Final = 0
    ERROR: Final = 0x10
    QUESTION: Final = 0x20
    WARNING: Final = 0x30
    INFORMATION: Final = 0x40


__DEFAULT_BUTTON_VALUES: Final = (None, 0, 0x100, 0x200, 0x300)
__TOPMOST: Final = 0x40000
__SETFOREGROUND: Final = 0x10000


@overload
def create_msg_box(title: str, text: str, button_style: Literal[BUTTON_STYLES.OK] = BUTTON_STYLES.OK, icon_style: ICON_STYLES = ICON_STYLES.NONE, default_button: Literal[1] = 1, topmost: bool = True) -> RETURN_VALUES:
    pass

@overload
def create_msg_box(title: str, text: str, button_style: Literal[BUTTON_STYLES.OK_CANCEL, BUTTON_STYLES.YES_NO, BUTTON_STYLES.RETRY_CANCEL], icon_style: ICON_STYLES = ICON_STYLES.NONE, default_button: Literal[1, 2] = 1, topmost: bool = True) -> RETURN_VALUES:
    pass

@overload
def create_msg_box(title: str, text: str, button_style: Literal[BUTTON_STYLES.ABORT_RETRY_IGNORE, BUTTON_STYLES.YES_NO_CANCEL, BUTTON_STYLES.CANCEL_TRY_AGAIN_CONTINUE], icon_style: ICON_STYLES = ICON_STYLES.NONE, default_button: Literal[1, 2, 3] = 1, topmost: bool = True) -> RETURN_VALUES:
    pass


def create_msg_box(title: str, text: str, button_style: BUTTON_STYLES = BUTTON_STYLES.OK, icon_style: ICON_STYLES = ICON_STYLES.NONE, default_button: Literal[1, 2, 3] = 1, topmost: bool = True) -> RETURN_VALUES:
    if type(t_default_button_value := __DEFAULT_BUTTON_VALUES[default_button]) != int:
        raise IndexError("default_button out of range")

    t_topmost = 0
    if topmost:
        t_topmost = __TOPMOST

    return RETURN_VALUES(windll.user32.MessageBoxW(None, text, title, __SETFOREGROUND | t_topmost | button_style.value | icon_style.value | t_default_button_value))

class MSGBoxStream():
    def __init__(self):
        self.t = Thread()
        self.msg = ""

    def __send(self):
        time.sleep(0.25)
        from jk import msgbox
        msgbox.create_msg_box(
            f"GUI-Builder - ERROR", self.msg, msgbox.BUTTON_STYLES.OK)
        self.msg = ""

    def write(self, text: str) -> int:
        self.msg += text
        if not self.t.is_alive():
            self.t = Thread(target=self.__send)
            self.t.start()
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(0)
        return len(text)

    def flush(self) -> None:
        return