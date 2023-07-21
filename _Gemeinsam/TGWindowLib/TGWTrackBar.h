#ifndef _TGWTrackBar_h_
#define _TGWTrackBar_h_

#include "TGWindow.h"

class TGWMainWindow;

class TGWTrackBar : public TGWindow
{
public:
  TGWTrackBar(TGWMainWindow* myParentWindow, int posX, int posY, int width, int height);
  void createCustomizedWindow();
};

#endif
