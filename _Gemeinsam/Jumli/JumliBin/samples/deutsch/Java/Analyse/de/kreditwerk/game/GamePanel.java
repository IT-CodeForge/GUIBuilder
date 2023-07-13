package de.kreditwerk.game;

// Generated by Jumli
import javax.swing.JPanel;
import java.awt.event.MouseListener;

// User defined imports
import java.awt.event.MouseEvent;
import java.awt.*;

/**
* public class GamePanel
* *
* * public class GamePanel
* * This class draws the game.
*/
public class GamePanel extends JPanel implements MouseListener
{
	protected void paintComponent( Graphics graphics )
	{
		super.paintComponent( graphics );	
		
		// Drawing the line	
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
				if( game.playground[x][y] == 1 )
				{
					graphics.drawLine( x * xSize, y * ySize, ( x + 1 ) * xSize, ( y + 1 ) * ySize );
					graphics.drawLine( x * xSize, ( y + 1 ) * ySize, ( x + 1 ) * xSize, y * ySize );
				}
				else if( game.playground[x][y] == 2 )
				{
					graphics.drawOval( x * xSize, y * ySize, xSize, ySize );
				}		
			}
		} 
	}

	public GamePanel()
	{
		addMouseListener( this );		
		
		game = new Game();
		game.clear();
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
		int xPoint = e.getX();
		int yPoint = e.getY();
		
		int xField = 0;
		int yField = 0;
		
		Dimension size = getSize();
		int xSize = (int) size.getWidth() / 3;
		int ySize = (int) size.getHeight() / 3;

		for( int x = 0; x < 3; x++ ) 
		{
			for( int y = 0; y < 3; y++ ) 
			{	
				if( xPoint >= x * xSize && xPoint < (x + 1) * xSize )
				{
					// found x
					xField = x;
				}
				
				if( yPoint >= y * ySize && yPoint < (y + 1) * ySize )
				{
					// found y
					yField = y;
				}
			}
		}
		
		try
		{
			game.play( xField, yField, 1 );
		}
		catch( Exception ex )
		{
			String message = ex.getMessage();
			System.out.println( message );
			game.clear();
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
	
	private Game game;

}