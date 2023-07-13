#include "JumliWx.h"
#include "JumliWxDoc.h"
#include "JumliWxFrame.h"
#include "JumliWxView.h"
#include "wx/xrc/xmlres.h"

IMPLEMENT_APP(JumliWx)

JumliWx::JumliWx()
: m_JumliWxFrame( NULL ),
  m_DocManager( NULL )	
{
}

bool JumliWx::OnInit()
{
	wxXmlResource::Get()->SetFlags( 0 );
	wxXmlResource::Get()->InitAllHandlers();
	wxXmlResource::Get()->Load( "JumliWx.xrc" );	
	
	m_DocManager = new wxDocManager;
    new wxDocTemplate( m_DocManager, "JumliWx", "*.xyz", "", "xyz", "JumliWx Doc", "JumliWx View",
       				   CLASSINFO(JumliWxDoc), CLASSINFO(JumliWxView));
	m_JumliWxFrame = new JumliWxFrame( m_DocManager, NULL, -1, "JumliWx", wxPoint(0, 0), wxSize(800, 600), wxDEFAULT_FRAME_STYLE );
	
    m_JumliWxFrame->Show( TRUE );
    SetTopWindow( m_JumliWxFrame );
	
	return true;
}


int JumliWx::OnExit()
{
	delete m_DocManager;
    return 0;
}

JumliWxFrame * JumliWx::GetJumliWxFrame()
{
	return m_JumliWxFrame;	
}
