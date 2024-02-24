from __future__ import annotations
import math
from typing import Optional

class vector2d:
    def __init__(self, x:Optional[float]=None, y:Optional[float]=None, lenght:Optional[float]=None, radians:Optional[float]=None):
        
        self.x = 0.0
        self.y = 0.0

        if lenght != None and radians != None:
            self.x = math.cos(radians) * lenght
            self.y = math.sin(radians) * lenght
        elif x != None and y != None:
            self.x = x
            self.y = y
    
    @property
    def lenght(self)->float:
        return self.__get_lenght()
    
    @lenght.setter
    def lenght(self, value:float):
        self.normalize()
        self *= value
    
    def __add__(self, other:vector2d)->vector2d:  #defines behaviour on + operand
        try:
            return vector2d(self.x + other.x, self.y + other.y)
        except:
            raise ValueError("You can only add a vector2 to a vector2")
        
    def __iadd__(self, other:vector2d)->vector2d: #defines behaviour on += operand
        try:
            return vector2d(self.x + other.x, self.y + other.y)
        except:
            raise ValueError("You can only add a vector2d to a vector2d")
    
    def __sub__(self, other:vector2d)->vector2d: #defines behaviour on - operand
        try:
            return vector2d(self.x -other.x, self.y -other.y)
        except:
            raise ValueError("You can only subtract a vector2d to a vector2d")
    
    def __isub__(self, other:vector2d)->vector2d: #defines behaviour on -= operand
        try:
            return vector2d(self.x -other.x, self.y -other.y)
        except:
            raise ValueError("You can only subtract a vector2d to a vector2d")
        
    def __mul__(self, other: int|float|vector2d)->vector2d: #defines behaviour on * operand
        if type(other) in [float, int]:
            return vector2d(self.x * other, self.y * other)
        try:
            return vector2d(self.x * other.x, self.y * other.y)
        except:
            raise ValueError("You must multiply either vector2 with vector2d or vector2d with float or int")
    
    def __rmul__(self, other: int|float|vector2d)->vector2d: #defines behaviour on * operand           
        if type(other) in [float,int]:
            return vector2d(self.x * other, self.y * other)
        try:
            return vector2d(self.x * other.x, self.y * other.y)
        except:
            raise ValueError("You must multiply either vector2 with vector2d or vector2d with float or int")
    
    def __imul__(self, other: int|float|vector2d)->vector2d: #defines behaviour on *= operand
        if type(other) in [float,int]:
            return vector2d(self.x * other, self.y * other)
        try:
            return vector2d(self.x * other.x, self.y * other.y)
        except:
            raise ValueError("You must multiply either vector2 with vector2d or vector2d with float or int")
    
    def __truediv__(self, other: int|float|vector2d)->vector2d: #defines behaviour on / operand
        if type(other) in [float,int]:
            return vector2d(self.x / other, self.y / other)
        try:
            return vector2d(self.x / other.x, self.y / other.y)
        except:
            raise ValueError("You must multiply either vector2 with vector2d or vector2d with float or int")
    
    def __idiv__(self, other: int|float|vector2d)->vector2d: #defines behaviour on /= operand            
        if type(other) in [float,int]:
            return vector2d(self.x / other, self.y / other)
        try:
            return vector2d(self.x / other.x, self.y / other.y)
        except:
            raise ValueError("You must multiply either vector2 with vector2d or vector2d with float or int")
    
    def __mod__(self, other:vector2d)->vector2d: #defines behaviour on % operand
        try:
            return vector2d(self.x % other, self.y % other)
        except:
            raise ValueError("You can only modulate a Vector with an int")
    
    def __imod__(self, other:vector2d)->vector2d: #defines behaviour on %= operand
        try:
            return vector2d(self.x % other, self.y % other)
        except:
            raise ValueError("You can only modulate a Vector with an int")
    
    def __pow__(self, other:vector2d)->vector2d: #defines behaviour on ** operand
        try:
            return vector2d(self.x ** other, self.y ** other)
        except:
            raise ValueError("You can only a vector2d to the power of an int or float")
    
    def __ipow__(self, other:vector2d)->vector2d: #defines behaviour on **= operand
        try:
            return vector2d(self.x ** other, self.y ** other)
        except:
            raise ValueError("You can only a vector2d to the power of an int or float")
    

    def __eq__(self, other: int|float|vector2d)->bool:
        if type(other) in [float, int]:
            return self.__get_lenght() == other
        if other == None:
            return False
        try:
            return self.x == other.x and self.y == other.y
        except:
            raise ValueError("You can only compare a vector2d with a vector2d")
    
    def __lt__(self, other: int|float|vector2d)->bool:
        if type(other) in [float, int]:
            return self.__get_lenght() < other
        if other == None:
            return False
        try:
            return self.x < other.x and self.y < other.y
        except:
            raise ValueError("You can only compare a vector2d with a vector2d")

    def __le__(self, other: int|float|vector2d)->bool:
        if type(other) in [float, int]:
            return self.__get_lenght() <= other
        if other == None:
            return False
        try:
            return self.x <= other.x and self.y <= other.y
        except:
            raise ValueError("You can only compare a vector2d with a vector2d")

    def __gt__(self, other: int|float|vector2d)->bool:
        if type(other) in [float, int]:
            return self.__get_lenght() > other
        if other == None:
            return False
        try:
            return self.x > other.x and self.y > other.y
        except:
            raise ValueError("You can only compare a vector2d with a vector2d")

    def __ge__(self, other: int|float|vector2d)->bool:
        if type(other) in [float, int]:
            return self.__get_lenght() >= other
        if other == None:
            return False
        try:
            return self.x >= other.x and self.y >= other.y
        except:
            raise ValueError("You can only compare a vector2d with a vector2d")

    
    def __str__(self)->str:
        return f"<{self.x}, {self.y}>"


    
    def __get_lenght(self)->float:
        return math.sqrt( self.x**2 + self.y**2)
    
    def get_rotation(self)->float:
        if self.y >= 0:
            return math.acos(self.x/self.__get_lenght())
        return 2 * math.pi - math.acos(self.x/self.__get_lenght())
    
    def normalize(self, change_self:bool=True)->vector2d:
        lenght = self.__get_lenght()
        if not lenght:
            if change_self:
                self.x,self.y = 0.0,0.0
            return vector2d(self.x, self.y)
        if change_self:
            self.x = self.x / lenght
            self.y = self.y / lenght
        return self / lenght
    
    def rotate(self, radians:float, change_self:bool=True)->vector2d:
        tempx = round(self.x*math.cos(radians) - self.y*math.sin(radians), 10)
        tempy = round(self.x*math.sin(radians) + self.y*math.cos(radians), 10)
        if change_self:
            self.x,self.y = tempx,tempy
        return vector2d(tempx, tempy)
    
    def switch(self, change_self:bool=True)->vector2d:
        if change_self:
            self.x, self.y = self.y, self.x
        return vector2d(self.y, self.x)
    
    def get_angle_to_vec(self, vector:vector2d)->float:
        calc_vec_self = self.normalize(False)
        calc_vec_other = vector.normalize(False)
        return math.acos(calc_vec_self.dotproduct(calc_vec_other))
    
    def dotproduct(self, vector:vector2d)->float:
        try:
            return self.x * vector.x + self.y * vector.y
        except:
            raise ValueError("You can only do a dotproduct of two vectors")
    
    def crossproduct(self, vector:vector2d)->float:
        try:
            return self.x*vector.y - self.y*vector.x
        except:
            raise ValueError("You can only do a crossproduct of two vectors")