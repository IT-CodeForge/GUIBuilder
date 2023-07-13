#ifndef _JUMLIWXFRAME_H_
#define _JUMLIWXFRAME_H_

#include "wx/docview.h"

class JumliWxFrame : public wxDocParentFrame
{
    DECLARE_CLASS( JumliWxFrame )

public:
	virtual ~JumliWxFrame();
	JumliWxFrame( wxDocManager* manager, wxFrame * parent, wxWindowID id, const wxString& title, const wxPoint& pos = wxDefaultPosition, const wxSize& size = wxDefaultSize, long style = wxDEFAULT_FRAME_STYLE, const wxString& name = "frame" );
	
	void OnAbout( wxCommandEvent& event );

	DECLARE_EVENT_TABLE()
};

#endif
