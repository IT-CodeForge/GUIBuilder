import os.path

class TGW_usercpp_generator:
    def __init__(self, user_cpp: str, type_translation: dict[str, str]) -> None:
        self.__user_cpp: str = user_cpp
        self.__type_translation: dict[str, str] = type_translation


    def generate_cpp_user(self, path: str, objects: list[dict[str, any]]) -> str:
        #reas old File, so it only changes the things it is allowed to change
        ret_str: str = self.__read_data(os.path.join(path, self.__user_cpp))

        #includes
        if ret_str.find('#include "GUI.h"\n\n') != -1:
            ret_str = ret_str.replace(ret_str[:ret_str.find('#include "GUI.h"\n\n') + 18], "")
        ret_str = self.__check_user_includes(objects) + '#include "GUI.h"\n\n' + ret_str

        #deletes removed user Events
        already_added_and_ret_str = self.__remove_user_events(objects, ret_str)
        ret_str = already_added_and_ret_str[0]
        
        #adds new user events
        ret_str += self.__add_user_events(objects, already_added_and_ret_str[1])
        
        return ret_str
    

    def __remove_user_events(self, objects: list[dict[str, any]], ret_str: str) -> list[str, list[str, str]]:
        already_added_events: list[list[str, str]] = []
        temp_str: str = ret_str
        print(temp_str)

        #finds all events and finds out, if they are stil implemented (e.g. Button event, got turned off)
        while temp_str.find("void GUI::event_") != -1:
            start_index: int = temp_str.find("void GUI::event_")
            end_index: int   = self.__get_method_end(temp_str[start_index:])
            event_name: str  = temp_str[temp_str[start_index + 16:].find("_") + start_index + 17:temp_str.find("(", start_index)]
            event_type: str  = temp_str[start_index + 16:temp_str[start_index + 16:].find("_") + start_index + 16]
            is_in_list: bool = False

            for object in objects:
                #type_checking checks, if the object has a certain event
                type_checking  =  (event_type == "pressed" and object.get("eventPressed", False)) or (event_type == "hovered" and object.get("eventHovered", False)) or (event_type == "changed" and object.get("eventChanged", False)) or (event_type == "timer" and object.get("type") == "timer")
                type_checking        |= (event_type == "Create" and object.get("eventCreate", False)) or (event_type == "Resize" and object.get("eventResize", False)) or (event_type == "Paint" and object.get("eventPaint", False)) or (event_type == "Click" and object.get("eventMouseClicked", False)) or (event_type == "Move" and object.get("eventMouseMove", False))
                
                if object["type"] == "window":
                
                    if type_checking:
                        is_in_list = True
                        already_added_events.append([event_name, event_type])
                    continue
                
                if event_name == object["name"] and (type_checking):
                    is_in_list = True
                    already_added_events.append([event_name, event_type])
            
            if not is_in_list:
                print(event_name, event_type)
                ret_str = ret_str.replace(ret_str[start_index:end_index + start_index + 2], "")
            temp_str = temp_str[start_index + 24:]
        print(already_added_events)

        return [ret_str, already_added_events]

    
    def __add_user_events(self, objects: list[dict[str, any]], already_added_events: list[list[str, str]]) -> str:
        #checks all events, and if one is not already added, add it to the file 
        ret_str: str = ""

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

            if [object["name"], "timer"] not in already_added_events and object["type"] == "timer":
                ret_str += "void GUI::event_timer_" + object["name"] + "()\n{\n}\n\n"

        return ret_str


    def __check_user_includes(self, objects: list[dict[str, any]]) -> str:
        #includes needed Classes
        ret_str: str = ""
        unique_type_list: list[str] = []

        for object in objects:

            if object["type"] == "window":
                continue

            if object["type"] not in unique_type_list:
                unique_type_list.append(object["type"])
        
        for type in unique_type_list:
            ret_str += '#include "' + self.__type_translation[type] + '.h"\n'

        return ret_str


#Utility
    def __read_data(self, file: str) -> str:
        #reads data of a file
        data: str = ""
        with open(file, "r") as f:
            data = f.read()

        return data

    
    def __get_method_end(self, string_file: str) -> int:
        #finds endindex of a method
        level: int = 0

        for i, char in enumerate(string_file):

            if char == "{":
                level += 1

            elif char == "}":
                level -= 1

                if level == 0:
                    return i + 1