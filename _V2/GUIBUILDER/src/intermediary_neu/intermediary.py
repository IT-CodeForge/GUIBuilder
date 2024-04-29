from typing import Any, Type
from .objects.IBaseObject import IBaseObject

#TODO: save, load

class Intermediary:
    def __init__(self) -> None:
        self.__next_id = 0
        self.__objects: dict[int, IBaseObject] = {}

    @property
    def objects(self) -> tuple[IBaseObject, ...]:
        """READ-ONLY"""
        return tuple(self.__objects.values())

    def create_object(self, type: Type[IBaseObject], *args: tuple[Any], **kwargs: dict[str, Any]) -> Any:
        object = type(self.__next_id, *args, **kwargs)
        self.__next_id += 1
        self.__objects.update({object.id: object})
        return object

    def delete_object(self, *, object: IBaseObject) -> None:
            self.__objects.pop(object.id)
