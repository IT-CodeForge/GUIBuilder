class ObjectAttribute:
    def __init__(self, name: str, value: any) -> None:
        self.__name: str = name
        self.__value: any = value

    def setName(self, name: str) -> None:
        self.__name = name

    def getName(self) -> str:
        return self.__name

    def setValue(self, value: any) -> None:
        self.__value = value

    def getValue(self) -> any:
        return self.__value