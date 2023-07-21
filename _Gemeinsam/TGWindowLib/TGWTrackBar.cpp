#include "TGWTrackBar.h"
#include <commctrl.h>
#include "UString.h"
#include "TGWMainWindow.h"

// https://msdn.microsoft.com/en-us/library/windows/desktop/hh298354(v=vs.85).aspx
// https://bobobobo.wordpress.com/2008/02/

// Dev-C++ --> Projekt --> Projekt Optionen --> Parameter --> Linker --> Bibliothek Hinzuf�gen: C:/Programme/MinGW-4.7.1/lib/libcomctl32.a

TGWTrackBar::TGWTrackBar(TGWMainWindow* myParentWindow, int posX, int posY, int width, int height)
  : TGWindow(myParentWindow, "TGWTrackBar", posX, posY, width, height, "TGWTrackBar")
{
}

void TGWTrackBar::createCustomizedWindow()
{
  myWindowHandle = CreateWindow(
                     TRACKBAR_CLASS,                                                 // PREDEFINED CLASS     // LPCSTR    lpClassName
                     captionBuffer.c_str(),                                                                                // LPCSTR    lpWindowName
                     WS_CHILD | WS_VISIBLE | TBS_AUTOTICKS |TBS_HORZ,  // tick marks, horizontal orientation // DWORD     dwStyle
                     posX, posY, width, height,
                     myParentWindow->getWindowHandle(),                                                      // HWND      hWndParent
                     NULL,                                                                                   // HMENU     hMenu
                     myApplicationHandle,                                                                    // HINSTANCE hInstance
                     NULL );                                                                                 // LPVOID    lpParam

  /*
     SendMessage(myWindowHandle, PBM_SETRANGE, true, MAKELPARAM(0, 150));
     SendMessage(myWindowHandle, PBM_SETSTEP, 1, 0 );
     SendMessage(myWindowHandle, TBM_SETPAGESIZE, true, 1);
     SendMessage(myWindowHandle, TBM_SETTICFREQ, true, 0);
     SendMessage(myWindowHandle, TBM_SETPOS, true, 0);
     SendMessage(myWindowHandle, TBM_SETSEL, true, MAKELONG( 1, 5 ) );
  */
}

