from intermediary.object.generic_object import GenericObject

class CheckboxObject(GenericObject):
    def __init__(self, id: int) -> None:
        super().__init__(id, "checkbox")

        # Initialize default values.
        self.setAttribute("name", f"Checkbox{id}")
        self.setAttribute("text", "Checkbox")
        self.setAttribute("position", [0, 0])
        self.setAttribute("size", [100, 25])
        self.setAttribute("textColor", [0, 0, 0])
        self.setAttribute("backgroundColor", [255, 255, 255])
        self.setAttribute("checked", False)
        self.setAttribute("eventChanged", True)
        self.setAttribute("eventHovered", False)