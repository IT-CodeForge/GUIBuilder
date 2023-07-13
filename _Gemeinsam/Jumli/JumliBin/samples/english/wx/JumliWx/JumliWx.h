#ifndef _JUMLIWX_H_
#define _JUMLIWX_H_

#include "wx/docview.h"
#include "wx/app.h"

class JumliWxFrame;

class JumliWx : public wxApp
{
public:
	JumliWx();	
	
	JumliWxFrame* GetJumliWxFrame();
	
	int OnExit();
	
	bool OnInit();
private:
	JumliWxFrame* m_JumliWxFrame;
	wxDocManager * m_DocManager;
	
};

DECLARE_APP(JumliWx)

#endif
