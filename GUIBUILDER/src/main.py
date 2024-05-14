from os import devnull, environ, path
import sys
from steuerung import Steuerung

version = "0.1"
dir_root: str
additional_files_path: str
dev_mode: bool

# from io import TextIOWrapper
# from os import fsync, path

# class FileAutoSave(TextIOWrapper):
#     @property
#     def path(self) -> str:
#         return path.abspath(self._path)

#     def __init__(self, path: str):
#         super().__init__(open(path, "a").detach())
#         self._path: str = path

#     def __del__(self):
#         self.close()

#     def write(self, text: str) -> int:
#         t_return = super().write(text)
#         self.flush()
#         fsync(self.fileno())
#         return t_return

if __name__ == "__main__":
    import main
    if environ.get("DEV") != None:
        main.dir_root = path.split(path.abspath(__file__))[0]
        main.additional_files_path = path.abspath(f"{main.dir_root}\\..\\additional_files")
        main.dev_mode = True
    else:
        # Release: Disables print(), etc
        sys.stdout = sys.stderr = open(devnull, 'w')
        # sys.stdout = FileAutoSave(r"C:\jk\out.log")
        # sys.stderr = FileAutoSave(r"C:\jk\err.log")
        main.dir_root = path.split(path.abspath(sys.executable))[0]
        main.additional_files_path = path.abspath(f"{main.dir_root}\\additional_files")
        main.dev_mode = False

    print("\n"*20)
    s = Steuerung()
    s.run()
