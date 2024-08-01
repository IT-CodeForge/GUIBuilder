import os


class BaseGenerator:
    @staticmethod
    def _read_file(path: str) -> str:
        retval: str = ""
        with open(path, "r", encoding="utf-8") as f:
            retval = f.read()
        return retval

    @staticmethod
    def _join_paths(starting_path: str, following_path: str) -> str:
        return os.path.abspath(os.path.join(starting_path, following_path))

    @classmethod
    def _join_relative_path(cls, relative_path: str) -> str:
        from main import additional_files_path
        return cls._join_paths(additional_files_path, relative_path)
