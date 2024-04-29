from typing import Any, Optional, Type, overload
from .objects.IBaseObject import IBaseObject

#TODO: save, load

class Intermadiary:
    def __init__(self) -> None:
        self.__next_id = 0
        self.__objects: dict[int, IBaseObject]

    @property
    def objects(self) -> tuple[IBaseObject, ...]:
        """READ-ONLY"""
        return tuple(self.__objects.values())

    def create_object(self, type: Type[IBaseObject], *args: tuple[Any], **kwargs: dict[str, Any]) -> int:
        object = type(self.__next_id, *args, **kwargs)
        self.__next_id += 1
        self.__objects.update({object.id: object})
        return object.id

    @overload
    def delete_object(self, *, object: IBaseObject) -> None:
        pass

    @overload
    def delete_object(self, *, id: int) -> None:
        pass

    def delete_object(self, *, object: Optional[IBaseObject] = None, id: Optional[int] = None) -> None:
        if object == None and id == None or object != None and id != None:
            raise TypeError("you must give object or id")
        if object != None:
            id = object.id
        if id != None:
            self.__objects.pop(id)
