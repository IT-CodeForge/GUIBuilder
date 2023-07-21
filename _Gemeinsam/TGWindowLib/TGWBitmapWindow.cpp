#include "TGWBitmapWindow.h"

#include "UString.h"
#include "TGWMainWindow.h"
#include "TGWReflectionObjectListe.h"
#include "SystemAPI.h"
#include "TGWBitmap.h"

TGWBitmapWindow::TGWBitmapWindow(TGWMainWindow* myParentWindow, int posX, int posY, int width, int height)
  : TGWindow(myParentWindow, "TGWBitmapWindow", posX, posY, width, height, "")
{
  theOnePicture = new TGWBitmap();
}

TGWBitmapWindow::~TGWBitmapWindow()
{
  delete theOnePicture;
}

void TGWBitmapWindow::createCustomizedWindow()
{
  unsigned long long int hMenuInt = getID();
  myWindowHandle = CreateWindow(
                     "STATIC",                                  // Predefined class; Unicode assumed  // LPCSTR    lpClassName
                     captionBuffer.c_str(),                                                           // LPCSTR    lpWindowName
                     WS_TABSTOP | WS_VISIBLE | WS_CHILD,                                              // DWORD     dwStyle
                     posX, posY, width, height,
                     myParentWindow->getWindowHandle(),                                               // HWND      hWndParent
                     (HMENU)hMenuInt,                                                                 // HMENU     hMenu
                     myApplicationHandle,                                                             // HINSTANCE hInstance
                     0);
  
  SystemAPI::setTransparency(getWindowHandle(), 0xFF); // Dieser Befehl ist zwingend notwendig. Warum?
                                                       // ist keine Transparenz-Loesung um Bildhintergrund auszublenden
 
  // Vielleicht das? ..WS_EX_TRANSPARENT
  // SetWindowLong(myWindowHandle, GWL_EXSTYLE, GetWindowLong(myWindowHandle, GWL_EXSTYLE) | WS_EX_LAYERED | WS_EX_TRANSPARENT);

}

void TGWBitmapWindow::loadFileToBitmap(UString dateiname)
{
  theOnePicture->loadFromFile(dateiname);
}

void TGWBitmapWindow::paintBitmap(int posX, int posY, bool fitWindowToBitmap, bool transpatent, int tansparantColor)
{ 
  if(fitWindowToBitmap)
  {
    setWindowSize( theOnePicture->getWidth(), theOnePicture->getHeight() );
  }
  
  theOnePicture->paintBitmapToCanvas(this->canvas, posX, posY, transpatent, tansparantColor);
}

