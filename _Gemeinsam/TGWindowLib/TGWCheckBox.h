#ifndef _TGBCheckBox_h_
#define _TGBCheckBox_h_

#include "TGWindow.h"

class TGWCheckBox : public TGWindow
{
public:
  TGWCheckBox(TGWMainWindow* myParentWindow, int posX, int posY, int width, int height, UString caption, bool isChecked=false);
  virtual ~TGWCheckBox();
  void createCustomizedWindow();
  bool getChecked();
};

#endif