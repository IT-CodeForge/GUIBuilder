#include "GUI.h"
#include "TGW_AllClassDefinitions.h"


GUI::GUI()
  :TGWMainWindow(10, 10, 1024, 512, "Hallo", 0x0c1722)
{
  einButton = new TGWButton(this, 10, 10, 128, 64, "Knopf");
}
