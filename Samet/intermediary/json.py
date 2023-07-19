import json
from intermediary.intermediary import Intermediary

class JSON:
    def __init__(self, intermediary: Intermediary) -> None:
        self.__intermediary = intermediary

    def load(self, name: str) -> None:
        objects: list[dict[str, any]] = []

        with open(f"{name}_objects.json", "r") as file:
            objects = json.loads(file.read())

        self.__intermediary.loadObjects(objects)

        events: dict[str, bool] = {} 

        with open(f"{name}_events.json", "r") as file:
            events = json.loads(file.read())

        self.__intermediary.loadEvents(events)

    def save(self, name: str) -> None:
        objects: list[dict[str, any]] = self.__intermediary.getObjects()

        with open(f"{name}_objects.json", "w") as file:
            file.write(json.dumps(objects, indent = 4))

        events: dict[str, bool] = self.__intermediary.getEvents()

        with open(f"{name}_events.json", "w") as file:
            file.write(json.dumps(events, indent = 4))