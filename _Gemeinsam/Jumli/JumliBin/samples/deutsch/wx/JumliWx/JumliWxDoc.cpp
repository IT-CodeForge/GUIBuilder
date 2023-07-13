#include "JumliWxDoc.h"
#include "JumliWxView.h"

IMPLEMENT_DYNAMIC_CLASS(JumliWxDoc, wxDocument)

BEGIN_EVENT_TABLE(JumliWxDoc, wxDocument)
END_EVENT_TABLE()

bool JumliWxDoc::OnNewDocument()
{
	bool ret;
	ret = wxDocument::OnNewDocument();
	
	return ret;
}

bool JumliWxDoc::OnSaveDocument( const wxString& filename )
{
	bool ret;
	ret = wxDocument::OnSaveDocument( filename );
	
	return ret;
}

bool JumliWxDoc::OnOpenDocument( const wxString& filename ) 
{
	bool ret;
	ret = wxDocument::OnOpenDocument( filename );
	
	(JumliWxView*)GetFirstView();
	
	return ret;
}
