#include "JumliWxFrame.h"
#include "wx/msgdlg.h"
#include "wx/xrc/xmlres.h"

IMPLEMENT_CLASS(JumliWxFrame, wxDocParentFrame)

BEGIN_EVENT_TABLE(JumliWxFrame, wxDocParentFrame)
	EVT_MENU(XRCID("IDM_ABOUT"), JumliWxFrame::OnAbout)
END_EVENT_TABLE()

JumliWxFrame::JumliWxFrame( wxDocManager* manager, wxFrame * parent, wxWindowID id, const wxString& title, const wxPoint& pos, const wxSize& size, long style, const wxString& name )
:wxDocParentFrame(manager, parent, id, title, pos, size, style)
{
	SetMenuBar( wxXmlResource::Get()->LoadMenuBar( this, "ID_MENU_MAIN" ) );
}

JumliWxFrame::~JumliWxFrame()
{
}

void JumliWxFrame::OnAbout( wxCommandEvent& event )
{
    wxMessageBox( "JumliWx", "About JumliWx");
}
