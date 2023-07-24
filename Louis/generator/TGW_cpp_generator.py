class TGW_cpp_generator:
    def __init__(self, type_translation: dict[str, str]) -> None:
        self.__type_translation: dict[str, str] = type_translation

    def generate_cpp(self, objects: list[dict[str, any]]) -> str:
        #includes
        ret_str: str  = '#include "GUI.h"\n#include "TGW_AllClassDefinitions.h"\n#include "TGWTimer.h"\n\n'

        #generate constructor definition head
        for object in objects:

            if object["type"] == "window":
                ret_str += '\nGUI::GUI()\n  :TGWMainWindow('
                ret_str += "10, 10, "
                ret_str += str(object["size"][0]) + ", " + str(object["size"][1]) + ", "
                ret_str += '"' + str(object["text"]) + '", '
                ret_str += "0x" + self.__hex_color_converter(object["backgroundColor"][0]) + self.__hex_color_converter(object["backgroundColor"][1])+ self.__hex_color_converter(object["backgroundColor"][2]) + ')\n{\n'
                break
        
        #generate constructor definition
        ret_str += self.__generate_constructor(objects)

        #generate native event definitions
        ret_str += self.__generate_button_event(objects)
        ret_str += self.__generate_timer_event(objects)
        ret_str += self.__generate_changed_event(objects)
        ret_str += self.__generate_parsed_events(objects)
        return ret_str

#generate constructor    
    def __generate_constructor(self, objects: list[dict[str, any]]) -> str:
        ret_str: str = ""

        for object in objects:

            if object["type"] == "window":
                continue
            ret_str += "  " + object["name"] + " = " + self.__generate_cpp_object(object)

        for object in objects:

            if object["type"] == "canvas":
               #erstmal gescrapt, bis die setBackgroundColor methode funktioniert | ret_str += self.offset + object["name"] + "->canvas->setBackgroundColor(0x" + self.__hex_color_converter(object["backgroundColor"][0]) + self.__hex_color_converter(object["backgroundColor"][1]) + self.__hex_color_converter(object["backgroundColor"][2]) + ");\n"
                pass
        ret_str += "}\n"

        return ret_str

#Generate Element Events (Events from Buttons, Checkboxes, Edits, etc.)
    def __generate_button_event(self, objects: list[dict[str, any]]) -> str:
        ret_str: str = "\nvoid GUI::eventButton(TGWButton* einButton, int event)\n{\n"
        for object in objects:
            if object["type"] == "button" and object["eventPressed"]:
                ret_str += "  if(einButton == this->" + object["name"] + ")\n  {\n"
                ret_str += "    event_pressed_" + object["name"] + "(event);\n  }\n"
        ret_str += "}\n"
        return ret_str
    
    def __generate_timer_event(self, objects: list[dict[str, any]]) -> str:
        ret_str: str  = "\nvoid GUI::eventTimer(int id)\n{\n"
        for object in objects:
            if object["type"] == "timer":
                ret_str += "  if(id == " + object["name"] + "Id && " + object["name"] + "IsEnabled == true)\n  {\n"
                ret_str += "    event_timer_" + object["name"] + "();\n  }\n"
        ret_str += "}\n"
        return ret_str
    
    def __generate_changed_event(self, objects: list[dict[str, any]]) -> str:
        ret_str: str  = "void GUI::eventCheckBox(TGWCheckBox* eineCheckBox, int isChecked_1_0)\n{\n"

        for object in objects:

            if object["type"] == "checkbox":
                ret_str += "  if(eineCheckBox == this->" + object["name"] + ")\n  {\n"
                ret_str += "    event_changed_" + object["name"] + "(isChecked_1_0);\n  }\n"
        ret_str += "}\n"
        ret_str += "void GUI::eventEditChanged(TGWEdit* einEdit)\n{\n"

        for object in objects:

            if object["type"] == "edit":
                ret_str += "  if(einEdit == this->" + object["name"] + ")\n  {\n"
                ret_str += "    event_changed_" + object["name"] + "();\n  }\n"
        ret_str += "}\n"

        return ret_str


