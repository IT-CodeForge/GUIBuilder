from typing import Final
from easy_tkinter.ETKButton import ETKButton
from easy_tkinter.ETKCheckbox import ETKCheckbox
from easy_tkinter.ETKContainer import ETKContainer
from easy_tkinter.ETKLabel import ETKLabel
from easy_tkinter.ETKMainWindow import ETKMainWindow
from easy_tkinter.ETKListingContainer import ETKListingContainer, ListingTypes
from easy_tkinter.vector2d import vector2d


class GUI(ETKMainWindow):
    def init(self) -> None:
        super().__init__(pos_x=0, pos_y=0, width=1540, height=768)

    MENUBAR_PADDING: Final = 10
    MENUBAR_HEIGHT: Final = 40
    MENUBAR_ELEMENT_HEIGHT: Final = 20
    ATTRIBUTES_WIDTH: Final = 100

    def add_elements(self):
        self.main = ETKListingContainer(offset=0)
        self.main.pos = vector2d(0, 0)
        self.main.height = self.height
        self.main.width = self.width

        self.menubar = ETKContainer()
        self.menubar.pos = vector2d(0, 0)
        self.menubar.width = self.main.width
        self.menubar.height = self.MENUBAR_HEIGHT
        self.main.elements.append(self.menubar)  # type:ignore

        self.menubar_left = ETKListingContainer(
            listing_type=ListingTypes.LEFT_TO_RIGHT, offset=self.MENUBAR_PADDING)
        self.menubar_left.pos = vector2d(self.ATTRIBUTES_WIDTH, 0)
        self.menubar_left.width = 500
        self.menubar_left.height = self.MENUBAR_HEIGHT
        self.menubar.add_element(self.menubar_left)  # type:ignore

        self.main2 = ETKListingContainer(
            listing_type=ListingTypes.LEFT_TO_RIGHT)
        self.main2.width = self.width
        self.main2.height = self.height - self.menubar.height
        self.main.elements.append(self.main2)  # type:ignore

        self.attributes = ETKListingContainer()
        self.attributes.width = self.ATTRIBUTES_WIDTH
        self.attributes.height = self.main2.height
        self.main2.elements.append(self.attributes)  # type:ignore

        # self.menubar.add_element(ETKLabel(self.object_id, width=self.menubar.width, height=self.menubar.height, fill=0xFF0000)) #type:ignore
        self.menubar_left.elements.append(ETKLabel(  # type:ignore
            self.object_id, width=self.menubar_left.width, height=self.menubar_left.height, fill=0xFF0000))
        # self.main2.elements.append(ETKLabel(self.object_id, width=self.main2.width, height=self.main2.height, fill=0x00FF00)) #type:ignore
        self.attributes.elements.append(ETKLabel(  # type:ignore
            self.object_id, width=self.attributes.width, height=self.attributes.height, fill=0xFFFF00))

        return

        self.menubar_button = ETKButton(
            self.object_id, "BUTTON", width=50, height=self.MENUBAR_ELEMENT_HEIGHT)
        self.menubar_button.enabled = False
        self.menubar_left.elements.append(self.menubar_button)  # type:ignore

        self.menubar_label = ETKLabel(
            self.object_id, "LABEL", width=50, height=self.MENUBAR_ELEMENT_HEIGHT)
        self.menubar_left.elements.append(self.menubar_label)  # type:ignore

        self.menubar_edit = ETKLabel(
            self.object_id, "EDIT", width=50, height=self.MENUBAR_ELEMENT_HEIGHT)
        self.menubar_left.elements.append(self.menubar_edit)  # type:ignore

        self.menubar_checkbox = ETKCheckbox(
            self.object_id, "CHECKBOX", width=100, height=self.MENUBAR_ELEMENT_HEIGHT)
        self.menubar_checkbox.enabled = False
        self.menubar_left.elements.append(self.menubar_checkbox)  # type:ignore

        self.menubar_canvas = ETKLabel(
            self.object_id, "CANVAS", width=70, height=self.MENUBAR_ELEMENT_HEIGHT)
        self.menubar_left.elements.append(self.menubar_canvas)  # type:ignore

        self.menubar_timer = ETKLabel(
            self.object_id, "TIMER", width=50, height=self.MENUBAR_ELEMENT_HEIGHT)
        self.menubar_left.elements.append(self.menubar_timer)  # type:ignore


if __name__ == "__main__":
    g = GUI()
    g.run()
