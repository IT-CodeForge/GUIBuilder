#add .get() for events
import os.path


class Generator:
    def __init__(self) -> None:
        self.gui_h = "GUI.h"
        self.gui_cpp = "GUI.cpp"
        self.event_cpp = "UserGUI.cpp"
        self.function_end = '}'
        self.offset = "  "
        self.type_translation = {"button": "TGWButton",
                                "window": "TGWMainWindow",
                                "timer": "TGWTimer",
                                "label": "TGWEdit",
                                "edit": "TGWEdit",
                                "checkbox": "TGWCheckBox",
                                "timer": "TGWTimer",
                                "canvas": "TGWBitmapWindow.h"}

                                



    def write_files(self, path: str, objects: list[dict[str, any]]):
        if not os.path.exists(os.path.join(path, self.gui_h)):
            self.__write_data(os.path.join(path, self.gui_h), "")
        if not os.path.exists(os.path.join(path, self.gui_cpp)):
            self.__write_data(os.path.join(path, self.gui_cpp), "")
        if not os.path.exists(os.path.join(path, self.event_cpp)):
            self.__write_data(os.path.join(path, self.event_cpp), "")
        self.__write_data(os.path.join(path, self.gui_h), self.__generate_h("GUI.h", objects, "TGWMainWindow.h"))
        self.__write_data(os.path.join(path, self.gui_cpp), self.__generate_cpp(objects))
        self.__write_data(os.path.join(path, self.event_cpp), self.__generate_cpp_user(path, objects))
    




    def __generate_h(self, className: str, objects: list[dict[str, any]], inheritance: str = '') -> str:
        ret_str  = '#ifndef _' + className[:className.find('.')] + '_h_\n'
        ret_str += '#define _' + className[:className.find('.')] + '_h_\n'
        ret_str += '#include "TGWMainWindow.h"\n'
        ret_str += '#include "TGW_AllClassDeclarations.h"\n'
        ret_str += "\n\nclass " + className[:className.find('.') ]
        if inheritance != "":
            ret_str += " : public " + inheritance[:inheritance.find('.')]
        ret_str += "\n{\n"

        ret_str += self.__generate_attributes(objects)
        
        ret_str += 'private:\n'
        for object in objects:
            if object["type"] == "window":
                if object.get("eventCreate") == True:
                    ret_str += "  void eventShow();\n  void event_Create_Window();\n"
                if object.get("eventPaint") == True:
                    ret_str += "  void eventPaint(HDC hDeviceContext);\n  void event_Paint_Background(HDC hDeviceContext);\n"
                if object.get("eventResize") == True:
                    ret_str += "  void eventResize();\n  void event_Resize_Window();\n"
                if object.get("eventMouseClick") == True:
                    ret_str += "  void eventMouseClick(int posX, int posY, TGWindow* affectedWindow);\n  void event_Click_Mouse(int posX, int posY, TGWindow* affectedWindow);\n"
                if object.get("eventMouseMove") == True:
                    ret_str += "  void eventMouseMove(int posX, int posY);\n  void event_Move_Mouse(int posX, int posY);\n"
                continue
            if object.get("eventPressed", False):
                ret_str += "  void event_pressed_" + object["name"] + "(int event);\n"
            if object.get("eventHovered", False):
                ret_str += "  void event_hovered_" + object["name"] + "();\n"
            if object.get("eventChanged", False):
                if object.get("type", "") == "edit":
                    ret_str += "  void event_changed_" + object["name"] + "();\n"
                if object.get("type", "") == "checkbox":
                    ret_str += "  void event_changed_" + object["name"] + "(int isChecked_1_0);\n"
            if object.get("type", "") == "timer":
                ret_str += "  void event_timer_" + object["name"] + ""
        ret_str += '  void eventCheckBox(TGWCheckBox* eineCheckBox, int isChecked_1_0);\n'
        ret_str += '  void eventEditChanged(TGWEdit* einEdit);\n'
        ret_str += '  void eventButton(TGWButton* einButton, int event);\n'
        ret_str += '  void eventTimer(int id);\n'
        #ret_str += "  void eventHovered(void* id);\n" | hovered vorerst gescrapt
        ret_str += 'public:\n  GUI();\n'
        ret_str += '};\n\n#endif'
        return ret_str
    
    def __generate_cpp(self, objects: list[dict[str, any]]) -> str:
        ret_str  = '#include "GUI.h"\n#include "TGW_AllClassDefinitions.h"\n#include "TGWTimer.h"\n\n'
        for object in objects:
            if object["type"] == "window":
                ret_str += '\nGUI::GUI()\n  :TGWMainWindow('
                ret_str += "10, 10, "
                ret_str += str(object["size"][0]) + ", " + str(object["size"][1]) + ", "
                ret_str += '"' + str(object["text"]) + '", '
                ret_str += "0x" + self.__hex_color_converter(object["backgroundColor"][0]) + self.__hex_color_converter(object["backgroundColor"][1])+ self.__hex_color_converter(object["backgroundColor"][2]) + ')\n{\n'
                break
        
        ret_str += self.__generate_constructor(objects)

        ret_str += self.__generate_button_event(objects)
        ret_str += self.__generate_timer_event(objects)
        ret_str += self.__generate_changed_event(objects)
        ret_str += self.__generate_parsed_events(objects)
        #ret_str += self.__generate_hov_event(objects) | hovered vorerst gescrapt
        return ret_str
    
    def __generate_cpp_user(self, path: str, objects: list[dict[str, any]]) -> str:
        ret_str = self.__read_data(os.path.join(path, self.event_cpp))
        if ret_str.find('#include "GUI.h"\n\n') != -1:
            ret_str = ret_str.replace(ret_str[:ret_str.find('#include "GUI.h"\n\n') + 18], "")
        ret_str = self.__check_user_includes(objects) + '#include "GUI.h"\n\n' + ret_str
        already_added_events = []

        temp_str = ret_str
        while temp_str.find("void GUI::event_") != -1:
            start_index = temp_str.find("void GUI::event_")
            end_index   = self.__get_method_contents(temp_str[start_index:])[0][2]
            event_name  = temp_str[temp_str[start_index + 16:].find("_") + start_index + 17:temp_str.find("(", start_index)]
            event_type  = temp_str[start_index + 16:temp_str[start_index + 16:].find("_") + start_index + 16]
            print(event_name, event_type)
            is_in_list   = False
            for object in objects:
                type_checking  = (event_type == "pressed" and object.get("eventPressed", False)) or (event_type == "hovered" and object.get("eventHovered", False)) or (event_type == "changed" and object.get("eventChanged", False))
                type_checking |= (event_type == "Create" and object.get("eventCreate", False)) or (event_type == "Resize" and object.get("eventResize", False)) or (event_type == "Paint" and object.get("eventPaint", False)) or (event_type == "Click" and object.get("eventMouseClicked", False)) or (event_type == "Move" and object.get("eventMouseMove", False))
                if object["type"] == "window":
                    if type_checking:
                        is_in_list = True
                        already_added_events.append([event_name, event_type])
                    continue
                if event_name == object["name"] and (type_checking):
                    is_in_list = True
                    already_added_events.append([event_name, event_type])
            if not is_in_list:
                ret_str = ret_str.replace(ret_str[start_index:end_index + start_index + 2], "")
            temp_str = temp_str[start_index + 24:]

        for object in objects:
            if object["type"] == "window":
                if ["Window", "Create"] not in already_added_events and object.get("eventCreate") == True:
                    ret_str += "void GUI::event_Create_Window()\n{\n}\n"
                if ["Background", "Paint"] not in already_added_events and object.get("eventPaint") == True:
                    ret_str += "void GUI::event_Paint_Background(HDC hDeviceContext)\n{\n}\n"
                if ["Window", "Resize"] not in already_added_events and object.get("eventResize") == True:
                    ret_str += "void GUI::event_Resize_Window()\n{\n}\n"
                if ["Mouse", "Click"] not in already_added_events and object.get("eventMouseClick") == True:
                    ret_str += "void GUI::event_Click_Mouse(int posX, int posY, TGWindow* affectedWindow)\n}\n"
                if ["Mouse", "Move"] not in already_added_events and object.get("eventMouseMove") == True:
                    ret_str += "void GUI::event_Move_Mouse(int posX, int posY)\n{\n}\n"
                continue
            if [object["name"], "pressed"] not in already_added_events and object.get("eventPressed", False):
                    ret_str += "void GUI::event_pressed_" + object["name"] + "(int event)\n{\n}\n\n"
            if [object["name"], "hovered"] not in already_added_events and object.get("eventHovered", False):
                    ret_str += "void GUI::event_hovered_" + object["name"] + "()\n{\n}\n\n"
            if [object["name"], "changed"] not in already_added_events and object.get("eventChanged", False):
                if object["type"] == "edit":
                    ret_str += "void GUI::event_changed_" + object["name"] + "()\n{\n}\n\n"
                if object["type"] == "checkbox":
                    ret_str += "void GUI::event_changed_" + object["name"] + "(int isChecked_1_0)\n{\n}\n\n"
        
        return ret_str





    

    def __generate_constructor(self, objects: list[dict[str, any]]) -> str:
        ret_str = ""
        for object in objects:
            if object["type"] == "window":
                continue
            ret_str += self.offset + object["name"] + " = " + self.__generate_cpp_object(object)
        ret_str += self.function_end + "\n"
        for object in objects:
            if object["type"] == "window":
                continue
            if "backgroundColor" in object:
                ret_str += "" #macht was sobald man die Farbe in Hallmans image sten kann|self.offset + object["name"] + "->set"
        return ret_str

    
    def __generate_attributes(self, objects: list[dict[str, any]]) -> str:
        ret_str = ""
        for object in objects:
            if object["type"] == "window":
                continue
            ret_str += self.offset + self.type_translation[object["type"]] + "* " + object["name"] + ";\n"
        
        ret_str += "\n"

        for object in objects:
            if object["type"] == "timer":
                ret_str += "int " + object["name"] + "Id = " + str(object["id"] + 1) + ";\n"
                ret_str += "bool " + object["name"] + "IsEnabled = " + str(object["enabled"]).lower() + ";\n"
        
        return ret_str


    def __generate_button_event(self, objects: list[dict[str, any]]) -> str:
        ret_str = "\nvoid GUI::eventButton(TGWButton* einButton, int event)\n{\n"
        for object in objects:
            if object["type"] == "button" and object["eventPressed"]:
                ret_str += "  if(einButton == this->" + object["name"] + ")\n  {\n"
                ret_str += "    event_pressed_" + object["name"] + "(event);\n  }\n"
        ret_str += self.function_end + "\n"
        return ret_str
    
    def __generate_timer_event(self, objects: list[dict[str, any]]) -> str:
        ret_str  = "\nvoid GUI::eventTimer(int id)\n{\n"
        for object in objects:
            if object["type"] == "timer":
                ret_str += "  if(id == " + object["name"] + "Id && " + object["name"] + "IsEnabled == true)\n  {\n"
                ret_str += "    event_timer_" + object["name"] + "();\n  }\n"
        ret_str += self.function_end + "\n"
        return ret_str
    
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
    
    def __generate_changed_event(self, objects: list[dict[str, any]]) -> str:
        ret_str  = "void GUI::eventCheckBox(TGWCheckBox* eineCheckBox, int isChecked_1_0)\n{\n"
        for object in objects:
            if object["type"] == "checkbox":
                ret_str += "  if(eineCheckBox == this->" + object["name"] + ")\n  {\n"
                ret_str += "    event_changed_" + object["name"] + "(isChecked_1_0);\n  }\n"
        ret_str += self.function_end + "\n"
        ret_str += "void GUI::eventEditChanged(TGWEdit* einEdit)\n{\n"
        for object in objects:
            if object["type"] == "edit":
                ret_str += "  if(einEdit == this->" + object["name"] + ")\n  {\n"
                ret_str += "    event_changed_" + object["name"] + "();\n  }\n"
        ret_str += self.function_end + "\n"
        return ret_str
    
    def __generate_parsed_events(self, objects: list[dict[str, any]]) -> str:
        ret_str = ""
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

	
	



    def __generate_button(self, object: dict[str, any]) -> str:
        ret_str  = ""
        ret_str += "new " + self.type_translation[object["type"]] + "(this, "
        ret_str += str(object["position"][0]) + ", " + str(object["position"][1]) + ", "
        ret_str += str(object["size"][0]) + ", " + str(object["size"][1]) + ", "
        ret_str += '"' + object["text"] + '");\n'
        return ret_str
    
    def __generate_label(self, object: dict[str, any]) -> str:
        ret_str  = ""
        ret_str += "new " + self.type_translation[object["type"]] + "(this, "
        ret_str += str(object["position"][0]) + ", " + str(object["position"][1]) + ", "
        ret_str += str(object["size"][0]) + ", " + str(object["size"][1]) + ", "
        ret_str += '"' + object["text"] + '", false, false);\n'
        return ret_str
    
    def __generate_edit(self, object: dict[str, any]) -> str:
        ret_str  = ""
        ret_str += "new " + self.type_translation[object["type"]] + "(this, "
        ret_str += str(object["position"][0]) + ", " + str(object["position"][1]) + ", "
        ret_str += str(object["size"][0]) + ", " + str(object["size"][1]) + ", "
        ret_str += '"' + object["text"] + '", ' + object["multipleLines"] + ', false);\n'
        return ret_str
    
    def __generate_checkbox(self, object: dict[str, any]) -> str:
        ret_str  = ""
        ret_str += "new " + self.type_translation[object["type"]] + "(this, "
        ret_str += str(object["position"][0]) + ", " + str(object["position"][1]) + ", "
        ret_str += str(object["size"][0]) + ", " + str(object["size"][1]) + ", "
        ret_str += '"' + object["text"] + '", ' + str(object["checked"]).lower() + ');\n'
        return ret_str
    
    def __generate_timer(self, object: dict[str, any]) -> str:
        ret_str  = ""
        ret_str += "new " + self.type_translation[object["type"]] + "(this, "
        ret_str += str(object["interval"][0]) + ", "
        ret_str += '&' + object["name"] + 'Id);\n'
        return ret_str
    
    

    def __check_user_includes(self, objects: list[dict[str, any]]) -> str:
        ret_str = ""
        unique_type_list = []
        for object in objects:
            if object["type"] == "window":
                continue
            if object["type"] not in unique_type_list:
                unique_type_list.append(object["type"])
        
        for type in unique_type_list:
            ret_str += '#include "' + self.type_translation[type] + '.h"\n'
        return ret_str
    
    
    def __generate_cpp_object(self, object: dict[str, any]) -> str:
        ret_str = ""
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
        return ret_str
    




    def __write_data(self, file: str, data: str):
        with open(file, "w") as f:
            f.write(data)
    
    def __read_data(self, file: str) -> str:
        data = ""
        with open(file, "r") as f:
            data = f.read()
        return data
        




    def __hex_color_converter(self, num: int) -> str:
        hex_num = hex(num).lstrip("0x")[:2]
        while len(hex_num) < 2:
            hex_num = "0" + hex_num
        return hex_num[:2]
    
    def __get_method_contents(self, string_file:str) -> list[list[str,int,int]]:
        method_contents = []
        level = 0
        t_start_i = 0
        for i, char in enumerate(string_file):
            if char == "{":
                if level == 0:
                    t_start_i = i
                level += 1
            elif char == "}":
                level -= 1
                if level == 0:
                    method_contents.append([string_file[t_start_i:i+1], t_start_i, i+1])
        return method_contents


        


    
