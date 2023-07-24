from enum import Enum
from intermediary.object.object_attribute import ObjectAttribute
from intermediary.object.generic_object import GenericObject
from intermediary.object.window_object import WindowObject
from intermediary.object.button_object import ButtonObject
from intermediary.object.label_object import LabelObject
from intermediary.object.edit_object import EditObject
from intermediary.object.checkbox_object import CheckboxObject
from intermediary.object.timer_object import TimerObject
from intermediary.object.canvas_object import CanvasObject

class ObjectEnum(Enum):
    WINDOW = 0
    BUTTON = 1
    LABEL = 2
    EDIT = 3
    CHECKBOX = 4
    TIMER = 5
    CANVAS = 6

class EventEnum(Enum):
    TIMER = 0
    KEY_UP = 1
    KEY_DOWN = 2
    MOUSE_MOVE = 3
    MOUSE_CLICK = 4
    PAINT = 5

class Intermediary:
    """A class which is used to handle communication between the client and generator. Intermediate representation of data."""

    def __init__(self) -> None:
        self.__enum_mapping: dict[ObjectEnum, type] = {
            ObjectEnum.WINDOW: WindowObject,
            ObjectEnum.BUTTON: ButtonObject,
            ObjectEnum.LABEL: LabelObject,
            ObjectEnum.EDIT: EditObject,
            ObjectEnum.CHECKBOX: CheckboxObject,
            ObjectEnum.TIMER: TimerObject,
            ObjectEnum.CANVAS: CanvasObject
        }

        self.__string_mapping: dict[str, type] = {
            "window": WindowObject,
            "button": ButtonObject,
            "label": LabelObject,
            "edit": EditObject,
            "checkbox": CheckboxObject,
            "timer": TimerObject,
            "canvas": CanvasObject
        }

        self.__objects: list[GenericObject] = []
        self.__count: int = 0
    
    def createObject(self, type: ObjectEnum) -> int:
        """Creates an intermediate representation of an object."""

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
        """Removes an intermediate representation of an object."""

        for object in self.__objects:
            if object.getAttribute("id") == id:
                self.__objects.remove(object)
                return

        print(f"Error: An object with the ID {id} could not be removed.")

    def getObject(self, id: int) -> GenericObject:
        """Retrieves an intermediate representation of an object."""

        for object in self.__objects:
            if object.getAttribute("id") == id:
                return object

        print(f"Error: An object with the ID {id} could not be retrieved.")

    def loadObjectsFromDictionaryList(self, objects: list[dict[str, any]]) -> None:
        """Loads a list of objects in dictionary format."""

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
        """Retrieves a list of objects in intermediate representation."""

        return self.__objects

    def getObjectsAsDictionaryList(self) -> list[dict[str, any]]:
        """Retrieves a list of objects in dictionary format."""

        objects: list[dict[str, any]] = []

        for object in self.__objects:
            # Append the object's attributes to the list.
            objects.append(object.getAttributesAsDictionary())
            
        return objects