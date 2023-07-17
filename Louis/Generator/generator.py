#import intermediary

from dataclasses import replace


class Generator:
    def __init__(self) -> None:
        self.includes = []
        self.gui_h = "GUI.h"
        self.gui_cpp = "GUI.cpp"
        self.event_cpp = "Event.cpp"
        self.gui_h_header = '#ifndef _GUI_h_\n#define _GUI_h_\n\n#include "TGWMainWindow.h"\n#include "TGW_AllClassDeclarations.h"\n\nclass GUI : public TGWMainWindow\n{\n' #WIP
        self.gui_h_footer = 'public:\n  GUI();\n  void loop();\n};\n\n#endif' #WIP
        self.gui_cpp_header = '#include "GUI.h"\n\n#include "TGW_AllClassDefinitions.h"\n#include "SystemAPI.h"\n#include <mmsystem.h>' #WIP
        self.gui_cpp_constructor = '\n\nGUI::GUI()\n  :TGWMainWindow(10, 10, 400, 500, "GUI", 0xFF0000)\n{\n' #WIP
        self.gui_cpp_loop = '\n\nvoid GUI::loop()\n{\n' #WIP
        self.event_cpp_header = '' #WIP
        self.event_cpp_footer = '' #WIP
        self.function_end = '}'
    def writeData(self, file: str, data: str):
        with open(file, "w") as f:
            f.write(data)
    
    def readData(self, file: str) -> str:
        data = ""
        with open(file, "r") as f:
            data = f.read()
        return data
    
    def writeGUIh(self):
        contents = ''
        self.writeData(myGenerator.gui_h, myGenerator.gui_h_header + contents + myGenerator.gui_h_footer)

    def writeGUIcpp(self):
        contents = ""
    
    def getLoopContents(self) -> str:
        prevGuicpp = self.readData(self.gui_cpp)
        loop_start = prevGuicpp.find('void GUI::loop()\n{')
        print(prevGuicpp.replace(prevGuicpp[:(loop_start + 19)], '').replace(prevGuicpp[-1], '').replace(prevGuicpp[-1], ''))
    
    def getMethodContents(self, file:str) -> list[str]:
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
                    methodContents.append(dataGuicpp[t_start_i:i+1])
        return methodContents
    
    def generateHHeader(self, className: str, inheritance: str = '') -> str:
        retstring  = '#ifndef _' + className[:className.find('.')] + '_h_\n'
        retstring += '#define _' + className[:className.find('.')] + '_h_\n'
        retstring += '#include "TGW_AllClassDeclarations.h"\n'
        #Platz für extra includes falls notwendig
        retstring += "\n\nclass " + className[:className.find('.') ]
        if inheritance != "":
            retstring += " : public " + inheritance[:inheritance.find('.')]
        retstring += "\n{\n"
        return retstring


    
if __name__ == "__main__":
    myGenerator = Generator()
    myGenerator.writeData(myGenerator.gui_h, myGenerator.generateHHeader("GUI.h", "TGWMainWindow.h") + myGenerator.gui_h_footer)
    myGenerator.writeData(myGenerator.gui_cpp, myGenerator.gui_cpp_header + myGenerator.gui_cpp_constructor + myGenerator.function_end + myGenerator.gui_cpp_loop + myGenerator.function_end)
    #print(myGenerator.getMethods())
