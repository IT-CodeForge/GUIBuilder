#ifndef _TGWBitmapWindow_h_
#define _TGWBitmapWindow_h_

#include "TGWindow.h"

class TGWMainWindow;
class TGWBitmap;

class TGWBitmapWindow :public TGWindow
{
  TGWBitmap* theOnePicture;

public:
  TGWBitmapWindow(TGWMainWindow* myParentWindow, int posX, int posY, int width, int height);
  ~TGWBitmapWindow();

  void createCustomizedWindow();
  void loadFileToBitmap(UString dateiname); // A very simple implementation. For more features use WinGdiBitmap..
  void paintBitmap(int posX=0, int posY=0, bool fitWindowToBitmap = true, bool transpatent = false, int tansparantColor = 0x000000);     // A very simple implementation. 
};

#endif
