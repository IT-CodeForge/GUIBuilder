import javax.swing.JFrame;


/**
* public class SpielFrame
* Diese Klasse ist das Hauptfenster. Damit das Programm richtig 
* beendet wird, hat sie einen Konstruktor, in dem Jumli 
* Sourcecode zum Beenden hinzufügt.
*/
public class SpielFrame extends JFrame
{

	public SpielFrame()
	{
		// Hier wird das Panel erzeugt und in das Frame eingefügt		
		SpielPanel panel = new SpielPanel();
		getContentPane().add( panel );		
		
		// anonyme innere Klasse zum korrekten Beenden
		addWindowListener( new java.awt.event.WindowAdapter(){
			public void windowClosing( java.awt.event.WindowEvent evt ){
				 System.exit(0);
			}
		});
	}
}