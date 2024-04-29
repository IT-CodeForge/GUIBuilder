from typing import Any, Final, Optional
from ETK import *
from steuerung import Steuerung


class GUI(ETKMainWindow):
    def __init__(self, steuerung: Steuerung) -> None:
        super().__init__()
        self.__steuerung = steuerung

    LANGUAGES: Final = ["Python (ETK)", "C++ (TGW)"]
    MENUBAR_PADDING: Final = 10
    MENUBAR_HEIGHT: Final = 40
    MENUBAR_ELEMENT_HEIGHT: Final = 20
    ATTRIBUTES_WIDTH: Final = 300
    ATTRIBUTES_ELEMENT_HEIGHT: Final = 20

    def _add_elements(self):
        self.add_event(ETKBaseEvents.MOUSE_UP, self.__mouse_up_event_handler)
        self.add_event(ETKBaseEvents.MOUSE_MOVED,
                       self.__mouse_moved_event_handler)
        self.__moving_element: Optional[ETKBaseObject] = None

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
        self.menubar_inner.add_element(
            self.menubar_right, ETKAlignments.TOP_RIGHT)

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

        self.element_area = ETKContainer(
            self._tk_object, size=ETKContainerSize(500, 500), background_color=0xFFFFFF)
        self.main2.add_element(self.element_area)

        # region Menubar_left Elemente

        self.menubar_button = ETKButton(
            self._tk_object, "BUTTON", size=vector2d(50, self.MENUBAR_ELEMENT_HEIGHT))
        self.menubar_button.enabled = False
        self.menubar_button.add_event(
            ETKBaseEvents.MOUSE_DOWN, self.__menubar_left_handler)
        self.menubar_left.add_element(self.menubar_button)

        self.menubar_label = ETKLabel(
            self._tk_object, "LABEL", size=vector2d(50, self.MENUBAR_ELEMENT_HEIGHT))
        self.menubar_label.add_event(
            ETKBaseEvents.MOUSE_DOWN, self.__menubar_left_handler)
        self.menubar_left.add_element(self.menubar_label)

        self.menubar_edit = ETKLabel(
            self._tk_object, "EDIT", size=vector2d(50, self.MENUBAR_ELEMENT_HEIGHT))
        self.menubar_edit.add_event(
            ETKBaseEvents.MOUSE_DOWN, self.__menubar_left_handler)
        self.menubar_left.add_element(self.menubar_edit)

        self.menubar_checkbox = ETKCheckbox(
            self._tk_object, "CHECKBOX", size=vector2d(100, self.MENUBAR_ELEMENT_HEIGHT))
        self.menubar_checkbox.enabled = False
        self.menubar_checkbox.add_event(
            ETKBaseEvents.MOUSE_DOWN, self.__menubar_left_handler)
        self.menubar_left.add_element(self.menubar_checkbox)

        self.menubar_canvas = ETKLabel(
            self._tk_object, "CANVAS", size=vector2d(70, self.MENUBAR_ELEMENT_HEIGHT))
        self.menubar_canvas.add_event(
            ETKBaseEvents.MOUSE_DOWN, self.__menubar_left_handler)
        self.menubar_left.add_element(self.menubar_canvas)

        self.menubar_timer = ETKLabel(
            self._tk_object, "TIMER", size=vector2d(50, self.MENUBAR_ELEMENT_HEIGHT))
        self.menubar_timer.add_event(
            ETKBaseEvents.MOUSE_DOWN, self.__menubar_left_handler)
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

        self.language_selector = ETKDropdownMenu(
            self._tk_object, self.LANGUAGES, self.LANGUAGES[0], size=vector2d(130, self.MENUBAR_ELEMENT_HEIGHT))
        self.menubar_right.add_element(self.language_selector)

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

        # region attributes_window Elemente

        self.attributes_window_title_container = ETKContainer(self._tk_object, size=ETKContainerSize(
            self.attributes_window.size.x-4, self.ATTRIBUTES_ELEMENT_HEIGHT))
        self.attributes_window.add_element(
            self.attributes_window_title_container)

        self.attributes_window_title = ETKLabel(self._tk_object, "Fenster-Eigenschaften:", size=vector2d(
            180, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=self.attributes_window.background_color)
        self.attributes_window_title_container.add_element(
            self.attributes_window_title, ETKAlignments.MIDDLE_CENTER)

        # endregion

    def __mouse_up_event_handler(self):
        if self.__moving_element != None:
            self.__moving_element = None

    def __mouse_moved_event_handler(self, event: tuple[ETKBaseObject, ETKEvents, Any]):
        mouse_pos = vector2d(event[2].x_root, event[2].y_root) - self.abs_pos
        if self.__moving_element != None:
            element_pos = mouse_pos - self.__moving_element_rel_click_pos
            rel_mouse_pos = element_pos - self.element_area.abs_pos
            if rel_mouse_pos.x < 0:
                rel_mouse_pos.x = 0
            if rel_mouse_pos.y < 0:
                rel_mouse_pos.y = 0
            rel_max_pos = rel_mouse_pos + self.__moving_element.size
            if rel_max_pos.x > self.element_area.size.x:
                rel_mouse_pos.x = self.element_area.size.x - self.__moving_element.size.x
            if rel_max_pos.y > self.element_area.size.y:
                rel_mouse_pos.y = self.element_area.size.y - self.__moving_element.size.y
            self.__moving_element.pos = rel_mouse_pos

    def __element_mouse_down_handler(self, event_data: tuple[ETKBaseObject, ETKEvents, Any]):
        self.__start_moving_element(
            event_data[0], vector2d(event_data[2].x, event_data[2].y))

    def __menubar_left_handler(self, event_data: tuple[ETKBaseObject, ETKEvents, Any]):
        match event_data[0]:
            case self.menubar_button:
                new_element = ETKButton(self._tk_object)
                new_element.enabled = False
            case self.menubar_label:
                new_element = ETKLabel(self._tk_object)
            case self.menubar_edit:
                new_element = ETKLabel(self._tk_object)
            case self.menubar_checkbox:
                new_element = ETKCheckbox(self._tk_object)
                new_element.enabled = False
            case self.menubar_canvas:
                new_element = ETKLabel(self._tk_object)
            case self.menubar_timer:
                new_element = ETKLabel(self._tk_object)
            case _:
                return

        new_element.add_event(ETKBaseEvents.MOUSE_DOWN,
                              self.__element_mouse_down_handler)
        self.element_area.add_element(new_element)
        self.__start_moving_element(new_element)

    def __start_moving_element(self, element: ETKBaseObject, rel_click_pos: vector2d = vector2d()):
        self.__moving_element = element
        self.__moving_element_rel_click_pos = rel_click_pos
