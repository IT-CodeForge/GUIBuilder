import json
import os.path
from intermediary.intermediary import Intermediary

class JSON:
    def __init__(self, intermediary: Intermediary) -> None:
        self.__intermediary = intermediary

    def load(self, name: str) -> None:
        objects: list[dict[str, any]] = []

        with open(os.path.join(name, "gui_objects.json"), "r") as file:
            objects = json.loads(file.read())

        self.__intermediary.loadObjectsFromDictionaryList(objects)

    def save(self, name: str) -> None:
        objects: list[dict[str, any]] = self.__intermediary.getObjectsAsDictionaryList()

        with open(os.path.join(name, "gui_objects.json"), "w") as file:
            file.write(json.dumps(objects, indent = 4))