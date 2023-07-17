from intermediary.intermediary import Intermediary
from intermediary.intermediary import ObjectEnum

if __name__ == "__main__":
    intermediary: Intermediary = Intermediary()
    object_ids: list[int] = []

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

    # Removing attributes.
    my_button_object.removeAttribute("name")

    name = my_button_object.getAttribute("name")
    print(name)

    print("")
    print("Removing objects.")
    print("********************")

    # Removing objects.
    intermediary.removeObject(my_button_object_id)

    my_button_object = intermediary.getObject(my_button_object_id)
    print(my_button_object)
