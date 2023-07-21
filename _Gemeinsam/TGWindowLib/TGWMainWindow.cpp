#include "TGWMainWindow.h"
#include "TGWReflectionObjectListe.h"
#include "UString.h"
#include "TGWEdit.h"
#include "TGWButton.h"
#include "TGWCheckBox.h"
#include "TGWCanvas.h"

#ifdef _LOG_TGWMainWindow_
#include "UStringListe2DExt.h"
#include "Log.h"
UStringListe2DExt wMessages;
#endif

TGWMainWindow *TGWMainWindow::theOnlyMainWindow;

TGWMainWindow::TGWMainWindow(int posX, int posY, int width, int height, UString caption, int colorRRGGBB)
    : TGWindow(0, "TGWMainWindow", posX, posY, width, height, caption, colorRRGGBB)
{
  theOnlyMainWindow = this;
  dieReflectionObjectListe = new TGWReflectionObjectListe();
  hasNonecreatedObjects    = false;
  actualMousePosX = 0;
  actualMousePosY = 0;
  
  #ifdef _LOG_TGWMainWindow_
  bool success = wMessages.readFromFile("..\\TGWindowLib\\WM_Messages.csv");
  if (!success)
    messageBox("WM_XX Liste failed!");
  #endif
}

TGWMainWindow::~TGWMainWindow()
{
  delete dieReflectionObjectListe;
}

LRESULT CALLBACK TGWMainWindow::windowMessageCallbackMethod(HWND h_MainWindow_MessageTarget, UINT Message, WPARAM wParam, LPARAM lParam)
{
  return theOnlyMainWindow->objectMessageCallbackMethod(h_MainWindow_MessageTarget, Message, wParam, lParam);
}

//https://docs.microsoft.com/en-us/windows/desktop/learnwin32/writing-the-window-procedure
//http://www.winprog.org/tutorial/window_click.html
LRESULT TGWMainWindow::objectMessageCallbackMethod(HWND h_MainWindow_MessageTarget, UINT Message, WPARAM wParam, LPARAM lParam)
{
  // h_MainWindow_MessageTarget
  // Not all Mesages are exclusively for this Main Window.

  if (myWindowHandle != h_MainWindow_MessageTarget)
  {
  }

  switch (Message)
  {
  case WM_PARENTNOTIFY:
  {
    // IsDlgButtonChecked(
    eventClient();
  }
  break; //----------------------------------------------------------------------
  case WM_LBUTTONDOWN:
  {
    TGWindow *affectedWindow = checkAffectedWindow(actualMousePosX, actualMousePosY);

    eventMouseClick(actualMousePosX, actualMousePosY, affectedWindow);
  }
  break; //----------------------------------------------------------------------
  case WM_MOUSEMOVE:
  {
    actualMousePosX = lParam & 0xFFFF;
    actualMousePosY = (lParam & 0xFFFF0000) >> 16;
    eventMouseMove(actualMousePosX, actualMousePosY);
  }
  break; //----------------------------------------------------------------------
  case WM_KEYUP:
  {
    eventKeyUp(wParam);
  }
  break; //----------------------------------------------------------------------
  case WM_KEYDOWN:
  {
    eventKeyDown(wParam);
  }
  break; //----------------------------------------------------------------------
  case WM_COMMAND:
  {
    //https://docs.microsoft.com/en-us/windows/desktop/menurc/wm-command
    HWND hControlWindow = (HWND)lParam;

    if (hControlWindow == 0) //////////// Messagesource = Menu or Accelerator
    {
      int menu0_accellerator1 = HIWORD(wParam);
      if (menu0_accellerator1 == 0)
      {
        //int menuID = LOWORD(wParam);
        //eventMenue(...)
      }
      else
      {
        //int accelID = LOWORD(wParam);
        //eventAccelerator(...)
      }
    }
    else ///////////////////////////// Messagesource = Control
    {
      int controlID = LOWORD(wParam);
      int notificationCode = HIWORD(wParam);

      TGWReflectionObject *obj;
      for (int i = 0; i < dieReflectionObjectListe->size(); i++)
      {
        obj = dieReflectionObjectListe->at(i);
        if (obj->getID() == controlID)
        {
          break;
        }
      }

      eventControl(hControlWindow, controlID, notificationCode, obj);
    }
  }
  break;              //----------------------------------------------------------------------
  case WM_SHOWWINDOW: //Die WM_SHOWWINDOW Nachricht wird nicht gesendet wenn das SW_SHOWNORMAL-Flag im Aufruf der Funktion ShowWindow angegeben wird!
  {
    // Wir bei "normalen" Fenstern niemals gebraucht --> eventShow wird in "run(..)" nach dem ersten Anzeigen des Fenstern aufgerufen.
    /*
      if(!showFirstTime)
        eventShow(false, (wParam  == true));
      */
  }
  break;          //----------------------------------------------------------------------
  case WM_CREATE: // Only the MainWindow receives this message after the window is created, but before the window becomes visible.
  {
    // ** is handled in this->run(..) **

    //myWindowHandle = h_MainWindow_MessageTarget;
    //return eventCreateMainWindow((LPCREATESTRUCT)lParam);
    return 0; // If return -1 the window is destroyed
  }
  break; //----------------------------------------------------------------------
  case WM_TIMER:
  {
    eventTimer((int)wParam);
  }
  break; //----------------------------------------------------------------------
  case WM_PAINT:
  {
    HDC hdeviceContext = BeginPaint(myWindowHandle, &paintStructWMPaint);
    eventPaint(hdeviceContext);
    EndPaint(myWindowHandle, &paintStructWMPaint);
  }
  break; //----------------------------------------------------------------------
  case WM_CLOSE:
  {
    if (eventClose() == true)
    {
      DestroyWindow(h_MainWindow_MessageTarget);
    }
  }
  break; //----------------------------------------------------------------------
  case WM_DESTROY:
  {
    eventDestroy();
    PostQuitMessage(0); // Applikation beenden
  }
  break; //----------------------------------------------------------------------
  case WM_EXITSIZEMOVE:
  {
    eventResize();
  }
  break; //----------------------------------------------------------------------
  default:
  {
#ifdef _LOG_TGWMainWindow_
    int zeilennummer = wMessages.searchRelatedY(0, UString(Message));
    UString WM_text = wMessages.getAt(1, zeilennummer);
    Log::out(WM_text);
#endif
    // Default Windows Processing for unhandled Messages
    return DefWindowProc(h_MainWindow_MessageTarget, Message, wParam, lParam);
  }
  }
  return 0;
}

