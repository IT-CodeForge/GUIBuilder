#ifndef _TGWEdit_h_
#define _TGWEdit_h_

#include "TGWindow.h"
#include "UString.h"

class TGWMainWindow;

class TGWEdit : public TGWindow
{
protected:
  bool editable;
  bool scrollMultiline;
public:
  TGWEdit(TGWMainWindow* parent, int posX, int posY, int widh, int height, UString caption = "", bool scrollMultiline = true, bool editable = true);
  void createCustomizedWindow();
  void setText(UString t){setCaption(t);};
  UString getText(){return getCaption();};
  void addText(UString t);
  //void println(const char* text);
  //void print(int zahl);
};

#endif
