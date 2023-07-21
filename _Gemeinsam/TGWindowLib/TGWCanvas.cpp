#include "TGWCanvas.h"
#include "SystemAPI.h"

TGWCanvas::TGWCanvas(HWND windowHandle, int bgColorRRGGBB)
{
  myWindowHandle = windowHandle;
  myDeviceContext = GetDC(myWindowHandle);
  setBackgroundColor(bgColorRRGGBB);
  this->paintPen             = 0;
  this->paintBrush           = 0;
}

TGWCanvas::~TGWCanvas()
{
  if (paintBrush          != 0) DeleteObject(paintBrush);
  if (backgroundColorBrush!= 0) DeleteObject(backgroundColorBrush);
  ReleaseDC(myWindowHandle, myDeviceContext); myDeviceContext = 0;
}

// paint example
// https://msdn.microsoft.com/en-us/library/windows/desktop/dd145184(v=vs.85).aspx
// https://learn.microsoft.com/en-us/windows/win32/gdi/creating-colored-pens-and-brushes
// https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-ellipse
void TGWCanvas::drawRectangle(int x1, int y1, int x2, int y2)
{
  Rectangle(myDeviceContext, x1, y1, x2, y2);
}

void TGWCanvas::drawEllipse(int x1, int y1, int x2, int y2)
{
  Ellipse(myDeviceContext, x1, y1, x2, y2);
}

void TGWCanvas::setPaintBrush(int colorRRGGBB)
{
  if(paintBrush != 0) DeleteObject(paintBrush);
  paintBrush = CreateSolidBrush(RGB( (colorRRGGBB & 0xFF0000)>>16, (colorRRGGBB & 0xFF00)>>8, colorRRGGBB & 0xFF ) );
  SelectObject(myDeviceContext, paintBrush);
}

void TGWCanvas::setPaintPen(int colorRRGGBB, int lineWidth)
{
  if(paintPen != 0) DeleteObject(paintPen);
  paintPen = CreatePen(PS_SOLID, lineWidth, RGB( (colorRRGGBB & 0xFF0000)>>16, (colorRRGGBB & 0xFF00)>>8, colorRRGGBB & 0xFF ) );
  SelectObject(myDeviceContext, paintPen);
}

void TGWCanvas::lineTo(int x1, int y1)
{
  LineTo(myDeviceContext, x1, y1);
}

void TGWCanvas::moveTo(int x1, int y1)
{
  MoveToEx(myDeviceContext, x1, y1,0);
}

void TGWCanvas::textOut(int x, int y, UString text)
{
  // See SetTextAlign - function

  ExtTextOutA(
    myDeviceContext,
    x,
    y,
    ETO_OPAQUE,   //options,
    0,   //pRect 
    text.c_str(),
    text.length(),  
    0);  // *lpDx
}

void TGWCanvas::setBackgroundColor(int col_RRGGBB)
{
  backGroundColor = col_RRGGBB;
   if (backgroundColorBrush != 0)
    DeleteObject(backgroundColorBrush);
  backgroundColorBrush = CreateSolidBrush(SystemAPI::intRRGGBB_to_systemRGB(backGroundColor));

  // Set the canvas background:
  // See https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setclasslongptra
  SetClassLongPtr(myWindowHandle, GCLP_HBRBACKGROUND, (LONG_PTR)backgroundColorBrush);

  // Set the background for several GUI-elements:
  // See https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-setbkcolor
  SetBkColor(myDeviceContext, SystemAPI::intRRGGBB_to_systemRGB(col_RRGGBB));
}

void TGWCanvas::clearRectangle(RECT & rect)
{
  FillRect(myDeviceContext, &rect, (HBRUSH)(COLOR_WINDOW + 1));
}

void TGWCanvas::clearRectangle(int x1, int y1, int x2, int y2)
{
  RECT rect;
  rect.left   = x1>x2?x2:x1;
  rect.right  = x1>x2?x1:x2;
  rect.top    = y1>y2?y1:y2;
  rect.bottom = y1>y2?y2:y1;
  clearRectangle(rect);
}