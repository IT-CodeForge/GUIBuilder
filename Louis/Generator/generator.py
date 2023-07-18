#import intermediary

from dataclasses import replace


class Generator:
    def __init__(self) -> None:
        self.includes = []
        self.gui_h = "GUI.h"
        self.gui_cpp = "GUI.cpp"
        self.event_cpp = "UserGUI.cpp"
        self.gui_cpp_loop = '\n\nvoid GUI::loop()\n{\n' #WIP
        self.event_cpp_header = '' #WIP
        self.event_cpp_footer = '' #WIP
        self.function_end = '}'
        self.offset = "  "
        self.loopStr = 'voidGUI::loop()'
        self.eventBtn = 'voidGUI::eventButton(TGWButton*einButton,intevent)'
        self.eventChB = 'voidGUI::eventCheckBox(TGWCheckBox*eineCheckBox,intisChecked_1_0)'
        self.typeTranslation = {"button": "TGWButton",
                                "window": "TGWMainWindow"}
        self.type2Code = {"button": self.eventBtn}
    
    def initialize(self):
        self.writeData(self.gui_h, "File initialize, if you read this somthing has gone terribly wrong")
        self.writeData(self.gui_cpp, "File initialize, if you read this somthing has gone terribly wrong")
        self.writeData(self.event_cpp, "")

    def writeData(self, file: str, data: str):
        with open(file, "w") as f:
            f.write(data)
    
    def readData(self, file: str) -> str:
        data = ""
        with open(file, "r") as f:
            data = f.read()
        return data
    
    def getMethodContents(self, file:str) -> list[list[str,int,int]]:
        dataGuicpp = self.readData(file)
        methodContents = []
        level = 0
        t_start_i = 0
        for i, char in enumerate(dataGuicpp):
            if char == "{":
                if level == 0:
                    t_start_i = i
                level += 1
            elif char == "}":
                level -= 1
                if level == 0:
                    methodContents.append([dataGuicpp[t_start_i:i+1], t_start_i, i+1])
        return methodContents
    
    def generateH(self, className: str, objects: list[dict[str, any]], inheritance: str = '') -> str:
        retStr  = '#ifndef _' + className[:className.find('.')] + '_h_\n'
        retStr += '#define _' + className[:className.find('.')] + '_h_\n'
        retStr += '#include "TGWMainWindow.h"\n'
        retStr += '#include "TGW_AllClassDeclarations.h"\n'
        #Platz für extra includes falls notwendig
        retStr += "\n\nclass " + className[:className.find('.') ]
        if inheritance != "":
            retStr += " : public " + inheritance[:inheritance.find('.')]
        retStr += "\n{\n"
        for object in objects:
            if object["type"] == "window":
                continue
            retStr += self.offset + self.typeTranslation[object["type"]] + "* " + object["name"] + ";\n"
        retStr += 'public:\n  GUI();\n  void loop();\n'
        retStr += 'private:\n'
        for object in objects:
            if object["type"] == "window":
                continue
            retStr += "  void event_" + object["name"] + "();\n"
        retStr += '};\n\n#endif'
        return retStr
        
    
    def generateCpp(self, objects: list[dict[str, any]]) -> str:
        retStr  = '#include "GUI.h"\n#include "TGW_AllClassDefinitions.h"\n\n'
        for object in objects:
            if object["type"] == "window":
                retStr += '\nGUI::GUI()\n  :TGWMainWindow('
                retStr += str(object["position"][0]) + ", " + str(object["position"][1]) + ", "
                retStr += str(object["size"][0]) + ", " + str(object["size"][1]) + ", "
                retStr += '"' + str(object["text"]) + '", '
                retStr += "0x" + self.hexColorConverter(object["color"][0]) + self.hexColorConverter(object["color"][1])+ self.hexColorConverter(object["color"][2]) + ')\n{\n'
                break
        for object in objects:
            if object["type"] == "window":
                continue
            retStr += "  " + object["name"] + " = " + self.generateCppObject(object)
        retStr += self.function_end + "\n"
        retStr += "\nvoid GUI::eventButton(TGWButton* einButton, int event)\n{\n"
        for object in objects:
            if object["type"] == "window":
                continue
            retStr += "  if(einButton == " + object["name"] + ")\n{\n"
            retStr += "    event_" + object["name"] + "();\n  }\n"
        retStr += self.function_end + "\n"
        return retStr
    
    def hexColorConverter(self, num: int) -> str:
        hexNum = hex(num).lstrip("0x")[:2]
        while len(hexNum) < 2:
            hexNum = "0" + hexNum
        return hexNum[:2]
    
    def generateCppObject(self, object: dict[str, any]) -> str:
        retStr = ""
        if object["type"] == "button":
            retStr += self.generateButton(object)
            return retStr
        return retStr

    def generateButton(self, object: dict[str, any]) -> str:
        retStr  = ""
        retStr += "new " + self.typeTranslation[object["type"]] + "(this, "
        retStr += str(object["position"][0]) + ", " + str(object["position"][1]) + ", "
        retStr += str(object["size"][0]) + ", " + str(object["size"][1]) + ", "
        retStr += '"' + object["text"] + '");\n'
        return retStr
    
    def generateCppUser(self, objects: list[dict[str, any]]) -> str:
        retStr = self.readData(self.event_cpp)
        oldFile = self.readData(self.event_cpp).replace(" ","")
        oldFile.find(self.eventBtn)
        oldFile.find(self.eventChB)
        eventList = []
        for object in objects:
            if object["type"] == "window":
                continue
            eventList.append(self.type2Code[object["type"]])
        if self.eventBtn in eventList and oldFile.find(self.eventBtn) == -1:
            retStr += "void GUI::eventButton(TGWButton* einButton, int event)\n{\n}\n\n"
        if self.eventBtn not in eventList and oldFile.find(self.eventBtn) != -1:
            eventStartIndex = retStr.find("void GUI::eventButton(TGWButton* einButton, int event)")
            eventEndIndex   = self.getMethodContents(retStr[eventStartIndex:])[0][2]
            retStr.replace(retStr[eventStartIndex:eventEndIndex], '')
        tempStr = retStr
        while tempStr.find("void event_") != -1:
            startIndex = tempStr.find("void event_")
            endIndex   = self.getMethodContents(tempStr[startIndex:])[0][2]
            content    = self.getMethodContents(tempStr[startIndex:])[0][0] #WIP
        
        if oldFile.find(self.loopStr) == -1:
            retStr += "void GUI::loop()\n{\n}\n\n"
        
        return retStr
            




#void eventButton(TGWButton* einButton, int event) {};´
#void eventCheckBox(TGWCheckBox* eineCheckBox, int isChecked_1_0) {};

        


    
if __name__ == "__main__":
    myGenerator = Generator()
    myGenerator.initialize()
    objects = [{"type": "window", "position": [10,10], "size": [1024,512], "text": "Hallo", "color": [12,23,34]},{"type": "button", "name": "einButton", "position": [10,10], "size": [128,64], "text": "Knopf"}]
    myGenerator.writeData(myGenerator.gui_h, myGenerator.generateH("GUI.h", objects, "TGWMainWindow.h"))
    myGenerator.writeData(myGenerator.gui_cpp, myGenerator.generateCpp(objects))
    myGenerator.writeData(myGenerator.event_cpp, myGenerator.generateCppUser(objects))

#,{"type": "button", "name": "einButton", "position": [10,10], "size": [128,64], "text": "Knopf"}