if __name__ == "__main__":
    myGenerator = Generator()
    objects = [{"type": "window", "position": [10,10], "size": [1024,512], "text": "Hallo", "backgroundColor": [12,23,34], "eventMouseMove": True},{"type": "button", "name": "einButton", "position": [10,10], "size": [128,64], "text": "Knopf", "eventPressed": True, "eventChanged": False},{"type": "checkbox", "name": "meineCheckbox", "position": [10,84], "size": [128,64], "text": "ich bin eine Checkbox", "eventChanged": True, "checked": False}]
    myGenerator.write_files("", objects)

#,{"type": "button", "name": "einButton", "position": [10,10], "size": [128,64], "text": "Knopf", "eventPressed": True, "eventHovered": False, "eventChanged": False},{"type": "button", "name": "einButton2", "position": [10,30], "size": [128,64], "text": "Knopf2", "eventPressed": True, "eventHovered": False, "eventChanged": False}
#and (event_type == "pressed" and not object["eventPressed"]) or (event_type == "hovered" and not object["eventHovered"]) or (event_type == "changed" and not object["eventChanged"])
"""
noch zu tun
type: "label":
	id
	name
	text
	position
	size
	backgroundColor // nicht möglich in Hallmann
	textColor // nicht möglich in Hallmann
	
type: "edit":
	id
	name
	text
	position
	size
	backgroundColor // nicht möglich in Hallmann
	textColor // nicht möglich in Hallmann
	multipleLines

pressed
hovered
changed
"""