from static_GUI import static_GUI
from ETK import *

class GUI(static_GUI):
    def _on_init(self)->None:
#tag:user_init#
        pass

#tag:event_funcs#

if __name__ == '__main__':
    w = GUI()
    w.run()