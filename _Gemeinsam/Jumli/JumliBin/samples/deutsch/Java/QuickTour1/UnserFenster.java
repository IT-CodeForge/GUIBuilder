
import javax.swing.JFrame;

/**
* public class UnserFenster
* Dies ist die Fenster- Klasse, die die Eigentschaften von JFrame erbt.
* 
* Folgende Angaben wurden im Dialog gemacht:
* 1: Der Name
* 2: Die Checkbox "bindet main ein" wurde ausgew�hlt
* 3. Die Checkbox "Konstruktor" wurde ausgew�hlt.
*/
public class UnserFenster extends JFrame
{
	// Tipp: F�r alle JDK-Klassen kann man sich die Original-Dokumentation
	// zeigen lassen. Dazu z.B. JFrame durch Doppelklick selektieren und F1 dr�cken.
	public static void main( String[] args )
	{
		// Dieser Bereich wurde manuell programmiert.	
		UnserFenster fenster = new UnserFenster();
		fenster.show();
		fenster.setSize( 200, 200 );
	}
	
	public UnserFenster()
	{
		// Jumli generiert in einem Konstruktor einer Klasse,
		// die von JFrame abgeleitet ist, einen anonymen inneren
		// WindowListener, der daf�r sorgt, dass nach dem Beenden
		// des Programms die Virtual Machine wieder beendet wird.
		addWindowListener( new java.awt.event.WindowAdapter(){
			public void windowClosing(java.awt.event.WindowEvent evt){
				 System.exit(0);
			}
		});
	}
	
	
	
}