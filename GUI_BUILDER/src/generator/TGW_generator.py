import os.path
from generator.TGW_header_generator  import *
from generator.TGW_cpp_generator     import *
from generator.TGW_usercpp_generator import *


class TGW_Generator:
    def __init__(self) -> None:
        self.__gui_h: str = "GUI.h"
        self.__gui_cpp: str = "GUI.cpp"
        self.__user_cpp: str = "UserGUI.cpp"

        self.__type_translation: dict[str, str] = {
            "button": "TGWButton",
            "window": "TGWMainWindow",
            "timer": "TGWTimer",
            "label": "TGWEdit",
            "edit": "TGWEdit",
            "checkbox": "TGWCheckBox",
            "timer": "TGWTimer",
            "canvas": "TGWCanvas"}

        self.__my_tgw_header_generator = TGW_header_generator(self.__type_translation)
        self.__my_tgw_cpp_generator = TGW_cpp_generator(self.__type_translation)
        self.__my_tgw_usercpp_generator = TGW_usercpp_generator(self.__user_cpp, self.__type_translation)


    def write_files(self, path: str, objects: list[dict[str, any]]):
        #creates UserCpp if it doesn't exist, since this reads the file wich would throw an error if the File not already existed
        if not os.path.exists(os.path.join(path, self.__user_cpp)):
            self.__write_data(os.path.join(path, self.__user_cpp), "")

        #creates the different files
        self.__write_data(os.path.join(path, self.__gui_h), self.__my_tgw_header_generator.generate_header(objects))
        self.__write_data(os.path.join(path, self.__gui_cpp), self.__my_tgw_cpp_generator.generate_cpp(objects))
        self.__write_data(os.path.join(path, self.__user_cpp), self.__my_tgw_usercpp_generator.generate_cpp_user(path, objects))
    

    def __write_data(self, file: str, data: str):
        with open(file, "w") as f:
            f.write(data)



        
   
if __name__ == "__main__":
    #code which tests evry functionality
    myGenerator = TGW_Generator()
    objects = [{"type": "window", "position": [10,10], "size": [1024,512], "text": "Hallo", "backgroundColor": [12,23,34], "eventMouseMove": True},
               {"type": "button", "name": "einButton", "position": [10,10], "size": [128,32], "text": "Knopf", "eventPressed": True, "eventChanged": False},
               {"type": "checkbox", "name": "meineCheckbox", "position": [10,52], "size": [128,32], "text": "ich bin eine Checkbox", "eventChanged": True, "checked": False},
               {"id": 0, "type": "timer", "name": "einTimer", "interval": 1000, "enabled": True},
               {"type": "canvas", "name": "einCanvas", "position": [148,10], "size": [138,138], "backgroundColor": [255,0,0]},
               {"type": "label", "name": "einLabel", "position": [10, 94], "size": [12, 128], "text": "Ich bin ein label"},
               {"type": "edit", "name": "einEdit", "position": [148, 94], "size": [12, 128], "text": "Ich bin ein edit", "multipleLines": True, "eventChanged": True}]
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