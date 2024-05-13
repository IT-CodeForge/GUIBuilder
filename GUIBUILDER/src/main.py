from os import devnull, environ
import sys
from steuerung import Steuerung

version = "0.1"

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
    if environ.get("DEV") == None:
        # Release: Disables print(), etc
        sys.stdout = sys.stderr = open(devnull, 'w')
        # sys.stdout = FileAutoSave(r"C:\jk\out.log")
        # sys.stderr = FileAutoSave(r"C:\jk\err.log")

    print("\n"*20)
    s = Steuerung()
    s.run()
