class TGW_header_generator:
    def __init__(self, type_translation: dict[str, str]) -> None:
        self.__type_translation: dict[str, str] = type_translation

    def generate_header(self, objects: list[dict[str, any]]) -> str:
        #ifndef
        ret_str: str  = '#ifndef _GUI_h_\n'
        ret_str += '#define _GUI_h_\n'

        #includes
        ret_str += '#include "TGWMainWindow.h"\n'
        ret_str += '#include "TGW_AllClassDeclarations.h"\n'

        #class head
        ret_str += "\n\nclass GUI : public : TGWMainWindow"
        ret_str += "\n{\n"

        #attribute
        ret_str += self.__generate_attributes(objects)
        
        #declaration of event methods
        ret_str += 'private:\n'
        ret_str += self.__generate_event_declaration(objects)
        

        #declaration constructor
        ret_str += 'public:\n  GUI();\n'
        ret_str += '};\n\n#endif'
        return ret_str


    def __generate_attributes(self, objects: list[dict[str, any]]) -> str:
        ret_str: str = ""

        for object in objects:

            if object["type"] == "window":
                continue
            ret_str += "  " + self.__type_translation[object["type"]] + "* " + object["name"] + ";\n"
        
        ret_str += "\n"

        for object in objects:

            if object["type"] == "timer":
                ret_str += "  int " + object["name"] + "Id = " + str(object["id"] + 1) + ";\n"
                ret_str += "  bool " + object["name"] + "IsEnabled = " + str(object["enabled"]).lower() + ";\n"
        
        return ret_str


    def __generate_event_declaration(self, objects: list[dict[str, any]]) -> str:
        ret_str: str = ""

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
                ret_str += "  void event_timer_" + object["name"] + "();\n"
        ret_str += '  void eventCheckBox(TGWCheckBox* eineCheckBox, int isChecked_1_0);\n'
        ret_str += '  void eventEditChanged(TGWEdit* einEdit);\n'
        ret_str += '  void eventButton(TGWButton* einButton, int event);\n'
        ret_str += '  void eventTimer(int id);\n'

        return ret_str
