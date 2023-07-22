from intermediary.object.generic_object import GenericObject

class WindowObject(GenericObject):
    def __init__(self, id: int) -> None:
        super().__init__(id, "window")

        # Initialize default values.
        self.setAttribute("name", f"Window")
        self.setAttribute("text", "Window")
        self.setAttribute("size", [500, 500])
        self.setAttribute("textColor", [0, 0, 0])
        self.setAttribute("backgroundColor", [255, 255, 255])
        self.setAttribute("eventCreate", False)
        self.setAttribute("eventDestroy", False)
        self.setAttribute("eventPaint", False)
        self.setAttribute("eventResize", False)
        self.setAttribute("eventMouseClick", False)
        self.setAttribute("eventMouseMove", False)