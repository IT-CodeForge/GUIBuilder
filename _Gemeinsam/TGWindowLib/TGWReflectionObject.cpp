#include "TGWReflectionObject.h"
#include "TGWMainWindow.h"

int TGWReflectionObject::nextID = TGWRO_START_ID;

TGWReflectionObject::TGWReflectionObject(TGWMainWindow* myParentWindow, UString className)
{
  this->myParentWindow = myParentWindow;
  this->className = className;
  myID = nextID++;
  creationCompleted = false;

  if (	myParentWindow != 0)
  {
    myParentWindow->addChildObject(this);
  }
}

UString TGWReflectionObject::getClassName()
{
  return className;
}

int TGWReflectionObject::getID()
{
  return myID;
}


