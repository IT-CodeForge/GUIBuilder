from typing import Optional
from .IBaseObject import IBaseObject


class IBaseObjectWidget(IBaseObject):
    ATTRIBUTES = IBaseObject.ATTRIBUTES.copy()
    ATTRIBUTES.update({"pos": tuple[int, int]})
    
    def __init__(self, id: int, name: Optional[str], pos: tuple[int, int], size: tuple[int, int]) -> None:
        super().__init__(id, name, size)
        self.pos: tuple[int, int] = pos