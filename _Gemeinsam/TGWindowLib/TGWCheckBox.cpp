#include "TGWCheckBox.h"
#include "TGWMainWindow.h"
#include "Windows.h"

//https://cplusplus.com/forum/windows/40147/

TGWCheckBox::TGWCheckBox(TGWMainWindow* myParentWindow, int posX, int posY, int width, int height, UString caption, bool isChecked)
  :TGWindow(myParentWindow, "TGWCheckBox", posX, posY, width, height, caption)
{
}

TGWCheckBox::~TGWCheckBox()
{
}

bool TGWCheckBox::getChecked()
{
  UINT ckd = IsDlgButtonChecked(myParentWindow->getWindowHandle(), getID()); 
  return (ckd == BST_CHECKED);
}

void TGWCheckBox::createCustomizedWindow()
{
  unsigned long long int hMenuOrID = getID();
  
  myWindowHandle = CreateWindow(
                     TEXT("BUTTON"), // Predefined class
                     captionBuffer.c_str(),
                     WS_VISIBLE | WS_CHILD | BS_CHECKBOX,
                     posX, posY, width, height,       
                     myParentWindow->getWindowHandle(), 
                     (HMENU) hMenuOrID, 
                     myApplicationHandle, 
                     NULL);

	CheckDlgButton(myParentWindow->getWindowHandle(), hMenuOrID, BST_UNCHECKED); // BST_CHECKED
}