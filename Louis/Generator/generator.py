#import intermediary


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
        self.typeTranslation = {"button": "TGWButton",
                                "window": "TGWMainWindow"}

                                



    def initialize(self):
        try:
            self.readData(self.gui_h)
            self.readData(self.gui_cpp)
            self.readData(self.event_cpp)
        except:
            self.writeData(self.gui_h, "File initialize, if you read this somthing has gone terribly wrong")
            self.writeData(self.gui_cpp, "File initialize, if you read this somthing has gone terribly wrong")
            self.writeData(self.event_cpp, "")
    
    def updateFiles(self, objects: list[dict[str, any]]):
        self.writeData(self.gui_h, self.generateH("GUI.h", objects, "TGWMainWindow.h"))
        self.writeData(self.gui_cpp, self.generateCpp(objects))
        self.writeData(self.event_cpp, self.generateCppUser(objects))
    




    def writeData(self, file: str, data: str):
        with open(file, "w") as f:
            f.write(data)
    
    def readData(self, file: str) -> str:
        data = ""
        with open(file, "r") as f:
            data = f.read()
        return data
        




    def hexColorConverter(self, num: int) -> str:
        hexNum = hex(num).lstrip("0x")[:2]
        while len(hexNum) < 2:
            hexNum = "0" + hexNum
        return hexNum[:2]
    
    def getMethodContents(self, stringFile:str) -> list[list[str,int,int]]:
        methodContents = []
        level = 0
        t_start_i = 0
        for i, char in enumerate(stringFile):
            if char == "{":
                if level == 0:
                    t_start_i = i
                level += 1
            elif char == "}":
                level -= 1
                if level == 0:
                    methodContents.append([stringFile[t_start_i:i+1], t_start_i, i+1])
        return methodContents





    def checkUserIncludes(self, objects: list[dict[str, any]]) -> str:
        retStr = ""
        uniqueTypeList = []
        for object in objects:
            if object["type"] == "button" and "button" not in uniqueTypeList:
                uniqueTypeList.append("button")
        
        for type in uniqueTypeList:
            retStr += '#include "' + self.typeTranslation[type] + '"\n'
        return retStr
    
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
        retStr += '  void eventButton(TGWButton* einButton, int event);\n'
        retStr += 'private:\n'
        for object in objects:
            if object["type"] == "window":
                continue
            retStr += "  void event_" + object["name"] + "(int event);\n"
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
            retStr += "  if(einButton == this->" + object["name"] + ")\n  {\n"
            retStr += "    event_" + object["name"] + "(event);\n  }\n"
        retStr += self.function_end + "\n"
        return retStr
    
    def generateCppUser(self, objects: list[dict[str, any]]) -> str:
        retStr = self.readData(self.event_cpp)
        if retStr.find('#include "GUI.h"\n\n') != -1:
            retStr = retStr.replace(retStr[:retStr.find('#include "GUI.h"\n\n') + 18], "")
        retStr = self.checkUserIncludes(objects) + '#include "GUI.h"\n\n' + retStr
        alreadyAddedEvents = []
        offset = 0
        tempStr = retStr
        while tempStr.find("void GUI::event_") != -1:
            startIndex = tempStr.find("void GUI::event_")
            endIndex   = self.getMethodContents(tempStr[startIndex:])[0][2]
            eventName  = tempStr[startIndex + 16:tempStr.find("(", startIndex)]
            isInList   = False
            for object in objects:
                if object["type"] == "window":
                    continue
                if eventName == object["name"]:
                    isInList = True
                    alreadyAddedEvents.append(eventName)
            if not isInList:
                retStr = retStr.replace(retStr[startIndex:endIndex + startIndex + 2], "")
            tempStr = tempStr[startIndex + 16:]
            offset += startIndex

        for object in objects:
            if object["type"] == "window":
                continue
            if object["name"] not in alreadyAddedEvents:
                retStr += "void GUI::event_" + object["name"] + "(int event)\n{\n}\n\n"
        
        loopcontent = ""
        start = retStr.find("void GUI::loop()")
        if start != -1:
            loopcontent = self.getMethodContents(retStr[start:])[0][0].lstrip("{\n").rstrip("}\n")
            end   = self.getMethodContents(retStr[start:])[0][2] + start + 2
            retStr = retStr.replace(retStr[start:end], "")
        retStr += "void GUI::loop()\n{\n" + loopcontent + "}\n\n"
        
        return retStr


        


    
if __name__ == "__main__":
    myGenerator = Generator()
    myGenerator.initialize()
    objects = [{"type": "window", "position": [10,10], "size": [1024,512], "text": "Hallo", "color": [12,23,34]}]
    myGenerator.updateFiles(objects)
    tempStr = "test\n123\n void event_meinButton(var1 var2)\n{print(hallo)}"

#,{"type": "button", "name": "einButton", "position": [10,10], "size": [128,64], "text": "Knopf"},{"type": "button", "name": "einButton2", "position": [10,30], "size": [128,64], "text": "Knopf2"}