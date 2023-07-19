from typing import Any

import eel
from tkinter import Tk, filedialog as fd
from intermediary.intermediary import *

intermediary = Intermediary()

@eel.expose
def load_gui_elements() -> list[dict[str, Any]]:
    global intermediary
    t_objekts = []
    for o in intermediary.getObjects():
        t_objekts.append(o.getAttributesAsDictionary())
    print(intermediary.getObjects())
    print(t_objekts)
    return t_objekts



@eel.expose
def create_btn() -> int:
    t_id = intermediary.createObject(ObjectEnum.BUTTON)
    return intermediary.getObject(t_id).getAttributesAsDictionary()



def generateTestData():
    global intermediary

    print("")
    print("Creating objects.")
    print("********************")

    # Creating objects.
    my_button_object_id = intermediary.createObject(ObjectEnum.BUTTON)
    print(f"Generated an object with ID {my_button_object_id}.")

    print("")
    print("Accessing objects.")
    print("********************")
    
    # Accessing objects.
    my_button_object = intermediary.getObject(my_button_object_id)
    print(f"Got an object for the ID {my_button_object_id}.")
    print(my_button_object)

    print("")
    print("Adding attributes.")
    print("********************")

    # Adding attributes.
    my_button_object.setAttribute("name", "Button1")
    print(f"Added an attribute with ID {my_button_object_id}.")

    print("")
    print("Accessing attributes.")
    print("********************")

    # Accessing attributes.
    name = my_button_object.getAttribute("name")
    print(name)

    print("")
    print("Removing attributes.")
    print("********************")



if __name__ == "__main__":
    #generateTestData() NOTE
    eel.init('additional_files\\gui')
    eel.brw.set_path('chrome', 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe') #NOTE
    eel.start('main.html', size=(320, 120), mode='firefox')