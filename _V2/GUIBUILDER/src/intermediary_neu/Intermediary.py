import json
from typing import Any, Type
from .objects.IBaseObject import IBaseObject

# TODO: save, load


class Intermediary:
    def __init__(self) -> None:
        self.__next_id = 0
        self.__objects: dict[int, IBaseObject] = {}

    @property
    def objects(self) -> tuple[IBaseObject, ...]:
        """READ-ONLY"""
        return tuple(self.__objects.values())

    def create_object(self, type: Type[IBaseObject], *args: Any, **kwargs: Any) -> Any:
        object = type(self.__next_id, *args, **kwargs)
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
        self.__next_id = data["next_id"]
        for c, d in data["objects"].items():
            import intermediary_all
            type = getattr(intermediary_all, c)
            object: IBaseObject = type(d["id"])
            object.load_attributes_from_dict(d)
            self.__objects.update({object.id: object})
