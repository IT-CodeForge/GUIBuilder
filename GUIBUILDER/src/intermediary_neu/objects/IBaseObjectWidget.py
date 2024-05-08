from typing import Any
from .IBaseObject import IBaseObject


class IBaseObjectWidget(IBaseObject):
    ATTRIBUTES = IBaseObject.ATTRIBUTES.copy()
    ATTRIBUTES.update({"pos": tuple[int, int]})
    
    def __init__(self, *, id: int, name: str, pos: tuple[int, int], size: tuple[int, int], **kwargs: Any) -> None:
        super().__init__(id=id, name=name, size=size, **kwargs)
        self.pos: tuple[int, int] = pos