import json
from typing import Any, Type, TypeVar, Union

from .objects.ICanvas import ICanvas
from .objects.ICheckbox import ICheckbox
from .objects.IEdit import IEdit
from .objects.ILabel import ILabel
from .objects.ITimer import ITimer
from .objects.IButton import IButton
from .objects.IWindow import IWindow
from .objects.IBaseObject import IBaseObject
from .exceptions import LoadingError

IObjectWidgets = Union[IButton, ICanvas, ICheckbox, IEdit, ILabel, ITimer]
IObjects = Union[IWindow, IObjectWidgets]


class Intermediary:
    def __init__(self) -> None:
        self.__next_id: int = 0
        self.__objects: dict[int, IObjects] = {}

    @property
    def objects(self) -> tuple[IObjects, ...]:
        """READ-ONLY"""
        return tuple(self.__objects.values())

    __T = TypeVar("__T", bound=IObjects)

    def create_object(self, type: Type[__T], **kwargs: Any) -> __T:
        object = type(id=self.__next_id, **kwargs)
        self.__next_id += 1
        self.__objects.update({object.id: object})
        return object

    def delete_object(self, object: IBaseObject) -> None:
        self.__objects.pop(object.id)

    def save_to_file(self, path: str, language: str) -> None:
        objects = [{"type": str(type(o).__name__)} | o.get_attributes_as_dict() for o in self.__objects.values()]
        data: dict[str, Any] = {"next_id": self.__next_id, "language": language, "objects": objects}
        with open(path, "w", encoding="utf-8") as f:
            f.write(json.dumps(data, indent=4))

    def load_from_file(self, path: str) -> str:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        try:
            self.__next_id = data["next_id"]
        except KeyError:
            raise LoadingError(f"Die Datei {path} ist unvollständig.\n Der Schlüssel 'next_id' fehlt.", f"The file {path} is invalid.\nIt does not contain the 'next_id' key.")

        try:
            lang = data["language"]
        except KeyError:
            raise LoadingError(f"Die Datei {path} ist unvollständig.\n Der Schlüssel 'language' fehlt.", f"The file {path} is invalid.\nIt does not contain the 'language' key.")

        if "objects" not in data.keys():
            raise LoadingError(f"Die Datei {path} ist unvollständig.\n Der Schlüssel 'objects' fehlt.", f"The file {path} is invalid.\nIt does not contain the 'objects' key.")
        o: dict[str, Any]
        for o in data["objects"]:
            import intermediary
            type: Type[IObjects] = getattr(intermediary, o["type"])
            for a in type.ATTRIBUTES:
                if a not in o.keys():
                    raise LoadingError(f"Das Objekt {o["type"]} mit der id {o.get("id")} in der Datei {path} ist unvollständig.\n Der Schlüssel '{a}' fehlt.", f"The object {o["type"]} with the id {o.get("id")} in the file {path} is invalid.\nIt does not contain the '{a}' key.")
            object: IObjects = type(o["id"])
            object.load_attributes_from_dict(o)
            self.__objects.update({object.id: object})

        return lang
