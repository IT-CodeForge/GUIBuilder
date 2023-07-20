from difflib import restore
import os.path
from turtle import st

class Generator:
    def __init__(self) -> None:
        self.gui_h = "GUI.h"
        self.gui_cpp = "GUI.cpp"
        self.event_cpp = "UserGUI.cpp"
        self.function_end = '}'
        self.offset = "  "
        self.type_translation = {"button": "TGWButton",
                                "window": "TGWMainWindow",
                                "timer": "TGWTimer"}

                                



    def write_files(self, path: str, objects: list[dict[str, any]]):
        if not os.path.exists(os.path.join(path, self.gui_h)):
            self.__write_data(os.path.join(path, self.gui_h), "")
        if not os.path.exists(os.path.join(path, self.gui_cpp)):
            self.__write_data(os.path.join(path, self.gui_cpp), "")
        if not os.path.exists(os.path.join(path, self.event_cpp)):
            self.__write_data(os.path.join(path, self.event_cpp), "")
        self.__write_data(os.path.join(path, self.gui_h), self.__generate_h("GUI.h", objects, "TGWMainWindow.h"))
        self.__write_data(os.path.join(path, self.gui_cpp), self.__generate_cpp(objects))
        self.__write_data(os.path.join(path, self.event_cpp), self.__generate_cpp_user(objects))
    




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
        
        ret_str += 'public:\n  GUI();\n  void eventMouseMove(int posX, int posY);\n'
        for object in objects:
            if object["type"] == "window":
                continue
            if object["eventPressed"]:
                ret_str += "  void event_pressed_" + object["name"] + "(int event);\n"
            if object["eventHovered"]:
                ret_str += "  void event_hovered_" + object["name"] + "();\n"
            if object["eventChanged"]:
                ret_str += "  void event_changed_" + object["name"] + "();\n"
        ret_str += 'private:\n'
        ret_str += "  void hoveredEvent();\n"
        ret_str += '  void eventButton(TGWButton* einButton, int event);\n'
        ret_str += '  void eventTimer(TGWMainWindow* messageHandlerWindow, int intervallMilliSeconds, int* id);\n'
        ret_str += '};\n\n#endif'
        return ret_str
    
    def __generate_cpp(self, objects: list[dict[str, any]]) -> str:
        ret_str  = '#include "GUI.h"\n#include "TGW_AllClassDefinitions.h"\n#include "TGWTimer"\n\n'
        for object in objects:
            if object["type"] == "window":
                ret_str += '\nGUI::GUI()\n  :TGWMainWindow('
                ret_str += str(object["position"][0]) + ", " + str(object["position"][1]) + ", "
                ret_str += str(object["size"][0]) + ", " + str(object["size"][1]) + ", "
                ret_str += '"' + str(object["text"]) + '", '
                ret_str += "0x" + self.__hex_color_converter(object["backgroundColor"][0]) + self.__hex_color_converter(object["backgroundColor"][1])+ self.__hex_color_converter(object["backgroundColor"][2]) + ')\n{\n'
                break
        
        ret_str += "  hoverEvent = new TGWTimer(this, 1, &hoverTimer);\n"
        for object in objects:
            if object["type"] == "window":
                continue
            ret_str += self.offset + object["name"] + " = " + self.__generate_cpp_object(object)
        ret_str += self.function_end + "\n"


        ret_str += self.__generate_btn_event(objects)
        ret_str += self.__generate_moumo_event()
        ret_str += self.__generate_tim_event(objects)
        ret_str += self.__generate_hov_event(objects)
        return ret_str
    
    def __generate_cpp_user(self, objects: list[dict[str, any]]) -> str:
        ret_str = self.__read_data(self.event_cpp)
        if ret_str.find('#include "GUI.h"\n\n') != -1:
            ret_str = ret_str.replace(ret_str[:ret_str.find('#include "GUI.h"\n\n') + 18], "")
        ret_str = self.__check_user_includes(objects) + '#include "GUI.h"\n\n' + ret_str
        already_added_events = []

        offset = 0
        temp_str = ret_str
        while temp_str.find("void GUI::event_") != -1:
            start_index = temp_str.find("void GUI::event_")
            end_index   = self.__get_method_contents(temp_str[start_index:])[0][2]
            event_name  = temp_str[start_index + 24:temp_str.find("(", start_index)]
            event_type  = temp_str[start_index + 16:start_index + 23]
            is_in_list   = False
            for object in objects:
                if object["type"] == "window":
                    continue
                if event_name == object["name"] and ((event_type == "pressed" and object["eventPressed"]) or (event_type == "hovered" and object["eventHovered"]) or (event_type == "changed" and object["eventChanged"])):
                    is_in_list = True
                    already_added_events.append([event_name, event_type])
            if not is_in_list:
                ret_str = ret_str.replace(ret_str[start_index:end_index + start_index + 2], "")
            temp_str = temp_str[start_index + 24:]
            offset += start_index

        for object in objects:
            if object["type"] == "window":
                continue
            if [object["name"], "pressed"] not in already_added_events and object["eventPressed"]:
                        ret_str += "void GUI::event_pressed_" + object["name"] + "(int event)\n{\n}\n\n"
            if [object["name"], "hovered"] not in already_added_events and object["eventHovered"]:
                        ret_str += "void GUI::event_hovered_" + object["name"] + "()\n{\n}\n\n"
            if [object["name"], "changed"] not in already_added_events and object["eventChanged"]:
                        ret_str += "void GUI::event_changed_" + object["name"] + "()\n{\n}\n\n"
        
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





    def __check_user_includes(self, objects: list[dict[str, any]]) -> str:
        ret_str = ""
        unique_type_list = []
        for object in objects:
            if object["type"] == "button" and "button" not in unique_type_list:
                unique_type_list.append("button")
        
        for type in unique_type_list:
            ret_str += '#include "' + self.type_translation[type] + '.h"\n'
        return ret_str
    
    
    def __generate_cpp_object(self, object: dict[str, any]) -> str:
        ret_str = ""
        if object["type"] == "button":
            ret_str += self.__generate_button(object)
            return ret_str
        return ret_str
    

    def __generate_attributes(self, objects: list[dict[str, any]]) -> str:
        ret_str = "  TGWTimer* hoverTimer = 1;\n"
        for object in objects:
            if object["type"] == "window":
                continue
            ret_str += self.offset + self.type_translation[object["type"]] + "* " + object["name"] + ";\n"
        
        ret_str += "\n"
        
        for object in objects:
            if object["type"] == "window":
                continue
            if object["eventHovered"]:
                x1 = object["position"][0]
                y1 = object["position"][1]
                x2 = object["position"][0] + object["size"][0]
                y2 = object["position"][1] + object["size"][1]
                ret_str += "  int " + object["name"] + "Id[4] = {" + f"{x1},{y1},{x2},{y2}" + "};\n"
        ret_str += "  int mouseX = 0;\n  int mouseY = 0;\n"
        return ret_str


    def __generate_btn_event(self, objects: list[dict[str, any]]) -> str:
        ret_str = "\nvoid GUI::eventButton(TGWButton* einButton, int event)\n{\n"
        for object in objects:
            if object["type"] == "button" and object["eventPressed"]:
                ret_str += "  if(einButton == this->" + object["name"] + ")\n  {\n"
                ret_str += "    event_pressed_" + object["name"] + "(event);\n  }\n"
        ret_str += self.function_end + "\n"
        return ret_str
    
    def __generate_tim_event(self, objects: list[dict[str, any]]) -> str:
        ret_str  = "\nvoid GUI::eventTimer(int id)\n{\n"
        ret_str += "  if(id == hoveredId)\n  {\n"
        ret_str += "    checkHovered();\n  }\n"
        for object in objects:
            if object["type"] == "timer":
                ret_str += "  if(id == " + object["name"] + "Id)\n  {\n"
                ret_str += "    event_timer_" + object["name"] + "();\n  }\n"
        ret_str += self.function_end + "\n"
        return ret_str
    
    def __generate_hov_event(self, objects: list[dict[str, any]]) -> str:
        ret_str  = "void GUI::hoveredEvent()\n{\n"
        for object in objects:
            if object["type"] == "window":
                continue
            if object["eventHovered"]:
                ret_str += "  if(mouseX >=" + object["name"] + "Id[0] && mouseX <= " + object["name"] + "Id[2] && mouseY >= " + object["name"] + "Id[1] && mouseY <= " + object["name"] + "Id[3])\n  {\n"
                ret_str += "    event_hovered_" + object["name"] + "();\n  }\n"
        ret_str += self.function_end + "\n"
        return ret_str
    
    def __generate_moumo_event(self) -> str:
        ret_str = "\nvoid GUI::eventMouseMove(int posX, int posY);\n{\n  mouseX = posX;\n  mouseY = posY;\n}\n"
        return ret_str


    def __generate_button(self, object: dict[str, any]) -> str:
        ret_str  = ""
        ret_str += "new " + self.type_translation[object["type"]] + "(this, "
        ret_str += str(object["position"][0]) + ", " + str(object["position"][1]) + ", "
        ret_str += str(object["size"][0]) + ", " + str(object["size"][1]) + ", "
        ret_str += '"' + object["text"] + '");\n'
        return ret_str


        


    
if __name__ == "__main__":
    myGenerator = Generator()
    objects = [{"type": "window", "position": [10,10], "size": [1024,512], "text": "Hallo", "backgroundColor": [12,23,34]},{"type": "button", "name": "einButton", "position": [10,10], "size": [128,64], "text": "Knopf", "eventPressed": True, "eventHovered": True, "eventChanged": False},{"type": "button", "name": "einButton2", "position": [10,30], "size": [128,64], "text": "Knopf2", "eventPressed": True, "eventHovered": False, "eventChanged": False}]
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