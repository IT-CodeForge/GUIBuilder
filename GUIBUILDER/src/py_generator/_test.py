def test(x: int, y: int):
    print(x,y)

if __name__ == "__main__":
    temp: dict[str, list[str]] = {}
    temp["k"] = temp.get("k", []) + ["h"]
    print(temp)
    temp["k"] = temp["k"] + ["h"]
    print(temp)
