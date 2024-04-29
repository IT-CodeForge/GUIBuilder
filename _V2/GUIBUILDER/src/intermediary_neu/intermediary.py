from typing import Optional, overload
from .objects.BaseObject import BaseObject


class Intermadiary:
    def __init__(self) -> None:
        self.__id = 0
        self.__objects: dict[int, BaseObject]

    @property
    def objects(self) -> tuple[BaseObject, ...]:
        """READ-ONLY"""
        return tuple(self.__objects.values())
    
    def add_object(self, object: BaseObject) -> int:
        if object in self.__objects.values() or object.id in self.__objects.keys():
            raise ValueError(f"object {object} already added")
        self.__objects.update({object.id: object})
        return object.id
    
    @overload
    def delete_object(self, *, object: BaseObject) -> None:
        pass

    @overload
    def delete_object(self, *, id: int) -> None:
        pass
    
    def delete_object(self, *, object: Optional[BaseObject] = None, id: Optional[int] = None) -> None:
        if object == None and id == None or object != None and id != None:
            raise TypeError("you must give object or id")
        if object != None:
            id = object.id
        if id != None:
            self.__objects.pop(id)