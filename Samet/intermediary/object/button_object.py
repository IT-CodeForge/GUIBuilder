from intermediary.object.generic_object import GenericObject

class ButtonObject(GenericObject):
    def __init__(self, id: int) -> None:
        super().__init__(id, "button")