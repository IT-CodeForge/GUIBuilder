from ast import parse, dump

def test(x: int, y: int):
    print(x,y)

if __name__ == "__main__":
    print(dump(parse(f"def e{1}_knopf_pressed(self, params: tuple[ETKBaseObject, ETKEvents, Any]):\n   pass").body[0], indent=2))
