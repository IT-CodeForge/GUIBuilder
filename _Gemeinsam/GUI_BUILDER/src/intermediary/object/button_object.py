from intermediary.object.generic_object import GenericObject

class ButtonObject(GenericObject):
    def __init__(self, id: int) -> None:
        super().__init__(id, "button")

        # Initialize default values.
        self.setAttribute("name", f"button{id}")
        self.setAttribute("text", "Button")
        self.setAttribute("position", [0, 0])
        self.setAttribute("size", [70, 25])
        self.setAttribute("textColor", [0, 0, 0])
        self.setAttribute("backgroundColor", [255, 255, 255])
        self.setAttribute("eventPressed", True)
        self.setAttribute("eventDoublePressed", False)
        self.setAttribute("eventHovered", False)