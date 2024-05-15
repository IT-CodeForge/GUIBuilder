from multiprocessing import freeze_support
from os import devnull, path
import sys
from threading import Thread
import time
from steuerung import Steuerung

version = "0.1"
dir_root: str
internal_dir_root: str
additional_files_path: str

# from io import TextIOWrapper
# from os import fsync, path

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
            ctypes.windll.shcore.SetProcessDpiAwareness(0) # NOTE
        return len(text)

    def flush(self) -> None:
        return

if __name__ == "__main__":
    import main
    freeze_support()

    # Überprüft ob es als exe oder als py-script vorliegt
    if path.split(sys.executable)[1] in ["python.exe", "pythonw.exe"]:
        main.dir_root = path.abspath(path.join(path.split(path.abspath(__file__))[0], ".."))
        main.internal_dir_root = main.dir_root
    else:
        # Release: Disables print(), etc
        sys.stdout = open(devnull, 'w')
        sys.stderr = MSGBoxStream()
        # sys.stdout = FileAutoSave(r"C:\jk\out.log")
        # sys.stderr = FileAutoSave(r"C:\jk\err.log")
        main.dir_root = path.split(path.abspath(sys.executable))[0]
        main.internal_dir_root = path.split(path.abspath(__file__))[0]
    main.additional_files_path = path.abspath(f"{main.internal_dir_root}\\additional_files")

    print("\n"*20)
    s = Steuerung()
    s.run()
