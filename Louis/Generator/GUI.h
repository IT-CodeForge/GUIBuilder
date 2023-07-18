#ifndef _GUI_h_
#define _GUI_h_
#include "TGWMainWindow.h"
#include "TGW_AllClassDeclarations.h"


class GUI : public TGWMainWindow
{
  TGWButton* einButton;
public:
  GUI();
  void loop();
};

#endif