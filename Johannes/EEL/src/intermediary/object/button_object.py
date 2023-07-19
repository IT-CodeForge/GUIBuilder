from intermediary.object.generic_object import GenericObject

class ButtonObject(GenericObject):
    def __init__(self, id: int) -> None:
        super().__init__(id, "button")

        # Initialize default values.
        self.setAttribute("name", f"Button{id}")
        self.setAttribute("text", "Button")
        self.setAttribute("position", [0, 0])
        self.setAttribute("size", [20, 20])
        self.setAttribute("color", [127, 127, 127])