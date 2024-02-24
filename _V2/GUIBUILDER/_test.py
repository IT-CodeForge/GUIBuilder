from vector2d import vector2d
from ast import literal_eval
from random   import randint
from time     import perf_counter

def cross_product(v1, v2):
    return v1[0] * v2[1] - v1[1] * v2[0]

def subtract(v1, v2):
    return [v1[0] - v2[0], v1[1] - v2[1]]

def find_intersection(p1:vector2d, p2:vector2d, p3:vector2d, p4:vector2d):
    s1 = p2-p1
    s2 = p4-p3

    denominator = s1.crossproduct(s2)

    if denominator == 0:
        return "Die Strecken sind entweder parallel oder kollinear"

    s = p3-p1
    t = s.crossproduct(s2) / denominator
    u = s.crossproduct(s1) / denominator

    if 0 <= t <= 1 and 0 <= u <= 1:
        intersection = p1 + t * s1
        return "Die Strecken schneiden sich im Punkt:", intersection
    else:
        return "Die Strecken schneiden sich nicht"

def gen_col_from_int(col:int)->str:
        if col == None:
            return ""
        hold_str = hex(col)[2:]
        if len(hold_str) < 6:
            hold_str = "0"*(6-len(hold_str)) + hold_str
        return "#" + hold_str

class Test:
    def hallo(self):
        print("hallo")
    
    def __del__(self):
        print("del")
 

if __name__ == "__main__":
    temp = {}
    temp["h"] = 1
    print(temp)
    
