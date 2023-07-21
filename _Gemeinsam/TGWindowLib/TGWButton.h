#ifndef _TGWButton_h_
#define _TGWButton_h_

#include "TGWindow.h"

class TGWMainWindow;

class TGWButton : public TGWindow
{  
public:
  static const int EV_CLICK        = 0;
  static const int EV_DOUBLECLICK  = 1;
 
  TGWButton(TGWMainWindow* myParentWindow, int posX, int posY, int width, int height, UString caption);
  void createCustomizedWindow();
};

#endif
