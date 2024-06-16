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

    def save_to_file(self, path: str) -> None:
        objects = {str(type(o).__name__): o.get_attributes_as_dict() for o in self.__objects.values()}
        data = {"next_id": self.__next_id, "objects": objects}
        with open(path, "w") as f:
            f.write(json.dumps(data, indent=4))

    def load_from_file(self, path: str) -> None:
        with open(path, "r") as f:
            data = json.load(f)
        try:
            self.__next_id = data["next_id"]
        except KeyError:
            raise LoadingError(f"Die Datei {path} ist unvollständig.\n Der Schlüssel 'next_id' fehlt.", f"The file {path} is invalid.\nIt does not contain the 'next_id' key.")
        if "objects" not in data.keys():
            raise LoadingError(f"Die Datei {path} ist unvollständig.\n Der Schlüssel 'objects' fehlt.", f"The file {path} is invalid.\nIt does not contain the 'objects' key.")
        for c, d in data["objects"].items():
            import intermediary
            type = getattr(intermediary, c)
            for a in type.ATTRIBUTES:
                if a not in d.keys():
                    raise LoadingError(f"Das Objekt {c} in der Datei {path} ist unvollständig.\n Der Schlüssel '{a}' fehlt.", f"The object {c} in the file {path} is invalid.\nIt does not contain the '{a}' key.")
            object: IObjects = type(d["id"])
            object.load_attributes_from_dict(d)
            self.__objects.update({object.id: object})
