from sys import executable
from typing import Final, Optional, Type
from ETK import *
from steuerung import Steuerung
from main import version
# TODO: fix licence box height


class GUI(ETKMainWindow):
    def __init__(self, steuerung: Steuerung) -> None:
        self.__steuerung = steuerung
        self.__mouse_pos = Vector2d()

        import ctypes
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        scale_factor = min((screensize[0] / 1920, screensize[1] / 1017))

        super().__init__(caption=f"GUI-Builder V{version}", size=Vector2d(1920, 1017), scale_factor=scale_factor)

    LANGUAGES: Final = ["C++ (TGW)", "Python (ETK)"]
    MENUBAR_PADDING: Final = 10
    MENUBAR_HEIGHT: Final = 40
    MENUBAR_ELEMENT_HEIGHT: Final = 20
    ATTRIBUTES_WIDTH: Final = 360
    ATTRIBUTES_ELEMENT_HEIGHT: Final = 20
    CC_NOTICE_HEIGHT: Final = 35

    def _add_elements(self):
        self._tk_object.iconbitmap(executable)  # type:ignore

        self.__moving_element = None

        self.add_event(ETKWindowEvents.EXIT, self.__steuerung.exit_event)

        self.add_event(ETKWindowEvents.MOUSE_UP, self.__mouse_up_event_handler)
        self.add_event(ETKWindowEvents.MOUSE_MOVED, self.__mouse_moved_event_handler)
        self.__moving_element: Optional[ETKBaseObject] = None
        self.active_attributes_element: Optional[ETKBaseObject] = None
        self.last_active_attributes_element: Optional[ETKBaseObject] = None

        self.main = ETKListingContainer(self._main, size=ETKContainerSize.from_vector2d(
            self.size), offset=0)

        self.menubar_outer = ETKContainer(self._main, size=ETKContainerSize(
            self.main.size.x, self.MENUBAR_HEIGHT))
        self.main.add_element(self.menubar_outer)

        self.attributes_text = ETKLabel(self._main, text="ROT hinterlegte Attribute sind in der\nausgewählten Sprache nicht verfügbar!", size=Vector2d(500, self.ATTRIBUTES_ELEMENT_HEIGHT*2), background_color=self.menubar_outer.background_color, text_color=0xFF0000)
        self.menubar_outer.add_element(self.attributes_text)

        self.menubar_inner = ETKContainer(self._main, Vector2d(self.ATTRIBUTES_WIDTH, 0), size=ETKContainerSize(
            self.menubar_outer.size.x - self.ATTRIBUTES_WIDTH, self.MENUBAR_HEIGHT), outline_thickness=2)
        self.menubar_outer.add_element(self.menubar_inner)

        self.menubar_left = ETKListingContainer(self._main, Vector2d(0, 0), ETKContainerSize(0, self.MENUBAR_HEIGHT, True, False, self.MENUBAR_PADDING, self.MENUBAR_PADDING), listing_type=ETKListingTypes.LEFT_TO_RIGHT, alignment=ETKAlignments.MIDDLE_CENTER, offset=self.MENUBAR_PADDING, outline_thickness=2)
        self.menubar_inner.add_element(self.menubar_left)

        self.menubar_right = ETKListingContainer(self._main, Vector2d(0, 0), ETKContainerSize(0, self.MENUBAR_HEIGHT, True, False, self.MENUBAR_PADDING, self.MENUBAR_PADDING), listing_type=ETKListingTypes.RIGHT_TO_LEFT, alignment=ETKAlignments.MIDDLE_CENTER, offset=self.MENUBAR_PADDING, outline_thickness=2)
        self.menubar_inner.add_element(
            self.menubar_right, ETKAlignments.TOP_RIGHT)

        self.main2 = ETKListingContainer(self._main, size=ETKContainerSize(
            self.size.x, self.size.y-self.menubar_outer.size.y), listing_type=ETKListingTypes.LEFT_TO_RIGHT, offset=0)
        self.main.add_element(self.main2)

        self.attributes = ETKListingContainer(self._main, size=ETKContainerSize(
            self.ATTRIBUTES_WIDTH, self.main2.size.y), offset=0)
        self.main2.add_element(self.attributes)

        self.attributes_element = ETKListingContainer(self._main, size=ETKContainerSize(
            self.attributes.size.x, self.attributes.size.y/2, paddings_x_l=2, paddings_x_r=2, paddings_y_o=2, paddings_y_u=2), outline_thickness=2, offset=3)
        self.attributes.add_element(self.attributes_element)

        self.attributes_window = ETKListingContainer(self._main, size=ETKContainerSize(
            self.attributes.size.x, self.attributes.size.y/2 - self.CC_NOTICE_HEIGHT, paddings_x_l=2, paddings_x_r=2, paddings_y_o=0, paddings_y_u=2), outline_thickness=2, offset=3)
        self.attributes.add_element(self.attributes_window)

        self.cc_notice = ETKLabel(self._main, text="\u00A9 2024 Johannes Kerger, Louis Sailer\r\nLicense: MIT-License", background_color=self.attributes.background_color, size=Vector2d(self.attributes.size.x, self.CC_NOTICE_HEIGHT))
        self.cc_notice.outline_thickness = 2
        self.attributes.add_element(self.cc_notice)

        self.element_area = ETKContainer(
            self._main, size=ETKContainerSize(500, 500), outline_thickness=2)
        self.main2.add_element(self.element_area)
        self.element_area.add_event(ETKContainerEvents.MOUSE_DOWN, self.__element_area_mousedown_handler)

        # region Menubar_left Elemente

        self.menubar_button = ETKButton(
            self._main, text="BUTTON", size=Vector2d(50, self.MENUBAR_ELEMENT_HEIGHT))
        self.menubar_button.enabled = False
        self.menubar_button.add_event(
            ETKButtonEvents.MOUSE_DOWN, self.__menubar_left_handler)
        self.menubar_left.add_element(self.menubar_button)

        self.menubar_label = ETKLabel(
            self._main, text="LABEL", size=Vector2d(50, self.MENUBAR_ELEMENT_HEIGHT))
        self.menubar_label.add_event(
            ETKLabelEvents.MOUSE_DOWN, self.__menubar_left_handler)
        self.menubar_left.add_element(self.menubar_label)

        self.menubar_edit = ETKLabel(
            self._main, text="EDIT", size=Vector2d(50, self.MENUBAR_ELEMENT_HEIGHT))
        self.menubar_edit.add_event(
            ETKLabelEvents.MOUSE_DOWN, self.__menubar_left_handler)
        self.menubar_left.add_element(self.menubar_edit)

        self.menubar_checkbox = ETKCheckbox(
            self._main, text="CHECKBOX", size=Vector2d(100, self.MENUBAR_ELEMENT_HEIGHT))
        self.menubar_checkbox.enabled = False
        self.menubar_checkbox.add_event(
            ETKCheckboxEvents.MOUSE_DOWN, self.__menubar_left_handler)
        self.menubar_left.add_element(self.menubar_checkbox)

        self.menubar_canvas = ETKLabel(
            self._main, text="CANVAS", size=Vector2d(70, self.MENUBAR_ELEMENT_HEIGHT))
        self.menubar_canvas.add_event(
            ETKLabelEvents.MOUSE_DOWN, self.__menubar_left_handler)
        self.menubar_left.add_element(self.menubar_canvas)

        self.menubar_timer = ETKLabel(
            self._main, text="TIMER", size=Vector2d(50, self.MENUBAR_ELEMENT_HEIGHT))
        self.menubar_timer.add_event(
            ETKLabelEvents.MOUSE_DOWN, self.__menubar_left_handler)
        self.menubar_left.add_element(self.menubar_timer)

        # endregion
        # region Menubar_right Elemente

        self.menubar_export = ETKButton(
            self._main, text="Export", size=Vector2d(50, self.MENUBAR_ELEMENT_HEIGHT))
        self.menubar_export.add_event(
            ETKButtonEvents.PRESSED, lambda: None)
        self.menubar_right.add_element(self.menubar_export)
        self.menubar_export.add_event(ETKButtonEvents.PRESSED, self.__steuerung.export)

        self.menubar_save = ETKButton(
            self._main, text="Save", size=Vector2d(50, self.MENUBAR_ELEMENT_HEIGHT))
        self.menubar_save.add_event(
            ETKButtonEvents.PRESSED, lambda: None)
        self.menubar_right.add_element(self.menubar_save)
        self.menubar_save.add_event(ETKButtonEvents.PRESSED, self.__steuerung.save_elements_to_file)

        self.menubar_load = ETKButton(
            self._main, text="Load", size=Vector2d(50, self.MENUBAR_ELEMENT_HEIGHT))
        self.menubar_load.add_event(
            ETKButtonEvents.PRESSED, lambda: None)
        self.menubar_right.add_element(self.menubar_load)
        self.menubar_load.add_event(ETKButtonEvents.PRESSED, self.__steuerung.load_elements_from_file)

        self.language_selector = ETKDropdownMenu(
            self._main, options=self.LANGUAGES, start_value=self.LANGUAGES[0], size=Vector2d(130, self.MENUBAR_ELEMENT_HEIGHT))
        self.menubar_right.add_element(self.language_selector)
        self.language_selector.add_event(ETKDropdownMenuEvents.CHANGED, self.__steuerung.change_language_event)

        # endregion
        # region attributes_element Elemente

        self.attributes_element_title_container = ETKContainer(self._main, size=ETKContainerSize(
            self.attributes_element.size.x-4, self.ATTRIBUTES_ELEMENT_HEIGHT))
        self.attributes_element.add_element(
            self.attributes_element_title_container)

        self.attributes_element_title = ETKLabel(self._main, text="Element-Eigenschaften:", size=Vector2d(
            180, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=self.attributes_element.background_color)
        self.attributes_element_title_container.add_element(
            self.attributes_element_title, ETKAlignments.MIDDLE_CENTER)

        self.attributes_element_inner = ETKListingContainer(self._main, size=ETKContainerSize(
            0, 0, True, True), offset=3)
        self.attributes_element.add_element(self.attributes_element_inner)
        self.attributes_element_inner.visibility = False

        self.attributes_element_delete = ETKButton(self._main, text="Delete", size=Vector2d(50, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=0xFF0000, text_color=0xFFFFFF)
        self.attributes_element_inner.add_element(self.attributes_element_delete)
        self.attributes_element_delete.add_event(ETKButtonEvents.PRESSED, self.__delete_element_event)

        self.attributes_element_id_container = ETKListingContainer(self._main, size=ETKContainerSize(0, 0, True, True), listing_type=ETKListingTypes.LEFT_TO_RIGHT, offset=0)
        self.attributes_element_id_const = ETKLabel(self._main, text="ID: ", size=Vector2d(30, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=self.attributes_element.background_color)
        self.attributes_element_id_container.add_element(self.attributes_element_id_const)
        self.attributes_element_id_var = ETKLabel(self._main, text="-", background_color=self.attributes_element.background_color)
        self.attributes_element_id_container.add_element(self.attributes_element_id_var)
        self.attributes_element_inner.add_element(self.attributes_element_id_container)

        self.attributes_element_name_container = ETKListingContainer(self._main, size=ETKContainerSize(0, 0, True, True), listing_type=ETKListingTypes.LEFT_TO_RIGHT, offset=3)
        self.attributes_element_name_const = ETKLabel(self._main, text="Name: ", size=Vector2d(45, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=self.attributes_element.background_color)
        self.attributes_element_name_container.add_element(self.attributes_element_name_const)
        self.attributes_element_name_var = ETKEdit(self._main, text="-", size=Vector2d(200, self.ATTRIBUTES_ELEMENT_HEIGHT))
        self.attributes_element_name_container.add_element(self.attributes_element_name_var)
        self.attributes_element_inner.add_element(self.attributes_element_name_container)
        self.attributes_element_name_var.add_event(ETKEditEvents.CHANGED_DELAYED, self.__element_attribut_changed_handler)

        self.attributes_element_text_container = ETKListingContainer(self._main, size=ETKContainerSize(0, 0, True, True), listing_type=ETKListingTypes.LEFT_TO_RIGHT, offset=3)
        self.attributes_element_text_const = ETKLabel(self._main, text="Text: ", size=Vector2d(45, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=self.attributes_element.background_color)
        self.attributes_element_text_container.add_element(self.attributes_element_text_const)
        self.attributes_element_text_var = ETKEdit(self._main, text="-", size=Vector2d(200, self.ATTRIBUTES_ELEMENT_HEIGHT))
        self.attributes_element_text_container.add_element(self.attributes_element_text_var)
        self.attributes_element_inner.add_element(self.attributes_element_text_container)
        self.attributes_element_text_var.add_event(ETKEditEvents.CHANGED_DELAYED, self.__element_attribut_changed_handler)

        self.attributes_element_pos_container = ETKListingContainer(self._main, size=ETKContainerSize(0, 0, True, True), listing_type=ETKListingTypes.LEFT_TO_RIGHT, offset=3)
        self.attributes_element_pos_const = ETKLabel(self._main, text="Pos: ", size=Vector2d(45, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=self.attributes_element.background_color)
        self.attributes_element_pos_container.add_element(self.attributes_element_pos_const)
        self.attributes_element_pos_var_x = ETKEdit(self._main, text="-", size=Vector2d(70, self.ATTRIBUTES_ELEMENT_HEIGHT))
        self.attributes_element_pos_container.add_element(self.attributes_element_pos_var_x)
        self.attributes_element_pos_var_y = ETKEdit(self._main, text="-", size=Vector2d(70, self.ATTRIBUTES_ELEMENT_HEIGHT))
        self.attributes_element_pos_container.add_element(self.attributes_element_pos_var_y)
        self.attributes_element_inner.add_element(self.attributes_element_pos_container)
        self.attributes_element_pos_var_x.add_event(ETKEditEvents.CHANGED_DELAYED, self.__element_attribut_changed_handler)
        self.attributes_element_pos_var_y.add_event(ETKEditEvents.CHANGED_DELAYED, self.__element_attribut_changed_handler)

        self.attributes_element_size_container = ETKListingContainer(self._main, size=ETKContainerSize(0, 0, True, True), listing_type=ETKListingTypes.LEFT_TO_RIGHT, offset=3)
        self.attributes_element_size_const = ETKLabel(self._main, text="Size: ", size=Vector2d(45, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=self.attributes_element.background_color)
        self.attributes_element_size_container.add_element(self.attributes_element_size_const)
        self.attributes_element_size_var_x = ETKEdit(self._main, text="-", size=Vector2d(70, self.ATTRIBUTES_ELEMENT_HEIGHT))
        self.attributes_element_size_container.add_element(self.attributes_element_size_var_x)
        self.attributes_element_size_var_y = ETKEdit(self._main, text="-", size=Vector2d(70, self.ATTRIBUTES_ELEMENT_HEIGHT))
        self.attributes_element_size_container.add_element(self.attributes_element_size_var_y)
        self.attributes_element_inner.add_element(self.attributes_element_size_container)
        self.attributes_element_size_var_x.add_event(ETKEditEvents.CHANGED_DELAYED, self.__element_attribut_changed_handler)
        self.attributes_element_size_var_y.add_event(ETKEditEvents.CHANGED_DELAYED, self.__element_attribut_changed_handler)

        self.attributes_element_text_color_container = ETKListingContainer(self._main, size=ETKContainerSize(0, 0, True, True), listing_type=ETKListingTypes.LEFT_TO_RIGHT, offset=3)
        self.attributes_element_text_color_const = ETKLabel(self._main, text="Text-Color (RGB 24bit): ", size=Vector2d(190, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=self.attributes_element.background_color)
        self.attributes_element_text_color_container.add_element(self.attributes_element_text_color_const)
        self.attributes_element_text_color_var_r = ETKEdit(self._main, text="-", size=Vector2d(50, self.ATTRIBUTES_ELEMENT_HEIGHT))
        self.attributes_element_text_color_container.add_element(self.attributes_element_text_color_var_r)
        self.attributes_element_text_color_var_g = ETKEdit(self._main, text="-", size=Vector2d(50, self.ATTRIBUTES_ELEMENT_HEIGHT))
        self.attributes_element_text_color_container.add_element(self.attributes_element_text_color_var_g)
        self.attributes_element_text_color_var_b = ETKEdit(self._main, text="-", size=Vector2d(50, self.ATTRIBUTES_ELEMENT_HEIGHT))
        self.attributes_element_text_color_container.add_element(self.attributes_element_text_color_var_b)
        self.attributes_element_inner.add_element(self.attributes_element_text_color_container)
        self.attributes_element_text_color_var_r.add_event(ETKEditEvents.CHANGED_DELAYED, self.__element_attribut_changed_handler)
        self.attributes_element_text_color_var_g.add_event(ETKEditEvents.CHANGED_DELAYED, self.__element_attribut_changed_handler)
        self.attributes_element_text_color_var_b.add_event(ETKEditEvents.CHANGED_DELAYED, self.__element_attribut_changed_handler)

        self.attributes_element_background_color_container = ETKListingContainer(self._main, size=ETKContainerSize(0, 0, True, True), listing_type=ETKListingTypes.LEFT_TO_RIGHT, offset=3)
        self.attributes_element_background_color_const = ETKLabel(self._main, text="BG-Color (RGB 24bit): ", size=Vector2d(190, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=self.attributes_element.background_color)
        self.attributes_element_background_color_container.add_element(self.attributes_element_background_color_const)
        self.attributes_element_background_color_var_r = ETKEdit(self._main, text="-", size=Vector2d(50, self.ATTRIBUTES_ELEMENT_HEIGHT))
        self.attributes_element_background_color_container.add_element(self.attributes_element_background_color_var_r)
        self.attributes_element_background_color_var_g = ETKEdit(self._main, text="-", size=Vector2d(50, self.ATTRIBUTES_ELEMENT_HEIGHT))
        self.attributes_element_background_color_container.add_element(self.attributes_element_background_color_var_g)
        self.attributes_element_background_color_var_b = ETKEdit(self._main, text="-", size=Vector2d(50, self.ATTRIBUTES_ELEMENT_HEIGHT))
        self.attributes_element_background_color_container.add_element(self.attributes_element_background_color_var_b)
        self.attributes_element_inner.add_element(self.attributes_element_background_color_container)
        self.attributes_element_background_color_var_r.add_event(ETKEditEvents.CHANGED_DELAYED, self.__element_attribut_changed_handler)
        self.attributes_element_background_color_var_g.add_event(ETKEditEvents.CHANGED_DELAYED, self.__element_attribut_changed_handler)
        self.attributes_element_background_color_var_b.add_event(ETKEditEvents.CHANGED_DELAYED, self.__element_attribut_changed_handler)

        self.attributes_element_interval_container = ETKListingContainer(self._main, size=ETKContainerSize(0, 0, True, True), listing_type=ETKListingTypes.LEFT_TO_RIGHT, offset=3)
        self.attributes_element_interval_const = ETKLabel(self._main, text="Interval: ", size=Vector2d(75, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=self.attributes_element.background_color)
        self.attributes_element_interval_container.add_element(self.attributes_element_interval_const)
        self.attributes_element_interval_var = ETKEdit(self._main, text="-", size=Vector2d(50, self.ATTRIBUTES_ELEMENT_HEIGHT))
        self.attributes_element_interval_container.add_element(self.attributes_element_interval_var)
        self.attributes_element_inner.add_element(self.attributes_element_interval_container)
        self.attributes_element_interval_var.add_event(ETKEditEvents.CHANGED_DELAYED, self.__element_attribut_changed_handler)

        self.attributes_element_enabled_container = ETKListingContainer(self._main, size=ETKContainerSize(0, 0, True, True), listing_type=ETKListingTypes.LEFT_TO_RIGHT, offset=3)
        self.attributes_element_enabled_const = ETKLabel(self._main, text="Enabled: ", size=Vector2d(67, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=self.attributes_element.background_color)
        self.attributes_element_enabled_container.add_element(self.attributes_element_enabled_const)
        self.attributes_element_enabled_var = ETKCheckbox(self._main, text="", size=Vector2d(17, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=self.attributes_element.background_color)
        self.attributes_element_enabled_container.add_element(self.attributes_element_enabled_var)
        self.attributes_element_inner.add_element(self.attributes_element_enabled_container)
        self.attributes_element_enabled_var.add_event(ETKCheckboxEvents.TOGGLED, self.__element_attribut_changed_handler)

        self.attributes_element_checked_container = ETKListingContainer(self._main, size=ETKContainerSize(0, 0, True, True), listing_type=ETKListingTypes.LEFT_TO_RIGHT, offset=3)
        self.attributes_element_checked_const = ETKLabel(self._main, text="Checked: ", size=Vector2d(67, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=self.attributes_element.background_color)
        self.attributes_element_checked_container.add_element(self.attributes_element_checked_const)
        self.attributes_element_checked_var = ETKCheckbox(self._main, text="", size=Vector2d(17, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=self.attributes_element.background_color)
        self.attributes_element_checked_container.add_element(self.attributes_element_checked_var)
        self.attributes_element_inner.add_element(self.attributes_element_checked_container)
        self.attributes_element_checked_var.add_event(ETKCheckboxEvents.TOGGLED, self.__element_attribut_changed_handler)

        self.attributes_element_multiple_lines_container = ETKListingContainer(self._main, size=ETKContainerSize(0, 0, True, True), listing_type=ETKListingTypes.LEFT_TO_RIGHT, offset=3)
        self.attributes_element_multiple_lines_const = ETKLabel(self._main, text="Multiline: ", size=Vector2d(83, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=self.attributes_element.background_color)
        self.attributes_element_multiple_lines_container.add_element(self.attributes_element_multiple_lines_const)
        self.attributes_element_multiple_lines_var = ETKCheckbox(self._main, text="", size=Vector2d(17, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=self.attributes_element.background_color)
        self.attributes_element_multiple_lines_container.add_element(self.attributes_element_multiple_lines_var)
        self.attributes_element_inner.add_element(self.attributes_element_multiple_lines_container)
        self.attributes_element_multiple_lines_var.add_event(ETKCheckboxEvents.TOGGLED, self.__element_attribut_changed_handler)

        self.attributes_element_spacing_container = ETKListingContainer(self._main, size=ETKContainerSize(0, 30, True, False), listing_type=ETKListingTypes.LEFT_TO_RIGHT, offset=3)
        self.attributes_element_inner.add_element(self.attributes_element_spacing_container)

        self.attributes_element_event_title = ETKLabel(self._main, text="Events:", size=Vector2d(
            180, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=self.attributes_element.background_color)
        self.attributes_element_inner.add_element(self.attributes_element_event_title)

        self.attributes_element_event_pressed_container = ETKListingContainer(self._main, size=ETKContainerSize(0, 0, True, True), listing_type=ETKListingTypes.LEFT_TO_RIGHT, offset=3)
        self.attributes_element_event_pressed_const = ETKLabel(self._main, text="Event pressed: ", size=Vector2d(120, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=self.attributes_element.background_color)
        self.attributes_element_event_pressed_container.add_element(self.attributes_element_event_pressed_const)
        self.attributes_element_event_pressed_var = ETKCheckbox(self._main, text="", size=Vector2d(17, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=self.attributes_element.background_color)
        self.attributes_element_event_pressed_container.add_element(self.attributes_element_event_pressed_var)
        self.attributes_element_inner.add_element(self.attributes_element_event_pressed_container)
        self.attributes_element_event_pressed_var.add_event(ETKCheckboxEvents.TOGGLED, self.__element_attribut_changed_handler)

        self.attributes_element_event_double_pressed_container = ETKListingContainer(self._main, size=ETKContainerSize(0, 0, True, True), listing_type=ETKListingTypes.LEFT_TO_RIGHT, offset=3)
        self.attributes_element_event_double_pressed_const = ETKLabel(self._main, text="Event double pressed: ", size=Vector2d(170, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=self.attributes_element.background_color)
        self.attributes_element_event_double_pressed_container.add_element(self.attributes_element_event_double_pressed_const)
        self.attributes_element_event_double_pressed_var = ETKCheckbox(self._main, text="", size=Vector2d(17, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=self.attributes_element.background_color)
        self.attributes_element_event_double_pressed_container.add_element(self.attributes_element_event_double_pressed_var)
        self.attributes_element_inner.add_element(self.attributes_element_event_double_pressed_container)
        self.attributes_element_event_double_pressed_var.add_event(ETKCheckboxEvents.TOGGLED, self.__element_attribut_changed_handler)

        self.attributes_element_event_changed_container = ETKListingContainer(self._main, size=ETKContainerSize(0, 0, True, True), listing_type=ETKListingTypes.LEFT_TO_RIGHT, offset=3)
        self.attributes_element_event_changed_const = ETKLabel(self._main, text="Event changed: ", size=Vector2d(120, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=self.attributes_element.background_color)
        self.attributes_element_event_changed_container.add_element(self.attributes_element_event_changed_const)
        self.attributes_element_event_changed_var = ETKCheckbox(self._main, text="", size=Vector2d(17, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=self.attributes_element.background_color)
        self.attributes_element_event_changed_container.add_element(self.attributes_element_event_changed_var)
        self.attributes_element_inner.add_element(self.attributes_element_event_changed_container)
        self.attributes_element_event_changed_var.add_event(ETKCheckboxEvents.TOGGLED, self.__element_attribut_changed_handler)

        self.attributes_element_event_hovered_container = ETKListingContainer(self._main, size=ETKContainerSize(0, 0, True, True), listing_type=ETKListingTypes.LEFT_TO_RIGHT, offset=3)
        self.attributes_element_event_hovered_const = ETKLabel(self._main, text="Event hovered: ", size=Vector2d(120, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=self.attributes_element.background_color)
        self.attributes_element_event_hovered_container.add_element(self.attributes_element_event_hovered_const)
        self.attributes_element_event_hovered_var = ETKCheckbox(self._main, text="", size=Vector2d(17, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=self.attributes_element.background_color)
        self.attributes_element_event_hovered_container.add_element(self.attributes_element_event_hovered_var)
        self.attributes_element_inner.add_element(self.attributes_element_event_hovered_container)
        self.attributes_element_event_hovered_var.add_event(ETKCheckboxEvents.TOGGLED, self.__element_attribut_changed_handler)

        # endregion
        # region attributes_window Elemente

        self.attributes_window_title_container = ETKContainer(self._main, size=ETKContainerSize(
            self.attributes_window.size.x-4, self.ATTRIBUTES_ELEMENT_HEIGHT))
        self.attributes_window.add_element(
            self.attributes_window_title_container)

        self.attributes_window_title = ETKLabel(self._main, text="Fenster-Eigenschaften:", size=Vector2d(
            180, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=self.attributes_window.background_color)
        self.attributes_window_title_container.add_element(
            self.attributes_window_title, ETKAlignments.MIDDLE_CENTER)

        self.attributes_window_id_container = ETKListingContainer(self._main, size=ETKContainerSize(0, 0, True, True), listing_type=ETKListingTypes.LEFT_TO_RIGHT, offset=0)
        self.attributes_window_id_const = ETKLabel(self._main, text="ID: ", size=Vector2d(30, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=self.attributes_window.background_color)
        self.attributes_window_id_container.add_element(self.attributes_window_id_const)
        self.attributes_window_id_var = ETKLabel(self._main, text="-", background_color=self.attributes_window.background_color)
        self.attributes_window_id_container.add_element(self.attributes_window_id_var)
        self.attributes_window.add_element(self.attributes_window_id_container)

        self.attributes_window_name_container = ETKListingContainer(self._main, size=ETKContainerSize(0, 0, True, True), listing_type=ETKListingTypes.LEFT_TO_RIGHT, offset=3)
        self.attributes_window_name_const = ETKLabel(self._main, text="Name: ", size=Vector2d(45, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=self.attributes_window.background_color)
        self.attributes_window_name_container.add_element(self.attributes_window_name_const)
        self.attributes_window_name_var = ETKEdit(self._main, text="-", size=Vector2d(200, self.ATTRIBUTES_ELEMENT_HEIGHT))
        self.attributes_window_name_container.add_element(self.attributes_window_name_var)
        self.attributes_window.add_element(self.attributes_window_name_container)
        self.attributes_window_name_var.add_event(ETKEditEvents.CHANGED_DELAYED, self.__window_attribut_changed_handler)

        self.attributes_window_title_container = ETKListingContainer(self._main, size=ETKContainerSize(0, 0, True, True), listing_type=ETKListingTypes.LEFT_TO_RIGHT, offset=3)
        self.attributes_window_title_const = ETKLabel(self._main, text="Titel: ", size=Vector2d(45, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=self.attributes_window.background_color)
        self.attributes_window_title_container.add_element(self.attributes_window_title_const)
        self.attributes_window_title_var = ETKEdit(self._main, text="-", size=Vector2d(200, self.ATTRIBUTES_ELEMENT_HEIGHT))
        self.attributes_window_title_container.add_element(self.attributes_window_title_var)
        self.attributes_window.add_element(self.attributes_window_title_container)
        self.attributes_window_title_var.add_event(ETKEditEvents.CHANGED_DELAYED, self.__window_attribut_changed_handler)

        self.attributes_window_size_container = ETKListingContainer(self._main, size=ETKContainerSize(0, 0, True, True), listing_type=ETKListingTypes.LEFT_TO_RIGHT, offset=3)
        self.attributes_window_size_const = ETKLabel(self._main, text="Size: ", size=Vector2d(45, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=self.attributes_window.background_color)
        self.attributes_window_size_container.add_element(self.attributes_window_size_const)
        self.attributes_window_size_var_x = ETKEdit(self._main, text="-", size=Vector2d(70, self.ATTRIBUTES_ELEMENT_HEIGHT))
        self.attributes_window_size_container.add_element(self.attributes_window_size_var_x)
        self.attributes_window_size_var_y = ETKEdit(self._main, text="-", size=Vector2d(70, self.ATTRIBUTES_ELEMENT_HEIGHT))
        self.attributes_window_size_container.add_element(self.attributes_window_size_var_y)
        self.attributes_window.add_element(self.attributes_window_size_container)
        self.attributes_window_size_var_x.add_event(ETKEditEvents.CHANGED_DELAYED, self.__window_attribut_changed_handler)
        self.attributes_window_size_var_y.add_event(ETKEditEvents.CHANGED_DELAYED, self.__window_attribut_changed_handler)

        self.attributes_window_title_color_container = ETKListingContainer(self._main, size=ETKContainerSize(0, 0, True, True), listing_type=ETKListingTypes.LEFT_TO_RIGHT, offset=3)
        self.attributes_window_title_color_const = ETKLabel(self._main, text="Title-Color (RGB 24bit): ", size=Vector2d(195, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=self.attributes_window.background_color)
        self.attributes_window_title_color_container.add_element(self.attributes_window_title_color_const)
        self.attributes_window_title_color_var_r = ETKEdit(self._main, text="-", size=Vector2d(50, self.ATTRIBUTES_ELEMENT_HEIGHT))
        self.attributes_window_title_color_container.add_element(self.attributes_window_title_color_var_r)
        self.attributes_window_title_color_var_g = ETKEdit(self._main, text="-", size=Vector2d(50, self.ATTRIBUTES_ELEMENT_HEIGHT))
        self.attributes_window_title_color_container.add_element(self.attributes_window_title_color_var_g)
        self.attributes_window_title_color_var_b = ETKEdit(self._main, text="-", size=Vector2d(50, self.ATTRIBUTES_ELEMENT_HEIGHT))
        self.attributes_window_title_color_container.add_element(self.attributes_window_title_color_var_b)
        self.attributes_window.add_element(self.attributes_window_title_color_container)
        self.attributes_window_title_color_var_r.add_event(ETKEditEvents.CHANGED_DELAYED, self.__window_attribut_changed_handler)
        self.attributes_window_title_color_var_g.add_event(ETKEditEvents.CHANGED_DELAYED, self.__window_attribut_changed_handler)
        self.attributes_window_title_color_var_b.add_event(ETKEditEvents.CHANGED_DELAYED, self.__window_attribut_changed_handler)

        self.attributes_window_background_color_container = ETKListingContainer(self._main, size=ETKContainerSize(0, 0, True, True), listing_type=ETKListingTypes.LEFT_TO_RIGHT, offset=3)
        self.attributes_window_background_color_const = ETKLabel(self._main, text="BG-Color (RGB 24bit): ", size=Vector2d(190, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=self.attributes_window.background_color)
        self.attributes_window_background_color_container.add_element(self.attributes_window_background_color_const)
        self.attributes_window_background_color_var_r = ETKEdit(self._main, text="-", size=Vector2d(50, self.ATTRIBUTES_ELEMENT_HEIGHT))
        self.attributes_window_background_color_container.add_element(self.attributes_window_background_color_var_r)
        self.attributes_window_background_color_var_g = ETKEdit(self._main, text="-", size=Vector2d(50, self.ATTRIBUTES_ELEMENT_HEIGHT))
        self.attributes_window_background_color_container.add_element(self.attributes_window_background_color_var_g)
        self.attributes_window_background_color_var_b = ETKEdit(self._main, text="-", size=Vector2d(50, self.ATTRIBUTES_ELEMENT_HEIGHT))
        self.attributes_window_background_color_container.add_element(self.attributes_window_background_color_var_b)
        self.attributes_window.add_element(self.attributes_window_background_color_container)
        self.attributes_window_background_color_var_r.add_event(ETKEditEvents.CHANGED_DELAYED, self.__window_attribut_changed_handler)
        self.attributes_window_background_color_var_g.add_event(ETKEditEvents.CHANGED_DELAYED, self.__window_attribut_changed_handler)
        self.attributes_window_background_color_var_b.add_event(ETKEditEvents.CHANGED_DELAYED, self.__window_attribut_changed_handler)

        self.attributes_window_spacing_container = ETKListingContainer(self._main, size=ETKContainerSize(0, 30, True, False), listing_type=ETKListingTypes.LEFT_TO_RIGHT, offset=3)
        self.attributes_window.add_element(self.attributes_window_spacing_container)

        self.attributes_window_event_title = ETKLabel(self._main, text="Events:", size=Vector2d(
            180, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=self.attributes_window.background_color)
        self.attributes_window.add_element(self.attributes_window_event_title)

        self.attributes_window_event_create_container = ETKListingContainer(self._main, size=ETKContainerSize(0, 0, True, True), listing_type=ETKListingTypes.LEFT_TO_RIGHT, offset=3)
        self.attributes_window_event_create_const = ETKLabel(self._main, text="Event create: ", size=Vector2d(110, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=self.attributes_window.background_color)
        self.attributes_window_event_create_container.add_element(self.attributes_window_event_create_const)
        self.attributes_window_event_create_var = ETKCheckbox(self._main, text="", size=Vector2d(17, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=self.attributes_window.background_color)
        self.attributes_window_event_create_container.add_element(self.attributes_window_event_create_var)
        self.attributes_window.add_element(self.attributes_window_event_create_container)
        self.attributes_window_event_create_var.add_event(ETKCheckboxEvents.TOGGLED, self.__window_attribut_changed_handler)

        self.attributes_window_event_destroy_container = ETKListingContainer(self._main, size=ETKContainerSize(0, 0, True, True), listing_type=ETKListingTypes.LEFT_TO_RIGHT, offset=3)
        self.attributes_window_event_destroy_const = ETKLabel(self._main, text="Event destroy: ", size=Vector2d(115, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=self.attributes_window.background_color)
        self.attributes_window_event_destroy_container.add_element(self.attributes_window_event_destroy_const)
        self.attributes_window_event_destroy_var = ETKCheckbox(self._main, text="", size=Vector2d(17, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=self.attributes_window.background_color)
        self.attributes_window_event_destroy_container.add_element(self.attributes_window_event_destroy_var)
        self.attributes_window.add_element(self.attributes_window_event_destroy_container)
        self.attributes_window_event_destroy_var.add_event(ETKCheckboxEvents.TOGGLED, self.__window_attribut_changed_handler)

        self.attributes_window_event_paint_container = ETKListingContainer(self._main, size=ETKContainerSize(0, 0, True, True), listing_type=ETKListingTypes.LEFT_TO_RIGHT, offset=3)
        self.attributes_window_event_paint_const = ETKLabel(self._main, text="Event paint: ", size=Vector2d(100, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=self.attributes_window.background_color)
        self.attributes_window_event_paint_container.add_element(self.attributes_window_event_paint_const)
        self.attributes_window_event_paint_var = ETKCheckbox(self._main, text="", size=Vector2d(17, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=self.attributes_window.background_color)
        self.attributes_window_event_paint_container.add_element(self.attributes_window_event_paint_var)
        self.attributes_window.add_element(self.attributes_window_event_paint_container)
        self.attributes_window_event_paint_var.add_event(ETKCheckboxEvents.TOGGLED, self.__window_attribut_changed_handler)

        self.attributes_window_event_resize_container = ETKListingContainer(self._main, size=ETKContainerSize(0, 0, True, True), listing_type=ETKListingTypes.LEFT_TO_RIGHT, offset=3)
        self.attributes_window_event_resize_const = ETKLabel(self._main, text="Event resize: ", size=Vector2d(110, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=self.attributes_window.background_color)
        self.attributes_window_event_resize_container.add_element(self.attributes_window_event_resize_const)
        self.attributes_window_event_resize_var = ETKCheckbox(self._main, text="", size=Vector2d(17, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=self.attributes_window.background_color)
        self.attributes_window_event_resize_container.add_element(self.attributes_window_event_resize_var)
        self.attributes_window.add_element(self.attributes_window_event_resize_container)
        self.attributes_window_event_resize_var.add_event(ETKCheckboxEvents.TOGGLED, self.__window_attribut_changed_handler)

        self.attributes_window_event_mouse_click_container = ETKListingContainer(self._main, size=ETKContainerSize(0, 0, True, True), listing_type=ETKListingTypes.LEFT_TO_RIGHT, offset=3)
        self.attributes_window_event_mouse_click_const = ETKLabel(self._main, text="Event mouse_click: ", size=Vector2d(147, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=self.attributes_window.background_color)
        self.attributes_window_event_mouse_click_container.add_element(self.attributes_window_event_mouse_click_const)
        self.attributes_window_event_mouse_click_var = ETKCheckbox(self._main, text="", size=Vector2d(17, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=self.attributes_window.background_color)
        self.attributes_window_event_mouse_click_container.add_element(self.attributes_window_event_mouse_click_var)
        self.attributes_window.add_element(self.attributes_window_event_mouse_click_container)
        self.attributes_window_event_mouse_click_var.add_event(ETKCheckboxEvents.TOGGLED, self.__window_attribut_changed_handler)

        self.attributes_window_event_mouse_move_container = ETKListingContainer(self._main, size=ETKContainerSize(0, 0, True, True), listing_type=ETKListingTypes.LEFT_TO_RIGHT, offset=3)
        self.attributes_window_event_mouse_move_const = ETKLabel(self._main, text="Event mouse_move: ", size=Vector2d(140, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=self.attributes_window.background_color)
        self.attributes_window_event_mouse_move_container.add_element(self.attributes_window_event_mouse_move_const)
        self.attributes_window_event_mouse_move_var = ETKCheckbox(self._main, text="", size=Vector2d(17, self.ATTRIBUTES_ELEMENT_HEIGHT), background_color=self.attributes_window.background_color)
        self.attributes_window_event_mouse_move_container.add_element(self.attributes_window_event_mouse_move_var)
        self.attributes_window.add_element(self.attributes_window_event_mouse_move_container)
        self.attributes_window_event_mouse_move_var.add_event(ETKCheckboxEvents.TOGGLED, self.__window_attribut_changed_handler)

        self.__steuerung.on_gui_init()

    # endregion
    # region Methods

    def __mouse_up_event_handler(self) -> None:
        if self.__moving_element != None:
            self.__steuerung.update_element_pos_event(self.__moving_element)
            self.__moving_element = None

    def __mouse_moved_event_handler(self, event: ETKEventData) -> None:
        if event.abs_pos == None:
            raise ValueError
        self.__mouse_pos = event.abs_pos
        self.__update_element_pos()

    def __update_element_pos(self) -> None:
        mouse_pos = self.__mouse_pos
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

    def __element_mouse_down_handler(self, event_data: ETKEventData) -> None:
        if event_data.abs_pos == None:
            raise ValueError
        self.__start_moving_element(
            event_data.sender, event_data.abs_pos - event_data.sender.abs_pos)
        self.__steuerung.update_element_attributes_gui(event_data.sender)

    def __element_attribut_changed_handler(self, event_data: ETKEventData) -> None:
        if type(event_data.sender) == ETKCheckbox or type(event_data.sender) == ETKEdit:
            self.__steuerung.set_element_attribute_event(event_data.sender)

    def __window_attribut_changed_handler(self, event_data: ETKEventData) -> None:
        if type(event_data.sender) == ETKCheckbox or type(event_data.sender) == ETKEdit:
            self.__steuerung.set_window_attribute_event(event_data.sender)

    def __menubar_left_handler(self, event_data: ETKEventData) -> None:
        new_element = self.__steuerung.create_new_element_event(event_data.sender)
        self.__start_moving_element(new_element)
        self.__steuerung.update_element_attributes_gui(new_element)

    def __delete_element_event(self) -> None:
        if self.active_attributes_element is None:
            raise RuntimeError
        self.__steuerung.delete_element(self.active_attributes_element)

    def __element_area_mousedown_handler(self, ev_data: ETKEventData) -> None:
        if ev_data.child_sender == None and self.attributes_element_inner.visibility:
            self.attributes_element_inner.visibility = False
            self.active_attributes_element = None

    def create_new_element(self, typ: Type[ETKBaseTkWidgetText]) -> ETKBaseTkWidgetText:
        new_element = typ(self._main)  # type:ignore
        new_element.outline_color = 0x0
        new_element.outline_thickness = 2

        if isinstance(new_element, ETKBaseWidgetDisableable):
            try:
                new_element.enabled = False
            except AttributeError:
                pass

        new_element.add_event(ETKEvents.MOUSE_DOWN, self.__element_mouse_down_handler)
        self.element_area.add_element(new_element)
        return new_element

    def __start_moving_element(self, element: ETKBaseObject, rel_click_pos: Vector2d = Vector2d()):
        self.__moving_element = element
        self.__moving_element_rel_click_pos = rel_click_pos
