from typing import Any, Type, Optional


class IBaseObject:
    ATTRIBUTES: dict[str, Type[Any]] = {"id": int, "name": Optional[str], "size": tuple[int, int]}

    def __init__(self, id: int, name: Optional[str], size: tuple[int, int]) -> None:
        if name == None:
            name = f"{id}_button"
        self.__id: int = id
        self.name: str = name
        self.size: tuple[int, int] = size

    @property
    def id(self) -> int:
        """READ-ONLY"""
        return self.__id

    def get_attributes_as_dict(self) -> dict[str, Any]:
        ad: dict[str, Any] = {}
        for a in self.ATTRIBUTES:
            ad.update({a: getattr(self, a)})
        return ad

    def __str__(self) -> str:
        ad = self.get_attributes_as_dict().items()
        s = [f"{a}: {repr(v)}" for a, v in ad]
        s2 = "; ".join(s)
        return f"{type(self).__name__}<{s2}>"

    def __repr__(self) -> str:
        st = self.__str__()
        st = st[:st.find("<") + 1] + f"self: {super().__repr__()}; " + st[st.find("<") + 1:]
        return st
