#include "TGWindow.h"
#include "UString.h"
#include "TGWMainWindow.h"
#include "TGWButton.h"
#include "TGWReflectionObjectListe.h"
#include "TGWCanvas.h"
#include "SystemAPI.h"

HINSTANCE TGWindow::myApplicationHandle = 0; // Wird in TGWMainWindow::registerWindowClass initialisiert

TGWindow::TGWindow(TGWMainWindow* myParentWindow, UString className, int posX, int posY, int width, int height, UString caption, int bgColorRRGGBB)
  :TGWReflectionObject(myParentWindow, className)
{
  this->myWindowHandle           = 0; // wird in createWindowSetWindowhandleAndCDC initialisiert
  this->temporaryBackgroundColor = bgColorRRGGBB;
  this->posX                     = posX   ;
  this->posY                     = posY   ;
  this->width                    = width  ;
  this->height                   = height ;
  this->captionBuffer            = caption;
  this->canvas                   = 0;      
  this->myHFont                  = 0;
}

TGWindow::~TGWindow()
{
  if(myHFont             != 0) DeleteObject(myHFont);
  if(canvas              != 0) delete canvas;
}

void TGWindow::createWindowSetWindowhandleAndCDC()
{
  createCustomizedWindow();

  if(myWindowHandle == 0)
  {
    messageBox("Window Creation Failed in TGWindow.cpp:196");
  }
  
  this->canvas = new TGWCanvas(myWindowHandle, temporaryBackgroundColor);   
}

void TGWindow::messageBox(UString message, UString caption)
{
  MessageBox(0, message.c_str(), caption.c_str(), MB_ICONEXCLAMATION | MB_OK | MB_SYSTEMMODAL);
}

int TGWindow::RGB_2_BGR(int col_RRGGBB)
{
  return ((col_RRGGBB & 0x00FF0000)>>16) + (col_RRGGBB & 0x0000FF00) + ((col_RRGGBB & 0x000000FF)<<16);
}

RECT TGWindow::getWindowRectangle()
{
  RECT r;
  GetWindowRect(myWindowHandle, &r);
  return r;
}

RECT TGWindow::getClientRectangle()
{
  RECT r;
  GetClientRect(myWindowHandle, &r);
  return r;
}

RECT TGWindow::getChildRectange(TGWindow* child)
{
  RECT rect = child->getWindowRectangle();

  POINT p;
  POINT q;
  p.x = rect.left;
  p.y = rect.top;
  q.x = rect.right;
  q.y = rect.bottom;

  ScreenToClient(myWindowHandle, &p);
  ScreenToClient(myWindowHandle, &q);

  rect.left   = p.x;
  rect.top    = p.y;
  rect.right  = q.x;
  rect.bottom = q.y;

  return rect;
}

bool TGWindow::checkOnArea(int posX, int posY)
{
  if(this->posX        > posX) return false;
  if(this->posX+width  < posX) return false;
  if(this->posY        > posY) return false;
  if(this->posY+height < posY) return false;
  return true;
}

void TGWindow::toClientPos(int posX, int posY, int & cPosX, int & cPosY)
{
  cPosX = posX - this->posX;
  cPosY = posY - this->posY;
}


int TGWindow::getClientWidth()
{
  RECT r;
  GetClientRect(myWindowHandle, &r);
  return r.right-r.left;
}

int TGWindow::getClientHeight()
{
  RECT r;
  GetClientRect(myWindowHandle, &r);
  return r.bottom-r.top;   
}

int TGWindow::getWidth()
{
  RECT r;
  GetWindowRect(myWindowHandle, &r);
  return r.right-r.left;
}

int TGWindow::getHeight()
{
  RECT r;
  GetWindowRect(myWindowHandle, &r);
  return r.bottom-r.top;   
}

void TGWindow::setWindowRectangle(int x1, int y1, int x2, int y2)
{
  SetWindowPos(myWindowHandle,
               0,
               x1, y1, x2, y2,
               SWP_NOZORDER|SWP_NOACTIVATE);
  posX = x1;
  posY = y1;
  width  = x2-x1;
  height = y2-y1;
}

void TGWindow::setWindowPos(int x1, int y1)
{
  SetWindowPos(myWindowHandle,
               0,
               x1, y1, 0, 0,
               SWP_NOZORDER|SWP_NOACTIVATE|SWP_NOSIZE);
  posX = x1;
  posY = y1;
}

void TGWindow::invalidate(RECT* area, bool eraseBevoreUpdate)
{
  InvalidateRect (myWindowHandle, area, eraseBevoreUpdate);
}

void TGWindow::setCaption(UString caption)
{
  caption = caption.replace("\n", "\r\n");
  this->captionBuffer = caption;	
  SetWindowText(myWindowHandle, caption.c_str());
}

UString TGWindow::getCaption()
{
  int len = GetWindowTextLength(myWindowHandle);
  char* buf = new char[len+2];
  GetWindowText(myWindowHandle, buf, len+1);
  this->captionBuffer = buf;
  delete[] buf;
  return captionBuffer;
}

/*
int TGWindow::getBackgroundColor()
{
  return RGB_2_BGR(GetBkColor(myDeviceContext));
}
*/

//JulianSchueler
void TGWindow::setFont(UString font, int size, bool bold, bool italic, bool underlined, bool strikeOut)
{
  //Get available fonts: EnumFontFamilies()
  int weight = FW_NORMAL;
  if(bold)
    weight = FW_BOLD;

  if(myHFont != 0) DeleteObject(myHFont);
  myHFont = CreateFont( size,      //int cHeight
                              0,         //int cWidth
                              0,         //int cEscapement
                              0,         //int cOrientation
                              weight,    //int cWeight
                              italic,    //DWORD bItalic
                              underlined,//DWORD bUnderline 
                              strikeOut, //DWORD bStrikeOut 
                              DEFAULT_CHARSET,    //DWORD iCharSet 
                              OUT_OUTLINE_PRECIS, //DWORD iOutPrecision 
                              CLIP_DEFAULT_PRECIS,
                              CLEARTYPE_QUALITY,  //DWORD iQuality 
                              DEFAULT_PITCH | FF_DONTCARE, //DWORD iPitchAndFamily 
                              font.c_str() );     //LPCSTR pszFaceName
  
  SendMessage(myWindowHandle, WM_SETFONT, (WPARAM)myHFont, TRUE);
  //SendMessage(myWindowHandle, WM_SETFONT, (LPARAM)GetStockObject(DEFAULT_GUI_FONT), TRUE);
  
}

void TGWindow::setWindowSize(int cx, int cy)
{
  SetWindowPos(myWindowHandle,
               0,
               0, 0, cx, cy,
               SWP_NOZORDER|SWP_NOACTIVATE|SWP_NOMOVE);
  width  = cx;
  height = cy;

  update();
}

void TGWindow::update()
{
  UpdateWindow(myWindowHandle);
}

void TGWindow::setVisible(bool trueFalse)
{
  if (trueFalse==false)
    ShowWindow(myWindowHandle, SW_HIDE);
  else
    ShowWindow(myWindowHandle, SW_SHOW);
}

void TGWindow::setNewBGColorDeleteClientareaAndRepaint(int colRRGGBB)
{
  canvas->setBackgroundColor(colRRGGBB);
  invalidate(0, true); // Beim nächsten paint alles loeschen (mit neuer BK-Farbe) 
  update(); // paint sofort auslösen
  // Recomended code for painting: use:   void eventPaint  (HDC hDeviceContext) {};  
}
