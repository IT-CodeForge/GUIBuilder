

/**
* public class Start
* Diese Klasse hat die main()-Methode 
* und ist nur dazu da, das Spiel zu starten.
*/
public class Start
{
	
	public static void main( String[] args )
	{
		// Hier wird das Fenster erzeugt	
		SpielFrame frame = new SpielFrame();
		frame.setSize( 400, 400 );
		frame.show();
	}
}