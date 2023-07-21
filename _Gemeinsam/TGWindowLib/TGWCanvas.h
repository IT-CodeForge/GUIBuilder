#ifndef _TGWCanvas_h_
#define _TGWCanvas_h_

#include <windows.h>
#include "UString.h"

class TGWCanvas
{
private:
  HDC              myDeviceContext;
  HWND             myWindowHandle;
  HBRUSH           backgroundColorBrush;
  int              backGroundColor;
   
public:
  HBRUSH           paintBrush;
  HPEN             paintPen;

public:
  TGWCanvas(HWND windowHandle, int bgColorRRGGBB);
  virtual ~TGWCanvas();
  HDC  getDeviceContext(){return myDeviceContext;};
  void setBackgroundColor(int col_RRGGBB); // Sets the color canvas, of textField background and other.
  void setPaintBrush(int colorRRGGBB);
  void setPaintPen  (int colorRRGGBB, int lineWidth=1);
  
  // The following in client-Coordinates:
  void clearRectangle(RECT & rect);
  void clearRectangle(int x1, int y1, int x2, int y2);
  void drawRectangle(int x1, int y1, int x2, int y2);
  void drawEllipse(int x1, int y1, int x2, int y2);
  void moveTo(int x1, int y1);
  void lineTo(int x1, int y1);
  void textOut(int x1, int y1, UString text);
};

#endif