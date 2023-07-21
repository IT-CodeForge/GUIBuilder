#ifndef _TGWindow_h_
#define _TGWindow_h_

/**
Ist fuer Grafik und Handles zustaendig
**/

#include <windows.h>

#include "TGWReflectionObject.h"
#include "UString.h"

class TGWMainWindow;
class TGWCanvas;

class TGWindow : public TGWReflectionObject
{
  friend TGWMainWindow;

protected:
  static HINSTANCE myApplicationHandle;
  int              temporaryBackgroundColor;

  HWND             myWindowHandle;
  UString          captionBuffer; 

  int posX;
  int posY;
  int width;
  int height;
  
  virtual void createCustomizedWindow()=0;

public:
  TGWCanvas* canvas;
  HFONT            myHFont;
  void createWindowSetWindowhandleAndCDC();

  TGWindow(TGWMainWindow* myParentWindow, UString className, int posX, int posY, int width, int height, UString caption="", int colorRRGGBB=0x888888);
  virtual ~TGWindow();

  UString getClassName()
  {
    return className;
  };

  static void messageBox(UString message, UString caption="Message");

  HWND getWindowHandle()
  {
    return myWindowHandle;
  };

  void setCaption(UString caption);
  UString getCaption();

  RECT getWindowRectangle();
  RECT getClientRectangle();
  RECT getChildRectange(TGWindow* child);

  int  getClientWidth();
  int  getClientHeight();
  int  getWidth();
  int  getHeight();

  void setWindowRectangle(int x1, int y1, int x2, int y2);
  void setWindowSize(int cx, int cy);
  void setWindowPos(int x1, int y1);
  bool checkOnArea(int posX, int posY);
  void toClientPos(int posX, int posY, int & cPosX, int & cPosY);

  void setVisible(bool trueFalse);

  int RGB_2_BGR(int col_RRGGBB);  //Color-Conversion

  void invalidate(RECT* area=0, bool eraseBevoreUpdate=false);// Repaint/update invalidArea on next PAINT-event; area==0 --> whole client area 
  void update();                     // Repaint the whole clientrectangle at once (blocking call) 

  void setFont(UString font = "MS Shell Dlg",
                   int size = 16, 
                  bool bold = false, 
                bool italic = false, 
            bool underlined = false, 
             bool strikeOut = false);  

  void setNewBGColorDeleteClientareaAndRepaint(int colRRGGBB);
};

#endif
