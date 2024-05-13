import os

class BaseGenerator:
    @staticmethod
    def _read_file(path: str) -> str:
        retval: str = ""
        with open(path, "r") as f:
            retval = f.read()
        return retval
    
    @staticmethod
    def _join_paths(starting_path: str, following_path: str) -> str:
        return os.path.abspath(os.path.join(starting_path, following_path))

    @classmethod
    def _join_relative_path(cls, relative_path: str) -> str:
        return cls._join_paths(os.path.split(__file__)[0], relative_path)