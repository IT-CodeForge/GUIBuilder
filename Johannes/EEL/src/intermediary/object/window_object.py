from intermediary.object.generic_object import GenericObject

class WindowObject(GenericObject):
    def __init__(self, id: int) -> None:
        super().__init__(id, "window")

        # Initialize default values.
        self.setAttribute("name", f"Window{id}")
        self.setAttribute("name", "Window")
        self.setAttribute("position", [0, 0])
        self.setAttribute("size", [300, 300])
        self.setAttribute("color", [127, 127, 127])