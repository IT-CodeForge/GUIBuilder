#include "TGWButton.h"
#include "UString.h"
#include "TGWMainWindow.h"

// https://msdn.microsoft.com/en-us/library/windows/desktop/hh298354(v=vs.85).aspx

TGWButton::TGWButton(TGWMainWindow* myParentWindow, int posX, int posY, int width, int height, UString caption)
  : TGWindow(myParentWindow, "TGWButton", posX, posY, width, height, caption)
{
}

void TGWButton::createCustomizedWindow()
{
  unsigned long long int hMenuInt = getID();
  myWindowHandle = CreateWindow(
                     "BUTTON",                                   // Predefined class; Unicode assumed  // LPCSTR    lpClassName
                     captionBuffer.c_str(),                                                            // LPCSTR    lpWindowName
                     WS_TABSTOP | WS_VISIBLE | WS_CHILD | BS_DEFPUSHBUTTON | BS_NOTIFY,                            // DWORD     dwStyle
                     posX, posY, width, height,
                     myParentWindow->getWindowHandle(),                                                // HWND      hWndParent
                     (HMENU)hMenuInt,                                                                  // HMENU     hMenu
                     myApplicationHandle,                                                              // HINSTANCE hInstance
                     0);                                                                               // LPVOID    lpParam
}

