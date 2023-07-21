from enum import Enum
from intermediary.object.object_attribute import ObjectAttribute
from intermediary.object.generic_object import GenericObject
from intermediary.object.window_object import WindowObject
from intermediary.object.button_object import ButtonObject
from intermediary.object.label_object import LabelObject
from intermediary.object.edit_object import EditObject
from intermediary.object.checkbox_object import CheckboxObject

class ObjectEnum(Enum):
    WINDOW = 0
    BUTTON = 1
    LABEL = 2
    EDIT = 3
    CHECKBOX = 4

class EventEnum(Enum):
    TIMER = 0
    KEY_UP = 1
    KEY_DOWN = 2
    MOUSE_MOVE = 3
    MOUSE_CLICK = 4
    PAINT = 5

class Intermediary:
    def __init__(self) -> None:
        self.__enum_mapping: dict[ObjectEnum, type] = {
            ObjectEnum.WINDOW: WindowObject,
            ObjectEnum.BUTTON: ButtonObject,
            ObjectEnum.LABEL: LabelObject,
            ObjectEnum.EDIT: EditObject,
            ObjectEnum.CHECKBOX, CheckboxObject
        }

        self.__string_mapping: dict[str, type] = {
            "window": WindowObject,
            "button": ButtonObject,
            "label": LabelObject,
            "edit": EditObject,
            "checkbox": CheckboxObject,
        }

        self.__objects: list[GenericObject] = []
        self.__count: int = 0
    
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
    
    def getObjects(self) -> list[GenericObject]:
        return self.__objects

    def getObjectsAsDictionaryList(self) -> list[dict[str, any]]:
        objects: list[dict[str, any]] = []

        for object in self.__objects:
            # Append the object's attributes to the list.
            objects.append(object.getAttributesAsDictionary())
            
        return objects