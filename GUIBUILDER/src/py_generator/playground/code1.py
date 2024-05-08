from math import pi

class Test2:
    def __init__(self) -> None:
        pass

    def temp(self, x: int):
        print(x)

class Test:
    def __init__(self, x: int=1) -> None:
        print("init", x)
        self.my_test = Test2()
        self.my_test.temp(3)

    def foo(self) -> float:
        print("foo")
        return pi

    def bar(self, val: str):
        print("bar", val)
