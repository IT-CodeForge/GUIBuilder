from enum import Enum
from multiprocessing import Event
from intermediary.object.object_attribute import ObjectAttribute
from intermediary.object.generic_object import GenericObject
from intermediary.object.window_object import WindowObject
from intermediary.object.button_object import ButtonObject

class ObjectEnum(Enum):
    WINDOW = 0
    BUTTON = 1

class EventEnum(Enum):
    Timer = 0
    KeyUp = 1
    KeyDown = 2
    MouseMove = 3
    MouseClick = 4
    Paint = 5

class Intermediary:
    def __init__(self) -> None:
        self.__enum_mapping: dict[ObjectEnum, type] = {
            ObjectEnum.WINDOW: WindowObject,
            ObjectEnum.BUTTON: ButtonObject
        }

        self.__string_mapping: dict[str, type] = {
            "window": WindowObject,
            "button": ButtonObject
        }

        self.__objects: list[GenericObject] = []
        self.__count: int = 0

        self.__timer_enabled = False
        self.__key_up_enabled = False
        self.__key_down_enabled = False
        self.__mouse_move_enabled = False
        self.__mouse_click_enabled = False
        self.__paint_enabled = False

    def createObject(self, type: ObjectEnum) -> int:
        object_type: type = self.__enum_mapping.get(type)

        if object_type == None:
            print(f"Error: An object mapping called {type} could not be found.")
            return

        object_id: int = self.__count
        self.__count = self.__count + 1

        object: GenericObject = object_type(object_id)
        self.__objects.append(object)

        return object_id

    def removeObject(self, id: int) -> None:
        for object in self.__objects:
            if object.getAttribute("id") == id:
                self.__objects.remove(object)
                return

        print(f"Error: An object with the ID {id} could not be removed.")

    def getObject(self, id: int) -> GenericObject:
        for object in self.__objects:
            if object.getAttribute("id") == id:
                return object

        print(f"Error: An object with the ID {id} could not be retrieved.")

    def loadObjects(self, objects: list[dict[str, any]]) -> None:
        # Clear all objects.
        self.__objects = []
        self.__count = 0

        for object in objects:
            object_type: type = self.__string_mapping.get(object["type"])
            object_id: int = object["id"]
            new_object: GenericObject = object_type(object_id)

            self.__objects.append(new_object)

            # Apply all available attributes to the object.
            for attribute in object:
                new_object.setAttribute(attribute, object[attribute])
                
    def getObjects(self) -> list[dict[str, any]]:
        objects: list[dict[str, any]] = []

        for object in self.__objects:
            attributes: list[ObjectAttribute] = object.getAttributes()
            dictionary: dict[str, any] = {}

            # Create a dictionary containing the object's attributes.
            for attribute in attributes:
                name: str = attribute.getName()
                value: any = attribute.getValue()

                dictionary[name] = value

            # Append the object's attributes to the list.
            objects.append(dictionary)
            
        return objects

    def setEvent(self, type: EventEnum) -> None:
        if type == EventEnum.Timer:
            self.__timer_enabled = True
        elif type == EventEnum.KeyUp:
            self.__key_up_enabled = True
        elif type == EventEnum.KeyDown:
            self.__key_down_enabled = True
        elif type == EventEnum.MouseMove:
            self.__mouse_move_enabled = True
        elif type == EventEnum.MouseClick:
            self.__mouse_click_enabled = True
        elif type == EventEnum.Paint:
            self.__paint_enabled = True

    def clearEvent(self, type: EventEnum) -> None:
        if type == EventEnum.Timer:
            self.__timer_enabled = False
        elif type == EventEnum.KeyUp:
            self.__key_up_enabled = False
        elif type == EventEnum.KeyDown:
            self.__key_down_enabled = False
        elif type == EventEnum.MouseMove:
            self.__mouse_move_enabled = False
        elif type == EventEnum.MouseClick:
            self.__mouse_click_enabled = False
        elif type == EventEnum.Paint:
            self.__paint_enabled = False

    def getEvents(self) -> dict[str, bool]:
        events: dict[str, bool] = {}

        events["timer_enabled"] = self.__timer_enabled
        events["keyup_enabled"] = self.__key_up_enabled
        events["keydown_enabled"] = self.__key_down_enabled
        events["mousemove_enabled"] = self.__mouse_move_enabled
        events["mouseclick_enabled"] = self.__mouse_click_enabled
        events["paint_enabled"] = self.__paint_enabled

        return events

    def loadEvents(self, events: dict[str, bool]) -> None:
        self.__timer_enabled = events["timer_enabled"]
        self.__timer_enabled = events["keyup_enabled"]
        self.__timer_enabled = events["keydown_enabled"]
        self.__timer_enabled = events["mousemove_enabled"]
        self.__timer_enabled = events["mouseclick_enabled"]
        self.__timer_enabled = events["paint_enabled"]