#Generate window Events (Mouse move, mouse Click, Create Window, etc.)    
    def __generate_parsed_events(self, objects: list[dict[str, any]]) -> str:
        ret_str: str = ""

        for object in objects:

            if object.get("type") != "window":
                continue

            if object.get("eventCreate") == True:
                ret_str += "\nvoid GUI::eventShow()\n{\n  event_Create_Window();\n}\n"

            if object.get("eventPaint") == True:
                ret_str += "\nvoid GUI::eventPaint(HDC hDeviceContext)\n{\n  event_Paint_Background(hDeviceContext);\n}\n"

            if object.get("eventResize") == True:
                ret_str += "\nvoid GUI::eventResize()\n{\n  event_Resize_Window();\n}\n"

            if object.get("eventMouseClick") == True:
                ret_str += "\nvoid GUI::eventMouseClick(int posX, int posY, TGWindow* affectedWindow)\n{\n  event_Click_Mouse(posX, posY, affectedWindow);\n}\n"

            if object.get("eventMouseMove") == True:
                ret_str += "\nvoid GUI::eventMouseMove(int posX, int posY)\n{\n  event_Move_Mouse(posX, posY);\n}\n"

        return ret_str


#Genertion of new Objects
    def __generate_cpp_object(self, object: dict[str, any]) -> str:
        ret_str: str = ""

        if object["type"] == "button":
            ret_str += self.__generate_button(object)

        if object["type"] == "label":
            ret_str += self.__generate_label(object)

        if object["type"] == "edit":
            ret_str += self.__generate_edit(object)

        if object["type"] == "checkbox":
            ret_str += self.__generate_checkbox(object)

        if object["type"] == "timer":
            ret_str += self.__generate_timer(object)

        if object["type"] == "canvas":
            ret_str += self.__generate_canvas(object)

        return ret_str


    def __generate_button(self, object: dict[str, any]) -> str:
        ret_str: str  = ""
        ret_str += "new " + self.__type_translation[object["type"]] + "(this, "
        ret_str += str(object["position"][0]) + ", " + str(object["position"][1]) + ", "
        ret_str += str(object["size"][0]) + ", " + str(object["size"][1]) + ", "
        ret_str += '"' + object["text"] + '");\n'

        return ret_str


    def __generate_label(self, object: dict[str, any]) -> str:
        ret_str: str  = ""
        ret_str += "new " + self.__type_translation[object["type"]] + "(this, "
        ret_str += str(object["position"][0]) + ", " + str(object["position"][1]) + ", "
        ret_str += str(object["size"][0]) + ", " + str(object["size"][1]) + ", "
        ret_str += '"' + object["text"] + '", false, false);\n'

        return ret_str


    def __generate_edit(self, object: dict[str, any]) -> str:
        ret_str: str  = ""
        ret_str += "new " + self.__type_translation[object["type"]] + "(this, "
        ret_str += str(object["position"][0]) + ", " + str(object["position"][1]) + ", "
        ret_str += str(object["size"][0]) + ", " + str(object["size"][1]) + ", "
        ret_str += '"' + object["text"] + '", ' + str(object["multipleLines"]).lower() + ', false);\n'

        return ret_str


    def __generate_checkbox(self, object: dict[str, any]) -> str:
        ret_str: str  = ""
        ret_str += "new " + self.__type_translation[object["type"]] + "(this, "
        ret_str += str(object["position"][0]) + ", " + str(object["position"][1]) + ", "
        ret_str += str(object["size"][0]) + ", " + str(object["size"][1]) + ", "
        ret_str += '"' + object["text"] + '", ' + str(object["checked"]).lower() + ');\n'

        return ret_str


    def __generate_timer(self, object: dict[str, any]) -> str:
        ret_str: str  = ""
        ret_str += "new " + self.__type_translation[object["type"]] + "(this, "
        ret_str += str(object["interval"]) + ", "
        ret_str += '&' + object["name"] + 'Id);\n'

        return ret_str


    def __generate_canvas(self, object: dict[str, any]) -> str:
        ret_str: str  = ""
        ret_str += "new " + self.__type_translation[object["type"]] + "(this, "
        ret_str += str(object["position"][0]) + ", " + str(object["position"][1]) + ", "
        ret_str += str(object["size"][0]) + ", " + str(object["size"][1]) + ');\n'

        return ret_str


#Utility    
    def __hex_color_converter(self, num: int) -> str:
        hex_num: str = hex(num).lstrip("0x")[:2]

        while len(hex_num) < 2:
            hex_num = "0" + hex_num

        return hex_num[:2]




"""
code for scrapped hover event
def __generate_hov_event(self, objects: list[dict[str, any]]) -> str:
        ret_str  = "void GUI::eventHovered(void* id)\n{\n"
        for object in objects:
            if object["type"] == "window":
                continue
            if object.get("eventHovered", False):
                ret_str += "  if(id == " + object["name"] + ")\n  {\n"
                ret_str += "    event_hovered_" + object["name"] + "();\n  }\n"
        ret_str += self.function_end + "\n"
        return ret_str
"""