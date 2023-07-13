#ifndef _JUMLIWXDOC_H_
#define _JUMLIWXDOC_H_

#include "wx/docview.h"

class JumliWxDoc : public wxDocument
{
	DECLARE_DYNAMIC_CLASS( JumliWxDoc )
public:
	virtual bool OnSaveDocument( const wxString& filename );
	virtual bool OnOpenDocument( const wxString& filename );
	virtual bool OnNewDocument();
	
	DECLARE_EVENT_TABLE()
};

#endif