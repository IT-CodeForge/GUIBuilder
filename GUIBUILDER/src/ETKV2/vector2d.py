from __future__ import annotations
import math
from typing import Optional, overload


class vector2d:
    @overload
    def __init__(self, x: float = 0, y: float = 0) -> None:
        pass

    @overload
    def __init__(self, *, lenght: float, radians: float) -> None:
        pass

    def __init__(self, x: Optional[float] = None, y: Optional[float] = None, *, lenght: Optional[float] = None, radians: Optional[float] = None) -> None:
        self.x = 0.0
        self.y = 0.0

        if lenght != None and radians != None:
            if x != None or y != None:
                self.__raise_error()
            self.x = math.cos(radians) * lenght
            self.y = math.sin(radians) * lenght
        elif x != None and y != None:
            if lenght != None or radians != None:
                self.__raise_error()
            self.x = x
            self.y = y

    def __raise_error(self) -> None:
        raise TypeError(
            "Expected: vector2d(x:float, y:float) or vector2d(*, lenght:float, radians:float)")

    @property
    def lenght(self) -> float:
        return self.__get_lenght()

    @lenght.setter
    def lenght(self, value: float) -> None:
        self.normalize()
        self *= value

    def __add__(self, other: vector2d) -> vector2d:  # defines behaviour on + operand
        try:
            return vector2d(self.x + other.x, self.y + other.y)
        except:
            raise ValueError("You can only add a vector2 to a vector2")

    def __iadd__(self, other: vector2d) -> vector2d:  # defines behaviour on += operand
        try:
            return vector2d(self.x + other.x, self.y + other.y)
        except:
            raise ValueError("You can only add a vector2d to a vector2d")

    def __sub__(self, other: vector2d) -> vector2d:  # defines behaviour on - operand
        try:
            return vector2d(self.x - other.x, self.y - other.y)
        except:
            raise ValueError("You can only subtract a vector2d to a vector2d")

    def __isub__(self, other: vector2d) -> vector2d:  # defines behaviour on -= operand
        try:
            return vector2d(self.x - other.x, self.y - other.y)
        except:
            raise ValueError("You can only subtract a vector2d to a vector2d")

    def __mul__(self, other: int | float | vector2d) -> vector2d:  # defines behaviour on * operand
        if type(other) == float or type(other) == int:
            return vector2d(self.x * other, self.y * other)
        elif type(other) == vector2d:
            return vector2d(self.x * other.x, self.y * other.y)
        raise ValueError("incompatible types")

    def __rmul__(self, other: int | float | vector2d) -> vector2d:  # defines behaviour on * operand
        if type(other) == float or type(other) == int:
            return vector2d(self.x * other, self.y * other)
        elif type(other) == vector2d:
            return vector2d(self.x * other.x, self.y * other.y)
        raise ValueError("incompatible types")

    # defines behaviour on *= operand
    def __imul__(self, other: int | float | vector2d) -> vector2d:
        if type(other) == float or type(other) == int:
            return vector2d(self.x * other, self.y * other)
        elif type(other) == vector2d:
            return vector2d(self.x * other.x, self.y * other.y)
        raise ValueError("incompatible types")

    # defines behaviour on / operand
    def __truediv__(self, other: int | float | vector2d) -> vector2d:
        if type(other) == float or type(other) == int:
            return vector2d(self.x / other, self.y / other)
        elif type(other) == vector2d:
            return vector2d(self.x / other.x, self.y / other.y)
        raise ValueError("incompatible types")

    # defines behaviour on /= operand
    def __idiv__(self, other: int | float | vector2d) -> vector2d:
        if type(other) == float or type(other) == int:
            return vector2d(self.x / other, self.y / other)
        elif type(other) == vector2d:
            return vector2d(self.x / other.x, self.y / other.y)
        raise ValueError("incompatible types")

    def __mod__(self, other: int) -> vector2d:  # defines behaviour on % operand
        if type(other) == int:
            return vector2d(self.x % other, self.y % other)
        raise ValueError("incompatible types")

    def __imod__(self, other: int) -> vector2d:  # defines behaviour on %= operand
        if type(other) == int:
            return vector2d(self.x % other, self.y % other)
        raise ValueError("incompatible types")

    def __pow__(self, other: int) -> vector2d:  # defines behaviour on ** operand
        if type(other) == int:
            return vector2d(self.x ** other, self.y ** other)
        raise ValueError("incompatible types")

    def __ipow__(self, other: int) -> vector2d:  # defines behaviour on **= operand
        if type(other) == int:
            return vector2d(self.x ** other, self.y ** other)
        raise ValueError("incompatible types")

    def __eq__(self, other: object) -> bool:
        if type(other) == float or type(other) == int:
            return self.__get_lenght() == other
        elif type(other) == vector2d:
            return self.x == other.x and self.y == other.y
        raise ValueError("incompatible compare types")

    def __lt__(self, other: int | float | vector2d) -> bool:
        if type(other) == float or type(other) == int:
            return self.__get_lenght() < other
        elif type(other) == vector2d:
            return self.x < other.x and self.y < other.y
        raise ValueError("incompatible compare types")

    def __le__(self, other: int | float | vector2d) -> bool:
        if type(other) == float or type(other) == int:
            return self.__get_lenght() <= other
        elif type(other) == vector2d:
            return self.x <= other.x and self.y <= other.y
        raise ValueError("incompatible compare types")

    def __gt__(self, other: int | float | vector2d) -> bool:
        if type(other) == float or type(other) == int:
            return self.__get_lenght() > other
        elif type(other) == vector2d:
            return self.x > other.x and self.y > other.y
        raise ValueError("incompatible compare types")

    def __ge__(self, other: int | float | vector2d) -> bool:
        if type(other) == float or type(other) == int:
            return self.__get_lenght() >= other
        elif type(other) == vector2d:
            return self.x >= other.x and self.y >= other.y
        raise ValueError("incompatible compare types")

    def __setitem__(self, address: int, other: float) -> None:
        if address not in [0, 1]:
            raise KeyError("Invalid index")
        if address == 0:
            self.x = other
        else:
            self.y = other

    def __getitem__(self, address: int) -> float:
        if address not in [0, 1]:
            raise KeyError("Invalid index")
        if address == 0:
            return self.x
        else:
            return self.y

    def __str__(self) -> str:
        return f"<{self.x}, {self.y}>"

    def __get_lenght(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)

    def get_rotation(self) -> float:
        if self.y >= 0:
            return math.acos(self.x/self.__get_lenght())
        return 2 * math.pi - math.acos(self.x/self.__get_lenght())

    def normalize(self) -> vector2d:
        lenght = self.__get_lenght()
        if not lenght:
            return self
        return self / lenght

    def rotate(self, radians: float) -> vector2d:
        tempx = round(self.x*math.cos(radians) - self.y*math.sin(radians), 10)
        tempy = round(self.x*math.sin(radians) + self.y*math.cos(radians), 10)
        return vector2d(tempx, tempy)

    def switch(self) -> vector2d:
        return vector2d(self.y, self.x)

    def get_angle_to_vec(self, vector: vector2d) -> float:
        calc_vec_self = self.normalize()
        calc_vec_other = vector.normalize()
        return math.acos(calc_vec_self.dotproduct(calc_vec_other))

    def dotproduct(self, vector: vector2d) -> float:
        try:
            return self.x * vector.x + self.y * vector.y
        except:
            raise ValueError("You can only do a dotproduct of two vectors")

    def crossproduct(self, vector: vector2d) -> float:
        try:
            return self.x*vector.y - self.y*vector.x
        except:
            raise ValueError("You can only do a crossproduct of two vectors")

    def copy(self) -> vector2d:
        return vector2d(self.x, self.y)
