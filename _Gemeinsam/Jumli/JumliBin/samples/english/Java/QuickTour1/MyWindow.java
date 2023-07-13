import javax.swing.JFrame;

/**
* public class MyWindow
* This window-class inherits all properties from JFrame.
* 
* Class-Dialog settings:
* 1: name
* 2: checkbox "main"
* 3. checkbox "Constructor"
*/
public class MyWindow extends JFrame
{
	// Tip: You can reach the JDK class-ducumentation by selecting "JFrame" and the key "F1".
	public static void main( String[] args )
	{
		MyWindow window = new MyWindow();
		window.show();
		window.setSize( 200, 200 );
	}
	
	public MyWindow()
	{
		// Jumli automatically creates an inner class
		// which handles the close event.
		addWindowListener( new java.awt.event.WindowAdapter(){
			public void windowClosing(java.awt.event.WindowEvent evt){
				 System.exit(0);
			}
		});
	}
}

