from .IBaseObject import IBaseObject


class IBaseObjectWidget(IBaseObject):
    ATTRIBUTES = IBaseObject.ATTRIBUTES.copy()
    ATTRIBUTES.update({"pos": tuple[int, int]})
    
    def __init__(self, id: int, name: str, pos: tuple[int, int], size: tuple[int, int]) -> None:
        IBaseObject.__init__(self, id, name, size)
        if IBaseObjectWidget in getattr(self, "_initialized", []):
            return
        self._initialized.append(IBaseObjectWidget)
        self.pos: tuple[int, int] = pos