from intermediary.intermediary import Intermediary
from intermediary.intermediary import ObjectEnum

if __name__ == "__main__":
    intermediary: Intermediary = Intermediary()

    # The frontend now adds objects...
    button_1_id = intermediary.createObject(ObjectEnum.BUTTON)
    button_1_object = intermediary.getObject(button_1_id)
    button_1_object.setAttribute("name", "Button1")
    button_1_object.setAttribute("text", "Hello")
    button_1_object.setAttribute("position", [0, 0])
    button_1_object.setAttribute("size", [20, 20])

    button_2_id = intermediary.createObject(ObjectEnum.BUTTON)
    button_2_object = intermediary.getObject(button_2_id)
    button_2_object.setAttribute("name", "Button2")
    button_2_object.setAttribute("text", "Bye")
    button_2_object.setAttribute("position", [25, 0])
    button_2_object.setAttribute("size", [20, 20])

    # Generator starts here.
    objects: dict[int, any] = intermediary.getObjects()

    for object in objects:
        print(object)