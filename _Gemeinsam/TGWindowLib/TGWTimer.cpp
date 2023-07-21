#include "TGWTimer.h"
#include "TGWMainWindow.h"

TGWTimer::TGWTimer(TGWMainWindow* messageHandlerWindow, int intervallMilliSeconds, int* id)
  :TGWReflectionObject(messageHandlerWindow, "TGWTimer")
{
  if(id!=0) *id = myID;

  myMessageHandlerWindow = messageHandlerWindow;

  waitForWinHandle = false; // Handle this on start timer!

  this->intervallMilliSeconds = 0; // Not running yet
  if(intervallMilliSeconds!=0) start(intervallMilliSeconds); // uses this->intervallMilliSeconds
}

int TGWTimer::start(int intervallMilliSeconds)
{
  HWND messageHandle = myMessageHandlerWindow->getWindowHandle();

  if( messageHandle==0 )
  {
    waitForWinHandle = true;
    this->intervallMilliSeconds = intervallMilliSeconds;  // start later
    return myID;
  }
  
  if((this->intervallMilliSeconds != 0)&&(waitForWinHandle == false))
  {
    stop();
  } 

  this->intervallMilliSeconds = intervallMilliSeconds;
  SetTimer(messageHandle, myID, intervallMilliSeconds, NULL);

  return myID;
}

void TGWTimer::stop()
{
  if((myMessageHandlerWindow->getWindowHandle()!=0)&&(myID!=0))
  {
    KillTimer(myMessageHandlerWindow->getWindowHandle(), myID);
  }
  intervallMilliSeconds = 0;
}

int TGWTimer::getID()
{
  return myID;
}

void TGWTimer::eventCreated()
{
  if(waitForWinHandle==true)
  {
    start(this->intervallMilliSeconds);
  }
};