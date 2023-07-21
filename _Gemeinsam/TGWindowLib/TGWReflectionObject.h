#ifndef _TGWReflectionObject_h_
#define _TGWReflectionObject_h_
#include "UString.h"

#define TGWRO_START_ID 100

class TGWMainWindow;

class TGWReflectionObject
{
protected:
  UString      className;
  TGWMainWindow*   myParentWindow;

  static int   nextID;
  int          myID;

public:
  bool         creationCompleted;
  TGWReflectionObject(TGWMainWindow* myParentWindow, UString className);
  virtual ~TGWReflectionObject(){};

  UString getClassName();
  int getID();
  virtual void eventCreated(){}; // Now this (if hase one) and all other windows handle exist
};

#endif
