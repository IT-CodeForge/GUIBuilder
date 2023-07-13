#include "JumliWxView.h"

IMPLEMENT_DYNAMIC_CLASS( JumliWxView, wxView )

BEGIN_EVENT_TABLE( JumliWxView, wxView )
END_EVENT_TABLE()

bool JumliWxView::OnCreate( wxDocument* doc, long flags )
{
	return true;
}

void JumliWxView::OnDraw( wxDC * dc )
{
}