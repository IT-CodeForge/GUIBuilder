from typing import Final
from ETK import *


class GUI(ETKMainWindow):
    def __init__(self) -> None:
        super().__init__(size=vector2d(1920, 1015))

    LANGUAGES: Final = ["Python (ETK)", "C++ (TGW)"]
    MENUBAR_PADDING: Final = 10
    MENUBAR_HEIGHT: Final = 40
    MENUBAR_ELEMENT_HEIGHT: Final = 20
    ATTRIBUTES_WIDTH: Final = 300
    ATTRIBUTES_ELEMENT_HEIGHT: Final = 20

    def _add_elements(self):
        self.main = ETKListingContainer(self._tk_object, size=ETKContainerSize.from_vector2d(
            self.size), offset=0)

        self.menubar_outer = ETKContainer(self._tk_object, size=ETKContainerSize(
            self.main.size.x, self.MENUBAR_HEIGHT))
        self.main.add_element(self.menubar_outer)

        self.menubar_inner = ETKContainer(self._tk_object, vector2d(self.ATTRIBUTES_WIDTH, 0), size=ETKContainerSize(
            self.menubar_outer.size.x - self.ATTRIBUTES_WIDTH, self.MENUBAR_HEIGHT), outline_thickness=2)
        self.menubar_outer.add_element(self.menubar_inner)

        self.menubar_left = ETKListingContainer(self._tk_object, vector2d(0, 0), ETKContainerSize(0, self.MENUBAR_HEIGHT, True, False, self.MENUBAR_PADDING,
                                                self.MENUBAR_PADDING), listing_type=ETKListingTypes.LEFT_TO_RIGHT, alignment=ETKAlignments.MIDDLE_CENTER, offset=self.MENUBAR_PADDING, outline_thickness=2)
        self.menubar_inner.add_element(self.menubar_left)

        self.menubar_right = ETKListingContainer(self._tk_object, vector2d(0, 0), ETKContainerSize(0, self.MENUBAR_HEIGHT, True, False, self.MENUBAR_PADDING,
                                                 self.MENUBAR_PADDING), listing_type=ETKListingTypes.RIGHT_TO_LEFT, alignment=ETKAlignments.MIDDLE_CENTER, offset=self.MENUBAR_PADDING, outline_thickness=2)
        self.menubar_inner.add_element(self.menubar_right, ETKAlignments.TOP_RIGHT)

        self.main2 = ETKListingContainer(self._tk_object, size=ETKContainerSize(
            self.size.x, self.size.y-self.menubar_outer.size.y), listing_type=ETKListingTypes.LEFT_TO_RIGHT, offset=0)
        self.main.add_element(self.main2)

        self.attributes = ETKListingContainer(self._tk_object, size=ETKContainerSize(
            self.ATTRIBUTES_WIDTH, self.main2.size.y), offset=0)
        self.main2.add_element(self.attributes)

        self.attributes_element = ETKListingContainer(self._tk_object, size=ETKContainerSize(
            self.attributes.size.x, self.attributes.size.y/2, paddings_x_l=2, paddings_x_r=2, paddings_y_o=2, paddings_y_u=2), outline_thickness=2)
        self.attributes.add_element(self.attributes_element)

        self.attributes_window = ETKListingContainer(self._tk_object, size=ETKContainerSize(
            self.attributes.size.x, self.attributes.size.y/2, paddings_x_l=2, paddings_x_r=2, paddings_y_o=0, paddings_y_u=2), outline_thickness=2)
        self.attributes.add_element(self.attributes_window)

        self.element_area = ETKContainer(self._tk_object, size=ETKContainerSize(500, 500), background_color=0xFFFFFF)
        self.main2.add_element(self.element_area)

        # region Menubar_left Elemente

        self.menubar_button = ETKButton(
            self._tk_object, "BUTTON", size=vector2d(50, self.MENUBAR_ELEMENT_HEIGHT))
        self.menubar_button.enabled = False
        self.menubar_left.add_element(self.menubar_button)

        self.menubar_label = ETKLabel(
            self._tk_object, "LABEL", size=vector2d(50, self.MENUBAR_ELEMENT_HEIGHT))
        self.menubar_left.add_element(self.menubar_label)

        self.menubar_edit = ETKLabel(
            self._tk_object, "EDIT", size=vector2d(50, self.MENUBAR_ELEMENT_HEIGHT))
        self.menubar_left.add_element(self.menubar_edit)

        self.menubar_checkbox = ETKCheckbox(
            self._tk_object, "CHECKBOX", size=vector2d(100, self.MENUBAR_ELEMENT_HEIGHT))
        self.menubar_checkbox.enabled = False
        self.menubar_left.add_element(self.menubar_checkbox)

        self.menubar_canvas = ETKLabel(
            self._tk_object, "CANVAS", size=vector2d(70, self.MENUBAR_ELEMENT_HEIGHT))
        self.menubar_left.add_element(self.menubar_canvas)

        self.menubar_timer = ETKLabel(
            self._tk_object, "TIMER", size=vector2d(50, self.MENUBAR_ELEMENT_HEIGHT))
        self.menubar_left.add_element(self.menubar_timer)

        # endregion
        # region Menubar_right Elemente

        self.menubar_export = ETKButton(
            self._tk_object, "Export", size=vector2d(50, self.MENUBAR_ELEMENT_HEIGHT))
        self.menubar_export.add_event(
            ETKButtonEvents.PRESSED, lambda: None)  # TODO
        self.menubar_right.add_element(self.menubar_export)

        self.menubar_save = ETKButton(
            self._tk_object, "Save", size=vector2d(50, self.MENUBAR_ELEMENT_HEIGHT))
        self.menubar_save.add_event(
            ETKButtonEvents.PRESSED, lambda: None)  # TODO
        self.menubar_right.add_element(self.menubar_save)

        self.menubar_load = ETKButton(
            self._tk_object, "Load", size=vector2d(50, self.MENUBAR_ELEMENT_HEIGHT))
        self.menubar_load.add_event(
            ETKButtonEvents.PRESSED, lambda: None)  # TODO
        self.menubar_right.add_element(self.menubar_load)

        self.language_selector = ETKDropdownMenu(self._tk_object, self.LANGUAGES, size=vector2d(130, self.MENUBAR_ELEMENT_HEIGHT))
        self.menubar_right.add_element(self.language_selector)
        
        # self.language_selector = ETKLabel(self._tk_object, "LANGUAGE_SELECTOR", size=vector2d(
        #     150, self.MENUBAR_ELEMENT_HEIGHT))  # TODO
        # self.menubar_right.add_element(self.language_selector)

        # endregion
        # region attributes_element Elemente

        self.attributes_element_title_container = ETKContainer(self._tk_object, size=ETKContainerSize(
            self.attributes_element.size.x-4, self.ATTRIBUTES_ELEMENT_HEIGHT))
        self.attributes_element.add_element(
            self.attributes_element_title_container)

        self.attributes_element_title = ETKLabel(self._tk_object, "Element-Eigenschaften:", size=vector2d(
            180, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=self.attributes_element.background_color)
        self.attributes_element_title_container.add_element(
            self.attributes_element_title, ETKAlignments.MIDDLE_CENTER)

        # endregion

        #region window_element Elemente

        self.attributes_window_title_container = ETKContainer(self._tk_object, size=ETKContainerSize(
            self.attributes_window.size.x-4, self.ATTRIBUTES_ELEMENT_HEIGHT))
        self.attributes_window.add_element(
            self.attributes_window_title_container)

        self.attributes_window_title = ETKLabel(self._tk_object, "Fenster-Eigenschaften:", size=vector2d(
            180, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=self.attributes_window.background_color)
        self.attributes_window_title_container.add_element(
            self.attributes_window_title, ETKAlignments.MIDDLE_CENTER)

        # endregion


if __name__ == "__main__":
    g = GUI()
    g.run()
