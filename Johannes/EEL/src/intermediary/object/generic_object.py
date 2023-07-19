from intermediary.object.object_attribute import ObjectAttribute

class GenericObject:
    def __init__(self, id: int, type: str) -> None:
        self.__attributes: list[ObjectAttribute] = []

        # Create an 'id' attribute.
        type_attribute = ObjectAttribute("id", id)
        self.__attributes.append(type_attribute)

        # Create a 'type' attribute.
        type_attribute = ObjectAttribute("type", type)
        self.__attributes.append(type_attribute)

    def setAttribute(self, name: str, value: any) -> None:
        if len(self.__attributes) <= 0:
            print("Error: Object does not have any attributes.")
            return
        
        for attribute in self.__attributes:
            # If the attribute already exists, set its value.
            if attribute.getName() == name:
                attribute.setValue(value)
                return

        # Attribute does not exist yet. Create a new attribute.
        attribute = ObjectAttribute(name, value)
        self.__attributes.append(attribute)

    def getAttribute(self, name: str) -> any:
        for attribute in self.__attributes:
            # If the attribute is found, return its value.
            if attribute.getName() == name:
                return attribute.getValue()

        # Attribute could not be found.
        print(f"Error: An attribute with the name '{name}' could not be retrieved.")

    def removeAttribute(self, name: str) -> None:
        for attribute in self.__attributes:
            if attribute.getName() == name:
                self.__attributes.remove(attribute)
                return

        print(f"Error: An attribute with the name '{name}' could not be removed.")

    def getAttributes(self) -> list[ObjectAttribute]:
        return self.__attributes
        
    def getAttributesAsDictionary(self) -> dict[str, any]:
        attributes: list[ObjectAttribute] = self.getAttributes()
        dictionary: dict[str, any] = {}

        # Create a dictionary containing the object's attributes.
        for attribute in attributes:
            name: str = attribute.getName()
            value: any = attribute.getValue()

            dictionary[name] = value
        
        return dictionary