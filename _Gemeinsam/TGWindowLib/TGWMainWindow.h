#ifndef _TGWMainWindow_h_
#define _TGWMainWindow_h_

/**
Diese Klasse implementiert zwei Dinge:
1. Den Message-Handler der Applikation in eventXXX-Aufrufe umsetzen.
2. Eine Liste mit den Client-Fenstern. //!Wird noch nicht benutzt!//
Da es nur eine Applikation gibt darf diese Klasse nur ein mal Instanziert werden.
Eine Mehrfachinstanzierung w�rde zu einer falschen Verzeigerung f�hren,
da mit dem zweiten Fenster der Zeiger f�r den Messagehandler nicht mehr auf
das erste Fenster Zeigen w�rde.
**/

#include "TGWindow.h"

class TGWReflectionObject;
class TGWBitmap;
class TGWButton;
class TGWCheckBox;
class TGWEdit;
class TGWReflectionObjectListe;

class TGWMainWindow : public TGWindow
{
  friend TGWReflectionObject;

private:
  int  actualMousePosX;
  int  actualMousePosY;

  void createUncreatedChildWindows();

protected:
  PAINTSTRUCT               paintStructWMPaint;
  static TGWMainWindow*     theOnlyMainWindow;
  TGWReflectionObjectListe* dieReflectionObjectListe;
  bool                      hasNonecreatedObjects;


  virtual void createCustomizedWindow();
  virtual void registerWindowClass(WNDCLASSEX &windowExtendedParameter);
          void eventControl(HWND hControlWindow, int controlID, int notificationCode, TGWReflectionObject* obj);

public:
  static LRESULT CALLBACK windowMessageCallbackMethod(HWND h_MainWindow_MessageTarget, UINT Message, WPARAM wParam, LPARAM lParam);
  LRESULT                 objectMessageCallbackMethod(HWND h_MainWindow_MessageTarget, UINT Message, WPARAM wParam, LPARAM lParam);

  TGWMainWindow(int posX, int posY, int width, int height, UString caption="Main Window", int colorRRGGBB=0xAAAAAA);
  virtual ~TGWMainWindow();

  int run(              // Blocking call until exit
    HINSTANCE          theApplicationHandle,
    int                nCmdShow
  );

  void addChildObject(TGWReflectionObject* theNewChild);
  TGWindow* checkAffectedWindow(int posX, int posY);

  //virtual void eventCreate () {};  // After creation of all main- and clientwindows, bevore show.
//  virtual void eventShow   (bool firstTime, bool showHide) {}; // Complex version...not used with normal windows.
  virtual void eventShow   () {};  // Simple version
  virtual void eventPaint  (HDC hDeviceContext) {};
  virtual void eventDestroy() {};
  virtual bool eventClose  (){return true; /* No close if returns false */};
  virtual void eventResize() {};
  virtual void eventKeyUp  (unsigned char virtualKeyCode){}; //https://learn.microsoft.com/de-de/windows/win32/inputdev/virtual-key-codes
  virtual void eventKeyDown(unsigned char virtualKeyCode){}; //https://learn.microsoft.com/de-de/windows/win32/inputdev/virtual-key-codes

  virtual void eventButton(TGWButton* einButton, int event) {};
  virtual void eventCheckBox(TGWCheckBox* eineCheckBox, int isChecked_1_0) {};
  virtual void eventTimer  (int id) {};
  virtual void eventMouseMove(int posX, int posY){};
  virtual void eventMouseClick(int posX, int posY, TGWindow* affectedWindow){};
  virtual void eventEditChanged(TGWEdit* einEdit);
  virtual void eventClient(){};
};

#endif

