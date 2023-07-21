from intermediary.object.generic_object import GenericObject

class LabelObject(GenericObject):
    def __init__(self, id: int) -> None:
        super().__init__(id, "label")

        # Initialize default values.
        self.setAttribute("name", f"Label{id}")
        self.setAttribute("text", "Label")
        self.setAttribute("position", [0, 0])
        self.setAttribute("size", [75, 25])
        self.setAttribute("textColor", [0, 0, 0])
        self.setAttribute("backgroundColor", [255, 255, 255])