TGWindow *TGWMainWindow::checkAffectedWindow(int posX, int posY)
{
  TGWReflectionObject *aktuellesReflectionObject;
  TGWindow *aktuellesFenster;
  int max = dieReflectionObjectListe->size();
  for (int i = 0; i < max; i++)
  {
    aktuellesReflectionObject = dieReflectionObjectListe->at(i);

    if (aktuellesReflectionObject->getClassName() != "TGWTimer")
    {
      aktuellesFenster = (TGWindow *)aktuellesReflectionObject;
      if (aktuellesFenster->checkOnArea(posX, posY))
        return aktuellesFenster;
    }
  }
  return 0;
}

int TGWMainWindow::run(HINSTANCE theApplicationHandle, int nCmdShow)
{
  myApplicationHandle = theApplicationHandle;

  WNDCLASSEX windowExtendedParameter;
  {
    windowExtendedParameter.hInstance = myApplicationHandle;
    windowExtendedParameter.lpfnWndProc = TGWMainWindow::windowMessageCallbackMethod;
  }

  registerWindowClass(windowExtendedParameter); // Register the callback methot to the application.

  // Create this mainwindow
  createWindowSetWindowhandleAndCDC(); // effects message WM_CREATE bevore winHandle is set

  createUncreatedChildWindows();
  eventCreated(); // Now this (if hase one) and all other windows handle exist

  ShowWindow(myWindowHandle, nCmdShow);
  // eventShow(true, true);  // first time, show not hide.

  eventShow(); // Vereinfachte Variante für "normale" Fenster
  update();

  //MessageLoop
  MSG message;
  {
    while (GetMessage(&message, NULL, 0, 0)) //Blocking call, false if WM_QUIT
    {
      createUncreatedChildWindows();
      TranslateMessage(&message);
      DispatchMessage(&message);
    }
  }

  return message.wParam; // The exit code of WM_QUIT
}  // end run()

void TGWMainWindow::createUncreatedChildWindows()
{
  if(!hasNonecreatedObjects) return;
  // Create all child Windows (added in constructor of derived window)
  TGWReflectionObject *aktuellesReflectionObject;
  int max = dieReflectionObjectListe->size();
  TGWindow* aktuellesWindow;
  for (int i = 0; i < max; i++)
  {
    aktuellesReflectionObject = dieReflectionObjectListe->at(i);
    if(aktuellesReflectionObject->creationCompleted==false)
    {
      if (aktuellesReflectionObject->getClassName() != "TGWTimer")
      {
        aktuellesWindow = (TGWindow*)aktuellesReflectionObject;
        aktuellesWindow->createWindowSetWindowhandleAndCDC(); //First point where the Object has a window handle.
      }
    }
  }

  for (int i = 0; i < max; i++)
  {
    aktuellesReflectionObject = dieReflectionObjectListe->at(i);
    if(aktuellesReflectionObject->creationCompleted==false)
    {
      aktuellesReflectionObject->eventCreated(); // Now this (if hase one) and all other windows handle exist
      aktuellesReflectionObject->creationCompleted = true;
    }
  }

  hasNonecreatedObjects = false;
}

