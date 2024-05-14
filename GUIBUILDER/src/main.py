from os import devnull, path
import sys
from steuerung import Steuerung

version = "0.1"
dir_root: str
internal_dir_root: str
additional_files_path: str

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

    # Überprüft ob es als exe oder als py-script vorliegt
    if path.split(sys.executable)[1] in ["python.exe", "pythonw.exe"]:
        main.dir_root = path.abspath(path.join(path.split(path.abspath(__file__))[0], ".."))
        main.internal_dir_root = main.dir_root
    else:
        # Release: Disables print(), etc
        sys.stdout = sys.stderr = open(devnull, 'w')
        # sys.stdout = FileAutoSave(r"C:\jk\out.log")
        # sys.stderr = FileAutoSave(r"C:\jk\err.log")
        main.dir_root = path.split(path.abspath(sys.executable))[0]
        main.internal_dir_root = path.split(path.abspath(__file__))[0]
    main.additional_files_path = path.abspath(f"{main.internal_dir_root}\\additional_files")

    print("\n"*20)
    s = Steuerung()
    s.run()
