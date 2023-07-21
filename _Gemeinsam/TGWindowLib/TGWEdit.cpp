#include "TGWEdit.h"
#include "UString.h"
#include "TGWMainWindow.h"
#include "UString.h"

TGWEdit::TGWEdit(TGWMainWindow* parent, int posX, int posY, int widh, int height, UString caption, bool scrollMultiline, bool editable)
  : TGWindow( parent, "TGWEdit", posX, posY, widh, height, "TGWEdit")
{
  this->scrollMultiline  = scrollMultiline;
  this->editable         = editable;
  this->captionBuffer    = caption;
}

//https://docs.microsoft.com/en-us/windows/desktop/controls/edit-controls
void TGWEdit::createCustomizedWindow()
{
  DWORD style = WS_CHILD | WS_VISIBLE;
  if (scrollMultiline)
  {
    style = style | WS_VSCROLL | ES_MULTILINE | ES_AUTOVSCROLL| ES_WANTRETURN | ES_OEMCONVERT;
  }

  if (!editable)
  {
    style = style | ES_READONLY;
  }

  myWindowHandle = CreateWindowEx(WS_EX_CLIENTEDGE,
                                  "edit",                        // Predefined class; Unicode assumed // LPCSTR    lpClassName
                                  captionBuffer.c_str(),                                              // Inhalt des Editfeldes / WindowName
                                  style,
                                  posX, posY, width, height,
                                  myParentWindow->getWindowHandle(), // Parent                        // HWND      hWndParent
                                  NULL, // Menu                                                       // HMENU     hMenu
                                  myApplicationHandle,                                                // HINSTANCE hInstance
                                  NULL);                                                              // LPVOID    lpParam
}

/*
void TGWEdit::println(const char* text)
{
  setCaption((UString((char*)getCaption())+text+"\r"+"\n").c_str());
}

void TGWEdit::print(int zahl)
{
  UString s;
  s.addDouble(zahl,0);
  setCaption((UString((char*)getCaption())+s).c_str());
}
*/

void TGWEdit::addText(UString addText)
{
  addText = addText.replace("\n", "\r\n");
  
  setText( getText()+addText );
}

