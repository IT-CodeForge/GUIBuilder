from intermediary.object.generic_object import GenericObject

class EditObject(GenericObject):
    def __init__(self, id: int) -> None:
        super().__init__(id, "edit")

        # Initialize default values.
        self.setAttribute("name", f"Edit{id}")
        self.setAttribute("text", "Edit")
        self.setAttribute("position", [0, 0])
        self.setAttribute("size", [200, 100])
        self.setAttribute("textColor", [0, 0, 0])
        self.setAttribute("backgroundColor", [255, 255, 255])
        self.setAttribute("multipleLines", True)
        self.setAttribute("eventChanged", False)
		self.setAttribute("eventHovered", False)