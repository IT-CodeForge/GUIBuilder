import json
from intermediary.intermediary import Intermediary

class JSON:
    def __init__(self, intermediary: Intermediary) -> None:
        self.__intermediary = intermediary

    def load(self, name: str) -> None:
        objects: list[dict[str, any]] = []

        with open(f"{name}.json", "r") as file:
            objects = json.loads(file.read())

        self.__intermediary.setObjects(objects)

    def save(self, name: str) -> None:
        objects: list[dict[str, any]] = self.__intermediary.getObjects()

        with open(f"{name}.json", "w") as file:
            file.write(json.dumps(objects, indent = 4))