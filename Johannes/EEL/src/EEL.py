from typing import Any

import eel
from tkinter import Tk, filedialog as fd
from intermediary.intermediary import *

intermediary = Intermediary()

@eel.expose
def load_gui_elements() -> list[dict[str, Any]]:
    global intermediary
    t_intermediary = intermediary
    t_data = t_intermediary.getObjects()
    print(t_data)
    return t_data



@eel.expose
def create_btn() -> int:
    return intermediary.createObject(ObjectEnum.BUTTON)



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
    generateTestData()
    eel.init('additional_files\\gui')
    eel.brw.set_path('chrome', 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe') #NOTE
    eel.start('main.html', size=(320, 120))