from enum import Enum

class TEST(Enum):
    A = 1
    B = 2

def temp(val:TEST):
    print(str(val.name))

if __name__ == "__main__":
    temp(TEST.A)