from intermediary.object.generic_object import GenericObject

class TimerObject(GenericObject):
    def __init__(self, id: int) -> None:
        super().__init__(id, "timer")

        # Initialize default values.
        self.setAttribute("name", f"Timer{id}")
        self.setAttribute("position", [0, 0])
        self.setAttribute("size", [40, 18])
        self.setAttribute("enabled", True)