void TGWMainWindow::registerWindowClass(WNDCLASSEX &windowExtendedParameter)
{
  //http://www.functionx.com/win32/Lesson01b.htm
  windowExtendedParameter.cbSize = sizeof(WNDCLASSEX);
  windowExtendedParameter.cbClsExtra = 0; // Allokiere keine zus�tzlichen bytes f�r die Instanz
  windowExtendedParameter.cbWndExtra = 0; // Allokiere keine zus�tzlichen bytes f�r das Fenster
  windowExtendedParameter.style = 0;
  //   windowExtendedParameter.hIcon       = LoadIcon(0, "big.ico"  );
  //   windowExtendedParameter.hIcon       = LoadIcon(NULL, IDI_APPLICATION);
  windowExtendedParameter.hIcon = LoadIcon(NULL, IDI_WINLOGO);
  windowExtendedParameter.hIconSm = LoadIcon(0, "small.ico");
  //   windowExtendedParameter.hIconSm     = LoadIcon(NULL, IDI_APPLICATION); // Standardicon laden
  windowExtendedParameter.hCursor = LoadCursor(NULL, IDC_ARROW);
  //   windowExtendedParameter.hbrBackground = CreateSolidBrush(ARGB_2_ABGR(0x00FFFF));
  //   windowExtendedParameter.hbrBackground = (HBRUSH)COLOR_HIGHLIGHT;
  windowExtendedParameter.hbrBackground = (HBRUSH)(COLOR_BTNFACE + 1);
  //   windowExtendedParameter.hbrBackground = GetStockObject(0x01);
  windowExtendedParameter.lpszMenuName = 0;
  windowExtendedParameter.lpszClassName = "TGWMainWindow";

  if (!RegisterClassEx(&windowExtendedParameter))
  {
    myWindowHandle = 0;
  }
}

// https://msdn.microsoft.com/en-us/library/windows/desktop/ms633575(v=vs.85).aspx
void TGWMainWindow::createCustomizedWindow()
{
  myWindowHandle = CreateWindowEx(
      WS_EX_CLIENTEDGE,      // DWORD     dwExStyle
      "TGWMainWindow",       // LPCSTR    lpClassName
      captionBuffer.c_str(), // LPCSTR    lpWindowName
      WS_OVERLAPPEDWINDOW,   // DWORD     dwStyle
      posX, posY, width, height,
      NULL,                // HWND      hWndParent
      NULL,                // HMENU     hMenu
      myApplicationHandle, // HINSTANCE hInstance
      NULL);               // LPVOID    lpParam
}

void TGWMainWindow::addChildObject(TGWReflectionObject *theNewChild)
{
  dieReflectionObjectListe->push_back(theNewChild);
  hasNonecreatedObjects = true;
}

void TGWMainWindow::eventControl(HWND hControlWindow, int controlID, int notificationCode, TGWReflectionObject *obj)
{
  if (obj->getClassName() == "TGWButton")
  {
    /*
      #define BN_CLICKED 0
      #define BN_PAINT 1
      #define BN_HILITE 2
      #define BN_UNHILITE 3
      #define BN_DISABLE 4
      #define BN_DOUBLECLICKED 5
      #define BN_PUSHED BN_HILITE
      #define BN_UNPUSHED BN_UNHILITE
      #define BN_DBLCLK BN_DOUBLECLICKED
      #define BN_SETFOCUS 6
      #define BN_KILLFOCUS 7
    */

    TGWButton *einButton = (TGWButton *)obj;
    if (notificationCode == BN_CLICKED)
      eventButton(einButton, TGWButton::EV_CLICK);
    if (notificationCode == BN_DOUBLECLICKED)
      eventButton(einButton, TGWButton::EV_DOUBLECLICK);
  }
  else if (obj->getClassName() == "TGWCheckBox")
  {
    TGWCheckBox *eineCheckbox = (TGWCheckBox *)obj;

    notificationCode = IsDlgButtonChecked(myWindowHandle, controlID);
    if (notificationCode == 1)
    {
      CheckDlgButton(myWindowHandle, controlID, BST_UNCHECKED);
    }
    else
    {
      CheckDlgButton(myWindowHandle, controlID, BST_CHECKED);
    }

    eventCheckBox(eineCheckbox, 1 - notificationCode);
  }
  else if (obj->getClassName() == "TGWEdit")
  {
    TGWEdit* einEdit = (TGWEdit *)obj;

    if (notificationCode == EN_CHANGE)
    {
      eventEditChanged(einEdit);
    }
  }
}

