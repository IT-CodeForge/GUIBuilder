from intermediary.object.generic_object import GenericObject

class CanvasObject(GenericObject):
    def __init__(self, id: int) -> None:
        super().__init__(id, "canvas")

        # Initialize default values.
        self.setAttribute("name", f"canvas{id}")
        self.setAttribute("position", [0, 0])
        self.setAttribute("size", [100, 100])
        self.setAttribute("backgroundColor", [255, 255, 255])
        self.setAttribute("eventHovered", False)