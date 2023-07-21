#ifndef _TGWTimer_h_
#define _TGWTimer_h_

#include "TGWReflectionObject.h"

class TGWMainWindow;

class TGWTimer : public TGWReflectionObject
{
  bool waitForWinHandle;
  TGWMainWindow* myMessageHandlerWindow;
  int intervallMilliSeconds;

public:
  TGWTimer(TGWMainWindow* messageHandlerWindow, int intervallMilliSeconds=0, int* id = 0);
  int start(int intervallMilliSeconds);
  void stop();
  int  getID();
  void eventCreated();  // Now this (if hase one) and all other windows handle exist
};

#endif
