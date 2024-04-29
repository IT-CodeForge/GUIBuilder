class BaseObject:
    def __init__(self, id: int) -> None:
        self.__id = id

    @property
    def id(self) -> int:
        """READ-ONLY"""
        return self.__id