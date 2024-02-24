import BMainWindow
from BCanvasItem import *
from BButton     import *
from BLabel      import *
from BCheckbox   import *
from BEdit       import *
from BTimer      import BTimer
from BContainer  import *
from BListingContainer import *
from BBitmap     import *

class GUI(BMainWindow.BMainWindow):
    def __init__(self) -> None:
        super().__init__(pos_x=0, pos_y=40, width=1540, height=768)
    
    def add_elements(self):
        self.menubar = BContainer()
        self.menubar.width = 600
        self.menubar.height = 20

        self.element_menubar = BListingContainer(listing_type=ListingTypes.LEFT_TO_RIGHT)
        self.element_menubar.pos = vector2d(10, 10)
        self.element_menubar.width = 1000
        self.element_menubar.height = 20
        self.menubar.add_element(self.element_menubar, allignment=Alignments.TOP_RIGHT)

        self.menu_button = BButton(self.object_id, "Button")
        self.menu_label = BLabel(self.object_id, "Label")
        self.menu_edit = BLabel(self.object_id, "Edit")
        self.menu_checkbox = BCheckbox(self.object_id, "Checkbox")
        self.menu_canvas = BLabel(self.object_id, "Canvas")
        self.menu_timer = BLabel(self.object_id, "Timer")

        self.menu_button.enabled = False
        self.menu_checkbox.enabled = False

        self.element_menubar.elements = [self.menu_button, self.menu_label, self.menu_edit, self.menu_checkbox, self.menu_canvas, self.menu_timer]
        

if __name__ == '__main__':
  w = GUI()
  w.run()