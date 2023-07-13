
// Diese imports wurden generiert
import javax.swing.JPanel;
import java.awt.event.MouseListener;

// Diese imports wurde manuell hinzugefügt
import java.awt.event.MouseEvent;
import java.awt.*;

/**
* public class SpielPanel
* In dieser Klasse wird gezeichnet.
*/
public class SpielPanel extends JPanel implements MouseListener
{
	
	protected void paintComponent( Graphics graphics )
	{
		// Tour 2: Hier z.B. einen Fehler provozieren
		// z.B. durch "super.paint  Component();"
		// Dann die Datei compilieren
		// Die Fehler werden im Nachrichtenfenster angezeigt
		// Durch Doppelklick im Nachrichtenfenster auf die Zeilen mit
		// der Angabe der Datei und der Zeile wird die Datei geöffnet 
		// und die Zeile selektiert.
		// Mit F4 kann man zwischen mehreren Fehlern wechseln.
		super.paintComponent( graphics );	
		
		// Linien zeichnen	
		Dimension size = getSize();
		int xSize = (int) size.getWidth() / 3;
		int ySize = (int) size.getHeight() / 3;

		for( int index = 1; index < 3; index++ ) 
		{
			graphics.drawLine( index * xSize, 0, index * xSize, (int) size.getHeight() );
			graphics.drawLine( 0, index * ySize, (int) size.getWidth(), index * ySize );
		}
		
		
		for( int x = 0; x < 3; x++ ) 
		{
			for( int y = 0; y < 3; y++ ) 
			{	
				if( spiel.spielfeld[x][y] == 1 )
				{
					graphics.drawLine( x * xSize, y * ySize, ( x + 1 ) * xSize, ( y + 1 ) * ySize );
					graphics.drawLine( x * xSize, ( y + 1 ) * ySize, ( x + 1 ) * xSize, y * ySize );
				}
				else if( spiel.spielfeld[x][y] == 2 )
				{
					graphics.drawOval( x * xSize, y * ySize, xSize, ySize );
				}		
			}
		} 
		
	}

	
	/**
	* public void mouseClicked( MouseEvent e )
	* Invoked when the mouse button has been clicked (pressed
	*  and released) on a component.
	*/
	public void mouseClicked( MouseEvent e )
	{
	}
	
	/**
	* public void mouseEntered( MouseEvent e )
	* Invoked when the mouse enters a component.
	*/
	public void mouseEntered( MouseEvent e )
	{
	}
	
	/**
	* public void mouseExited( MouseEvent e )
	* Invoked when the mouse exits a component.
	*/
	public void mouseExited( MouseEvent e )
	{
	}
	
	/**
	* public void mousePressed( MouseEvent e )
	* Invoked when a mouse button has been pressed on a component.
	*/
	public void mousePressed( MouseEvent e )
	{
		int xPunkt = e.getX();
		int yPunkt = e.getY();
		
		int xFeld = 0;
		int yFeld = 0;
		
		// aus den Panel Koordinaten die Spielfeld Koordinaten berechnen
		Dimension size = getSize();
		int xSize = (int) size.getWidth() / 3;
		int ySize = (int) size.getHeight() / 3;

		for( int x = 0; x < 3; x++ ) 
		{
			for( int y = 0; y < 3; y++ ) 
			{	
				if( xPunkt >= x * xSize && xPunkt < (x + 1) * xSize )
				{
					// das isses
					xFeld = x;
				}
				
				if( yPunkt >= y * ySize && yPunkt < (y + 1) * ySize )
				{
					// das isses
					yFeld = y;
				}
			}
		}
		
		try
		{
			spiel.spielen( xFeld, yFeld, 1 );
		}
		catch( Exception ex )
		{
			String message = ex.getMessage();
			System.out.println( message );
			spiel.clear();
		}
		
		repaint();
		
	}
	
	/**
	* public void mouseReleased( MouseEvent e )
	* Invoked when a mouse button has been released on a component.
	*/
	public void mouseReleased( MouseEvent e )
	{
	}
	
	public SpielPanel()
	{
		addMouseListener( this );		
		
		spiel = new Spiel();
		spiel.clear();
		
	}
	
	private Spiel spiel;
	
}