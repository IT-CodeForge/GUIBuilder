

public class Game
{
	
	// The "playground" is a 3 x 3 int-array
	// Definition:
	// 0 => Field is empty
	// 1 => Field is used by user
	// 2 => Field is used by computer 	
	public int[][] playground = new int[3][3];
	

	// Resets the game
	void clear()
	{
		for( int x = 0; x < 3; x++ )
		{
			for( int y = 0; y < 3; y++ )
			{
				playground[x][y] = 0;
			}
		}
	}
	
	// User or computer has selected a field
	boolean play( int x, int y, int type ) throws Exception
	{
		// Security stuff
		if( x >= 0 && x < 3 && y >= 0 && y < 3 )
		{
			if( playground[x][y] == 0 )
			{
				// Field is empty
				playground[x][y] = type;
				
				// if the game is over, we throw an exception.
				isItOver();	
				
				if( type == 1 )
				{		
					strikeBack();
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
	
	// Calculates, if there are three fileds in a row.
	void isItOver() throws Exception
	{
		int user = 0;
		int computer = 0;
		
		// vertically
		for( int x = 0; x < 3; x++ )
		{
			user = 0;
			computer = 0;
			
			for( int y = 0; y < 3 ;y++ )
			{
				if( playground[x][y] == 1 )
				{
					user++;
				}
				else if( playground[x][y] == 2 )
				{
					computer++;
				}
			}
			
			if( computer == 3 )
			{
				Exception e = new Exception( "Computer wins!" );
				throw e;
			}
			
			if( user == 3 )
			{
				Exception e = new Exception( "You win again!" );
				throw e;
			}
		}
		
		// horizontally
		for( int y = 0; y < 3; y++ )
		{
			user = 0;
			computer = 0;
			
			for( int x = 0; x < 3; x++ )
			{
				if( playground[x][y] == 1 )
				{
					user++;
				}
				else if( playground[x][y] == 2 )
				{
					computer++;
				}
			}
			
			if( computer == 3 )
			{
				Exception e = new Exception( "Computer wins!" );
				throw e;
			}
			
			if( user == 3 )
			{
				Exception e = new Exception( "You win again!" );
				throw e;
			}
		}
		
		// diagonally
		user = 0;
		computer = 0;
		
		for( int x = 0; x < 3; x++ )
		{
			if( playground[x][x] == 1 )
			{
				user++;
			}
			else if( playground[x][x] == 2 )
			{
				computer++;
			}
			
			if( computer == 3 )
			{
				Exception e = new Exception( "Computer wins!" );
				throw e;
			}
			
			if( user == 3 )
			{
				Exception e = new Exception( "You win again!" );
				throw e;
			}
		}
		
		// Is the playgrouns full?
		boolean isVoll = true;	
		for( int x = 0; x < 3; x++ )
		{
			for( int y = 0; y < 3 ;y++ )
			{
				if( playground[x][y] == 0 )
				{
					isVoll = false;
					break;
				}
			}
		}	
		
		if( isVoll )
		{
			Exception e = new Exception( "Remis" );
			throw e;
		}
		
	}
	
	void strikeBack() throws Exception
	{
		// Heavy AI
		for( int x = 0; x < 3; x++ )
		{
			for( int y = 0; y < 3 ;y++ )
			{
				if( playground[x][y] == 0 )
				{
					// This field is empty
					play( x, y, 2 );
					return;
				}
			}
		}
	}
}