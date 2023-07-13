#ifndef _JUMLIWXVIEW_H_
#define _JUMLIWXVIEW_H_

#include "wx/docview.h"

class JumliWxView : public wxView
{
	DECLARE_DYNAMIC_CLASS( JumliWxView )
public:
	void OnDraw( wxDC * dc );
	
	virtual bool OnCreate( wxDocument* doc, long flags );
	
    DECLARE_EVENT_TABLE()
};

#endif