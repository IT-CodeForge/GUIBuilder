from multiprocessing import freeze_support
from os import devnull, path
import sys
from threading import Thread
import time
from steuerung import Steuerung

version = "0.1"
dir_root: str  # path to root dir (project folder / folder of exe)
internal_dir_root: str  # path to internal root dir (project folder / folder of unpacked files)
additional_files_path: str


class MSGBoxStream():
    def __init__(self):
        self.t = Thread()
        self.msg = ""

    def __send(self):
        time.sleep(0.25)
        from jk import msgbox
        msgbox.create_msg_box(
            f"GUI-Builder - FEHLER", self.msg, msgbox.BUTTON_STYLES.OK)
        self.msg = ""

    def write(self, text: str) -> int:
        self.msg += text
        if not self.t.is_alive():
            self.t = Thread(target=self.__send)
            self.t.start()
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        return len(text)

    def flush(self) -> None:
        return


if __name__ == "__main__":
    import main
    freeze_support()  # must be called to ensure that multiprocessing works correctly if packaged to exe (ignored when run as script)
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(2)

    # fixes problem when application is ran without console (because then sys.stdout and sys.stderr are nonexisting and any print() etc. raises an Error)
    if sys.stdout is None:  # type:ignore
        sys.stdout = open(devnull, "w")  # redirects output to void
    if sys.stderr is None:  # type:ignore
        sys.stderr = MSGBoxStream()  # redirects errors to MSGBox

    # Überprüft ob es als exe oder als py-script vorliegt
    if not getattr(sys, "frozen", False):
        main.dir_root = path.abspath(path.join(path.split(path.abspath(__file__))[0], ".."))
        main.internal_dir_root = main.dir_root
    else:
        main.dir_root = path.split(path.abspath(sys.executable))[0]
        main.internal_dir_root = str(sys._MEIPASS)  # type:ignore
    main.additional_files_path = path.abspath(f"{main.internal_dir_root}\\additional_files")

    print("\n"*20)
    s = Steuerung()
    s.run()
