

public class Spiel
{
	
	// Das Spielfeld besteht aus 3x3 Feldern und wird durch einen int-Array verwalten
	// Für die Array-Werte gilt:
	// 0 => leeres Feld
	// 1 => Feld vom Benutzer belegt
	// 2 => Feld vom Computer belegt 	
	public int[][] spielfeld = new int[3][3];
	

	// Setzt das Spiel auf den Anfangszustand zurück
	void clear()
	{
		for( int x = 0; x < 3; x++ )
		{
			for( int y = 0; y < 3; y++ )
			{
				spielfeld[x][y] = 0;
			}
		}
	}
	
	// Der Benutzer oder der Computer haben ein Feld im Spielfeld ausgewählt	
	// Hier wird berechnet, ob der Zug möglich ist (Rückgabe true)
	// und dann entsprechend reagiert 
	boolean spielen( int x, int y, int typ ) throws Exception
	{
		// Ein bischen Sicherheit muß sein		
		if( x >= 0 && x < 3 && y >= 0 && y < 3 )
		{
			if( spielfeld[x][y] == 0 )
			{
				// Das Feld ist noch leer, also kann man den Zug einfügen
				spielfeld[x][y] = typ;
				
				// Das Spiel bewerten. Wenns vorbei ist, kommt eine Exception, die
				// das Panel fangen soll 
				istEsVorbei();	
				
				if( typ == 1 )
				{		
					// Jetzt kontern
					kontern();
				}	
			}
			else
			{
				return false;
			}
		}
		else
		{
			return false;
		}
		
		return true;
	}
	
	// Berechnet, ob eine Partei drei Felder in einer Reihe hat.
	void istEsVorbei() throws Exception
	{
		int user = 0;
		int computer = 0;
		
		// erst mal die senkrechten Reihen untersuchen
		for( int x = 0; x < 3; x++ )
		{
			user = 0;
			computer = 0;
			
			for( int y = 0; y < 3 ;y++ )
			{
				if( spielfeld[x][y] == 1 )
				{
					user++;
				}
				else if( spielfeld[x][y] == 2 )
				{
					computer++;
				}
			}
			
			if( computer == 3 )
			{
				Exception e = new Exception( "Computer hat gewonnen!" );
				throw e;
			}
			
			if( user == 3 )
			{
				Exception e = new Exception( "Sie haben gewonnen!" );
				throw e;
			}
		}
		
		// dann die waagerechten Reihen untersuchen
		for( int y = 0; y < 3; y++ )
		{
			user = 0;
			computer = 0;
			
			for( int x = 0; x < 3; x++ )
			{
				if( spielfeld[x][y] == 1 )
				{
					user++;
				}
				else if( spielfeld[x][y] == 2 )
				{
					computer++;
				}
			}
			
			if( computer == 3 )
			{
				Exception e = new Exception( "Computer hat gewonnen!" );
				throw e;
			}
			
			if( user == 3 )
			{
				Exception e = new Exception( "Sie haben gewonnen!" );
				throw e;
			}
		}
		
		// dann noch dier Diagonale
		user = 0;
		computer = 0;
		
		for( int x = 0; x < 3; x++ )
		{
			if( spielfeld[x][x] == 1 )
			{
				user++;
			}
			else if( spielfeld[x][x] == 2 )
			{
				computer++;
			}
			
			if( computer == 3 )
			{
				Exception e = new Exception( "Computer hat gewonnen!" );
				throw e;
			}
			
			if( user == 3 )
			{
				Exception e = new Exception( "Sie haben gewonnen!" );
				throw e;
			}
		}
		
		// vielleicht geht ja gar nichts mehr, weil das Spielfeld voll ist
		boolean isVoll = true;	
		for( int x = 0; x < 3; x++ )
		{
			for( int y = 0; y < 3 ;y++ )
			{
				if( spielfeld[x][y] == 0 )
				{
					isVoll = false;
					break;
				}
			}
		}	
		
		if( isVoll )
		{
			Exception e = new Exception( "Unentschieden" );
			throw e;
		}
		
	}
	
	void kontern() throws Exception
	{
		// hier ist keine KI am Werk, sondern dumpfes Ausprobieren
		for( int x = 0; x < 3; x++ )
		{
			for( int y = 0; y < 3 ;y++ )
			{
				if( spielfeld[x][y] == 0 )
				{
					// ein leeres Feld, das nehmen wir!		
					spielen( x, y, 2 );
					return;
				}
			}
		}
	}
}