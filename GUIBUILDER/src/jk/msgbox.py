# V1.4
from __future__ import annotations
from enum import Enum
from typing import Any, Callable, Final, Literal, overload
from ctypes import windll
from multiprocessing import Process, Queue
from threading import Thread, current_thread

__threads: list[Thread] = []


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


def __create_async_msg_box_inner(queue: Queue[RETURN_VALUES], title: str, text: str, button_style: BUTTON_STYLES, icon_style: ICON_STYLES, default_button: Literal[1, 2, 3], topmost: bool) -> None:
    queue.put(create_msg_box(title, text, button_style, icon_style, default_button, topmost)) #type:ignore


def __create_async_msg_box(title: str, text: str, button_style: BUTTON_STYLES, icon_style: ICON_STYLES, default_button: Literal[1, 2, 3], topmost: bool, callback: Callable[[RETURN_VALUES], Any]) -> None:
    __threads.append(current_thread())
    t_queue: Queue[RETURN_VALUES] = Queue()
    t_p = Process(
        target=__create_async_msg_box_inner, args=(t_queue, title, text, button_style, icon_style, default_button, topmost))
    t_p.start()
    t_p.join()
    callback(t_queue.get(False))
    __threads.remove(current_thread())


@overload
def create_async_msg_box(title: str, text: str, button_style: Literal[BUTTON_STYLES.OK] = BUTTON_STYLES.OK, icon_style: ICON_STYLES = ICON_STYLES.NONE, default_button: Literal[1] = 1, topmost: bool = True, callback: Callable[[RETURN_VALUES], Any] = lambda x: None) -> None:
    pass


@overload
def create_async_msg_box(title: str, text: str, button_style: Literal[BUTTON_STYLES.OK_CANCEL, BUTTON_STYLES.YES_NO, BUTTON_STYLES.RETRY_CANCEL], icon_style: ICON_STYLES = ICON_STYLES.NONE, default_button: Literal[1, 2] = 1, topmost: bool = True, callback: Callable[[RETURN_VALUES], Any] = lambda x: None) -> None:
    pass


@overload
def create_async_msg_box(title: str, text: str, button_style: Literal[BUTTON_STYLES.ABORT_RETRY_IGNORE, BUTTON_STYLES.YES_NO_CANCEL, BUTTON_STYLES.CANCEL_TRY_AGAIN_CONTINUE], icon_style: ICON_STYLES = ICON_STYLES.NONE, default_button: Literal[1, 2, 3] = 1, topmost: bool = True, callback: Callable[[RETURN_VALUES], Any] = lambda x: None) -> None:
    pass


def create_async_msg_box(title: str, text: str, button_style: BUTTON_STYLES = BUTTON_STYLES.OK, icon_style: ICON_STYLES = ICON_STYLES.NONE, default_button: Literal[1, 2, 3] = 1, topmost: bool = True, callback: Callable[[RETURN_VALUES], Any] = lambda x: None) -> None:
    t_t = Thread(target=__create_async_msg_box, args=(title, text, button_style, icon_style, default_button, topmost, callback))
    t_t.start()


@overload
def create_detached_msg_box(title: str, text: str, button_style: Literal[BUTTON_STYLES.OK] = BUTTON_STYLES.OK, icon_style: ICON_STYLES = ICON_STYLES.NONE, default_button: Literal[1] = 1, topmost: bool = True) -> None:
    pass

@overload
def create_detached_msg_box(title: str, text: str, button_style: Literal[BUTTON_STYLES.OK_CANCEL, BUTTON_STYLES.YES_NO, BUTTON_STYLES.RETRY_CANCEL], icon_style: ICON_STYLES = ICON_STYLES.NONE, default_button: Literal[1, 2] = 1, topmost: bool = True) -> None:
    pass

@overload
def create_detached_msg_box(title: str, text: str, button_style: Literal[BUTTON_STYLES.ABORT_RETRY_IGNORE, BUTTON_STYLES.YES_NO_CANCEL, BUTTON_STYLES.CANCEL_TRY_AGAIN_CONTINUE], icon_style: ICON_STYLES = ICON_STYLES.NONE, default_button: Literal[1, 2, 3] = 1, topmost: bool = True) -> None:
    pass


def create_detached_msg_box(title: str, text: str, button_style: BUTTON_STYLES = BUTTON_STYLES.OK, icon_style: ICON_STYLES = ICON_STYLES.NONE, default_button: Literal[1, 2, 3] = 1, topmost: bool = True) -> None:
    if type(t_default_button_value := __DEFAULT_BUTTON_VALUES[default_button]) != int:
        raise IndexError("default_button out of range")
    
    t_topmost = 0
    if topmost:
        t_topmost = __TOPMOST
    
    options = __SETFOREGROUND | t_topmost | button_style.value | icon_style.value | t_default_button_value

    from .exec import exec_programm, convert_to_cmd # type:ignore
    text = text.replace('"', "")
    text = text.replace("\r", "")
    text = text.replace("\n", '""  + vbCrLf + ""')
    exec_programm(convert_to_cmd(f'mshta vbscript:Execute("msgbox (""{text}""),{options},""{title}"":close")'), False)


def join_threads():
    for t in __threads:
        t.join()


if __name__ == "__main__":
    for bs in BUTTON_STYLES:
        print(create_msg_box("TEST", f"button_style={bs}", bs)) #type:ignore
    
    for ics in tuple(ICON_STYLES):
        create_msg_box("TEST" , f"icon_style={ics}", BUTTON_STYLES.OK, ics)
    
    for dbp in (1, 2, 3):
        create_msg_box("TEST", f"default_button={dbp}", BUTTON_STYLES.CANCEL_TRY_AGAIN_CONTINUE, ICON_STYLES.NONE, dbp)
    
    create_msg_box("TEST", "topmost=False", topmost = False)

    def callback(v: RETURN_VALUES):
        print(v)

    create_async_msg_box("TEST", "async_msg_box_1", BUTTON_STYLES.OK, callback=callback)
    create_async_msg_box("TEST", "async_msg_box_2", BUTTON_STYLES.CANCEL_TRY_AGAIN_CONTINUE, callback=callback)
    join_threads()   