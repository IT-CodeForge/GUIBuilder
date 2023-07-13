
using System.Windows.Forms;

public class FirstWindow : Form
{
	
	static void Main( string[] args )
	{
		Application.Run( new FirstWindow() );
	}
	
	public FirstWindow()
	{
		this.Text = "Only a window!";
	}
}