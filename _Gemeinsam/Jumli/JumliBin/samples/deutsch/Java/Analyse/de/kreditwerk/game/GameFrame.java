package de.kreditwerk.game;
import javax.swing.JFrame;

/**
* public class GameFrame
* This class is the main window.
*/
public class GameFrame extends JFrame
{
	public GameFrame()
	{
		// We create the panel and add it to the frame
		GamePanel panel = new GamePanel();
		getContentPane().add( panel );		
			
		addWindowListener( new java.awt.event.WindowAdapter(){
			public void windowClosing( java.awt.event.WindowEvent evt ){
				 System.exit(0);
			}
		});
	}
}
