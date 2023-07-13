
using System;
using System.Drawing;

namespace CSharpXXRIS
{
	/// <summary>
	/// Die Klasse Shape übernimmt die Gestalltung und die Bewegungen im Spielfeld
	/// </summary>
	public class Shape
	{
		// setzen unserer Klassenvariablen
		// public
		public Point[] pntShape;
		public Rectangle[] rctShape;
		public bool bolShapeMoving;

		//private
		private int intStartingXCoordinate;
		private int intCurrentShape = 1;
		private int intCurrentShapePosition = 1;
		private int[] intBlocXPos = new int[4];
		private int[] intBlocYPos = new int[4];
		private int[] intXPositions = new int[4];
		private int intPanelWidth;
		private int intPanelHeight;
		private bool bolIsNextShape = false;

		public Shape(int intShapeType, int intScreenWidth, int intScreenHeight, bool bolNextShape)
		{
			intStartingXCoordinate = ((intScreenWidth-1)/2);
			intPanelWidth = intScreenWidth;
			intPanelHeight = intScreenHeight;
			bolIsNextShape = bolNextShape;

			// setzen des aktuellen Shapes
			intCurrentShape = intShapeType;

			// setzen der Standard Shape Position
			SetShapeStart();
		}
		
		private void BuildShape(int intShapeType)
		{
			// alle Shapes werden aus Rechecken gebildet
			rctShape = new Rectangle[4];
			
			// beginnen mit dem Startrecheck - dies ist immer die zentrale Position
			rctShape[0] = new Rectangle(intBlocXPos[0],intBlocYPos[0],10,10);
			rctShape[1] = new Rectangle(intBlocXPos[1],intBlocYPos[1],10,10);
			rctShape[2] = new Rectangle(intBlocXPos[2],intBlocYPos[2],10,10);
			rctShape[3] = new Rectangle(intBlocXPos[3],intBlocYPos[3],10,10);
		}
		
		public Rectangle[] moveShapeDown(int intMovePixels, Rectangle[][] rctGameGrid)
		{
			bool bolCanMove = true;

			// schauen ob irgendwelche x-Positions über den Rand gehen
			for (int j=0;j<4;j++)
			{
				if (((intBlocYPos[j] +10) + intMovePixels) > intPanelHeight-1)
				{
					bolCanMove = false;
					bolShapeMoving = false;
					break;
				}
			}
			
			// der Spielstein hat den Boden noch nicht berührt, deshalb schauen wir ob
			// wir einen festen Stein in unserem Spielfeld getroffen haben
			if (bolCanMove)
			{
				for (int k=0;k<4;k++)
				{
					if (Decimal.Remainder(intBlocYPos[k],10) == 0 && intBlocYPos[k] >= 0)
					{
						if (!rctGameGrid[(intBlocYPos[k]/10)+1][intBlocXPos[k]/10].IsEmpty)
						{
							// der Spielstein berührt die festen Steine
							bolCanMove = false;
							bolShapeMoving = false;
							break;
						}
					}
				}
			}
			
			if (bolCanMove)
			{
				for (int i=0;i<4;i++)
				{
					intBlocYPos[i] += intMovePixels;
				}
			}
			
			BuildShape(intCurrentShape);
			return rctShape;
		}
		
		public Rectangle[] moveShapeLeft(int intMovePixels, Rectangle[][] rctGameGrid)
		{
			bool bolCanMove = true;
			int[] intYPositions = new int[4];

			int intFurthestX = intPanelWidth;
			
			// kontrolieren um zusehen ob irgendwelche x-Positionen über den Rand gehen
			// oder einen festen Stein berühren, um das zu garantiern brauchen wir den Stein
			// der ganz links ist
			// 
			for (int j=0;j<4;j++)
			{
				if (intBlocXPos[j] <= intFurthestX)
				{
					intFurthestX = intBlocXPos[j];
					intYPositions[j] = intBlocYPos[j];
					if (Decimal.Remainder(intBlocYPos[j],10) != 0)
					{
						intYPositions[j] += 5;
					}
				}
				if ((intBlocXPos[j] - intMovePixels) < 0)
				{
					bolCanMove = false;
					break;
				}
			}
			if (bolCanMove)
			{
				for (int i=0;i<4;i++)
				{
					if (intYPositions[i] >= 0)
					{
						if (!rctGameGrid[intYPositions[i]/10][(intFurthestX-10)/10].IsEmpty)
						{
							
							bolCanMove = false;
							break;
						}
					}
				}
			}
			if (bolCanMove)
			{
				for (int i=0;i<4;i++)
				{
					intBlocXPos[i] -= intMovePixels;
				}
			}
			BuildShape(intCurrentShape);
			return rctShape;
		}
		
		public Rectangle[] moveShapeRight(int intMovePixels, Rectangle[][] rctGameGrid)
		{
			// jetzt alles für die Rechtsbewegung
			bool bolCanMove = true;
			int[] intYPositions = new int[4];
			
			int intFurthestX = 0;
			
			for (int j=0;j<4;j++)
			{
				if (intBlocXPos[j] >= intFurthestX)
				{
					intFurthestX = intBlocXPos[j];
					intYPositions[j] = intBlocYPos[j];
					if (Decimal.Remainder(intBlocYPos[j],10) != 0)
					{
						intYPositions[j] += 5;
					}
				}
				if ((intBlocXPos[j] + intMovePixels) + 10 >= intPanelWidth)
				{
					bolCanMove = false;
					break;
				}
			}
			if (bolCanMove)
			{
				for (int i=0;i<4;i++)
				{
					if (intYPositions[i] >= 0)
					{
						if (!rctGameGrid[intYPositions[i]/10][(intFurthestX+10)/10].IsEmpty)
						{
							// der Steine dabei die festen Steine zuberühren							
							bolCanMove = false;
							break;
						}
					}
				}
			}
			if (bolCanMove)
			{
				for (int i=0;i<4;i++)
				{
					intBlocXPos[i] += intMovePixels;
				}
			}
			BuildShape(intCurrentShape);
			return rctShape;
		}
		
		public Rectangle[] FlipShape(string strDirection, Rectangle[][] rctGameGrid)
		{
			bool bolCanShapeMove = true;
			
			if (strDirection == "right")
			{
				intCurrentShapePosition++;
				if (intCurrentShapePosition > 4)
				{
					intCurrentShapePosition = 1;
				}
			}
			
			if (strDirection == "left")
			{
				intCurrentShapePosition--;
				if (intCurrentShapePosition < 1)
				{
					intCurrentShapePosition = 4;
				}
			}
			
			SetShapePosition();
			BuildShape(intCurrentShape);
			// bevor der Spielstein zurückgedreht wird schauen wir ob er passt
			
			Rectangle recGameArea = new Rectangle(0,0,intPanelWidth,intPanelHeight);
			int[] intYPositions = new int[4];
			
			for (int i=0;i<4;i++)
			{
				if (!recGameArea.Contains(rctShape[i]))
				{
					bolCanShapeMove = false;
					break;
				}
				// hier schauen wir ob der Spielstein mi anderen festen 
				// Steinen kollidiert
				
				intYPositions[i] = intBlocYPos[i];
				if (Decimal.Remainder(intBlocYPos[i],10) != 0)
				{
					intYPositions[i] += 5;
				}
				if (!rctGameGrid[intYPositions[i]/10][intBlocXPos[i]/10].IsEmpty)
				{
					// der Stein ist dabei die festen Steine zu berühren
					bolCanShapeMove = false;
					break;
				}
			}
			
			if (!bolCanShapeMove)
			{
				// alles zurück
				if (strDirection == "right") 
				{
					intCurrentShapePosition--;
					if (intCurrentShapePosition < 1) 
					{
						intCurrentShapePosition = 4;
					}
					SetShapePosition();
					BuildShape(intCurrentShape);
				}
				
				if (strDirection == "left") 
				{
					intCurrentShapePosition++;
					if (intCurrentShapePosition > 4) 
					{
						intCurrentShapePosition = 1;
					}
					SetShapePosition();
					BuildShape(intCurrentShape);
				}
			}
			
			return rctShape;
		}
		
		private void SetShapeStart()
		{
			if (!bolIsNextShape)
			{
				switch(intCurrentShape)
				{
					
					case 1:
						intBlocXPos[0] = intStartingXCoordinate;
						intBlocYPos[0] = -10;
						intBlocXPos[1] = intStartingXCoordinate-10;
						intBlocYPos[1] = -10;
						intBlocXPos[2] = intStartingXCoordinate+10;
						intBlocYPos[2] = -10;
						intBlocXPos[3] = intStartingXCoordinate;
						intBlocYPos[3] = -20;
						break;
					case 2:
						intBlocXPos[0] = intStartingXCoordinate;
						intBlocYPos[0] = -10;
						intBlocXPos[1] = intStartingXCoordinate-10;
						intBlocYPos[1] = -10;
						intBlocXPos[2] = intStartingXCoordinate+10;
						intBlocYPos[2] = -10;
						intBlocXPos[3] = intStartingXCoordinate+10;
						intBlocYPos[3] = -20;
						break;
					case 3:
						intBlocXPos[0] = intStartingXCoordinate;
						intBlocYPos[0] = -10;
						intBlocXPos[1] = intStartingXCoordinate-10;
						intBlocYPos[1] = -10;
						intBlocXPos[2] = intStartingXCoordinate+10;
						intBlocYPos[2] = -10;
						intBlocXPos[3] = intStartingXCoordinate-10;
						intBlocYPos[3] = -20;
						break;
					case 4:
						intBlocXPos[0] = intStartingXCoordinate;
						intBlocYPos[0] = -10;
						intBlocXPos[1] = intStartingXCoordinate+10;
						intBlocYPos[1] = -10;
						intBlocXPos[2] = intStartingXCoordinate;
						intBlocYPos[2] = -20;
						intBlocXPos[3] = intStartingXCoordinate+10;
						intBlocYPos[3] = -20;
						break;
					case 5:
						intBlocXPos[0] = intStartingXCoordinate;
						intBlocYPos[0] = -10;
						intBlocXPos[1] = intStartingXCoordinate;
						intBlocYPos[1] = -20;
						intBlocXPos[2] = intStartingXCoordinate;
						intBlocYPos[2] = -30;
						intBlocXPos[3] = intStartingXCoordinate;
						intBlocYPos[3] = -40;
						break;
					default:
						break;	
				}
			}
			else
			{
				switch(intCurrentShape)
				{
					
					case 1:
						intBlocXPos[0] = intStartingXCoordinate-5;
						intBlocYPos[0] = 35;
						intBlocXPos[1] = intStartingXCoordinate-15;
						intBlocYPos[1] = 35;
						intBlocXPos[2] = intStartingXCoordinate+5;
						intBlocYPos[2] = 35;
						intBlocXPos[3] = intStartingXCoordinate-5;
						intBlocYPos[3] = 25;
						break;
					case 2:
						intBlocXPos[0] = intStartingXCoordinate-5;
						intBlocYPos[0] = 35;
						intBlocXPos[1] = intStartingXCoordinate-15;
						intBlocYPos[1] = 35;
						intBlocXPos[2] = intStartingXCoordinate+5;
						intBlocYPos[2] = 35;
						intBlocXPos[3] = intStartingXCoordinate+5;
						intBlocYPos[3] = 25;
						break;
					case 3:
						intBlocXPos[0] = intStartingXCoordinate-5;
						intBlocYPos[0] = 35;
						intBlocXPos[1] = intStartingXCoordinate-15;
						intBlocYPos[1] = 35;
						intBlocXPos[2] = intStartingXCoordinate+5;
						intBlocYPos[2] = 35;
						intBlocXPos[3] = intStartingXCoordinate-15;
						intBlocYPos[3] = 25;
						break;
					case 4:
						intBlocXPos[0] = intStartingXCoordinate-10;
						intBlocYPos[0] = 35;
						intBlocXPos[1] = intStartingXCoordinate;
						intBlocYPos[1] = 35;
						intBlocXPos[2] = intStartingXCoordinate-10;
						intBlocYPos[2] = 25;
						intBlocXPos[3] = intStartingXCoordinate;
						intBlocYPos[3] = 25;
						break;
					case 5:
						intBlocXPos[0] = intStartingXCoordinate-5;
						intBlocYPos[0] = 45;
						intBlocXPos[1] = intStartingXCoordinate-5;
						intBlocYPos[1] = 35;
						intBlocXPos[2] = intStartingXCoordinate-5;
						intBlocYPos[2] = 25;
						intBlocXPos[3] = intStartingXCoordinate-5;
						intBlocYPos[3] = 15;
						break;
					default:
						break;	
				}
				BuildShape(intCurrentShape);
			}
		}
		
		public Rectangle[] GetShape()
		{
			return rctShape;
		}
		
		private void SetShapePosition()
		{
			switch(intCurrentShape)
			{
				case 1:
				switch(intCurrentShapePosition)
				{
					case 1:
						intBlocXPos[0] = intBlocXPos[0];
						intBlocYPos[0] = intBlocYPos[0];
						intBlocXPos[1] = intBlocXPos[0]-10;
						intBlocYPos[1] = intBlocYPos[0];
						intBlocXPos[2] = intBlocXPos[0]+10;
						intBlocYPos[2] = intBlocYPos[0];
						intBlocXPos[3] = intBlocXPos[0];
						intBlocYPos[3] = intBlocYPos[0]-10;
						break;
					case 2:
						intBlocXPos[0] = intBlocXPos[0];
						intBlocYPos[0] = intBlocYPos[0];
						intBlocXPos[1] = intBlocXPos[0];
						intBlocYPos[1] = intBlocYPos[0]-10;
						intBlocXPos[2] = intBlocXPos[0];
						intBlocYPos[2] = intBlocYPos[0]+10;
						intBlocXPos[3] = intBlocXPos[0]+10;
						intBlocYPos[3] = intBlocYPos[0];
						break;
					case 3:
						intBlocXPos[0] = intBlocXPos[0];
						intBlocYPos[0] = intBlocYPos[0];
						intBlocXPos[1] = intBlocXPos[0]+10;
						intBlocYPos[1] = intBlocYPos[0];
						intBlocXPos[2] = intBlocXPos[0]-10;
						intBlocYPos[2] = intBlocYPos[0];
						intBlocXPos[3] = intBlocXPos[0];
						intBlocYPos[3] = intBlocYPos[0]+10;
						break;
					case 4:
						intBlocXPos[0] = intBlocXPos[0];
						intBlocYPos[0] = intBlocYPos[0];
						intBlocXPos[1] = intBlocXPos[0];
						intBlocYPos[1] = intBlocYPos[0]+10;
						intBlocXPos[2] = intBlocXPos[0];
						intBlocYPos[2] = intBlocYPos[0]-10;
						intBlocXPos[3] = intBlocXPos[0]-10;
						intBlocYPos[3] = intBlocYPos[0];
						break;
					default:
						break;
				}
					break;
				case 2:
				switch(intCurrentShapePosition)
				{
					case 1:
						intBlocXPos[0] = intBlocXPos[0];
						intBlocYPos[0] = intBlocYPos[0];
						intBlocXPos[1] = intBlocXPos[0]-10;
						intBlocYPos[1] = intBlocYPos[0];
						intBlocXPos[2] = intBlocXPos[0]+10;
						intBlocYPos[2] = intBlocYPos[0];
						intBlocXPos[3] = intBlocXPos[0]+10;
						intBlocYPos[3] = intBlocYPos[0]-10;
						break;
					case 2:
						intBlocXPos[0] = intBlocXPos[0];
						intBlocYPos[0] = intBlocYPos[0];
						intBlocXPos[1] = intBlocXPos[0];
						intBlocYPos[1] = intBlocYPos[0]-10;
						intBlocXPos[2] = intBlocXPos[0];
						intBlocYPos[2] = intBlocYPos[0]+10;
						intBlocXPos[3] = intBlocXPos[0]+10;
						intBlocYPos[3] = intBlocYPos[0]+10;
						break;
					case 3:
						intBlocXPos[0] = intBlocXPos[0];
						intBlocYPos[0] = intBlocYPos[0];
						intBlocXPos[1] = intBlocXPos[0]+10;
						intBlocYPos[1] = intBlocYPos[0];
						intBlocXPos[2] = intBlocXPos[0]-10;
						intBlocYPos[2] = intBlocYPos[0];
						intBlocXPos[3] = intBlocXPos[0]-10;
						intBlocYPos[3] = intBlocYPos[0]+10;
						break;
					case 4:
						intBlocXPos[0] = intBlocXPos[0];
						intBlocYPos[0] = intBlocYPos[0];
						intBlocXPos[1] = intBlocXPos[0];
						intBlocYPos[1] = intBlocYPos[0]+10;
						intBlocXPos[2] = intBlocXPos[0];
						intBlocYPos[2] = intBlocYPos[0]-10;
						intBlocXPos[3] = intBlocXPos[0]-10;
						intBlocYPos[3] = intBlocYPos[0]-10;
						break;
					default:
						break;
				}
					break;
				case 3:
				switch(intCurrentShapePosition)
				{
					case 1:
						intBlocXPos[0] = intBlocXPos[0];
						intBlocYPos[0] = intBlocYPos[0];
						intBlocXPos[1] = intBlocXPos[0]-10;
						intBlocYPos[1] = intBlocYPos[0];
						intBlocXPos[2] = intBlocXPos[0]+10;
						intBlocYPos[2] = intBlocYPos[0];
						intBlocXPos[3] = intBlocXPos[0]-10;
						intBlocYPos[3] = intBlocYPos[0]-10;
						break;
					case 2:
						intBlocXPos[0] = intBlocXPos[0];
						intBlocYPos[0] = intBlocYPos[0];
						intBlocXPos[1] = intBlocXPos[0];
						intBlocYPos[1] = intBlocYPos[0]-10;
						intBlocXPos[2] = intBlocXPos[0];
						intBlocYPos[2] = intBlocYPos[0]+10;
						intBlocXPos[3] = intBlocXPos[0]+10;
						intBlocYPos[3] = intBlocYPos[0]-10;
						break;
					case 3:
						intBlocXPos[0] = intBlocXPos[0];
						intBlocYPos[0] = intBlocYPos[0];
						intBlocXPos[1] = intBlocXPos[0]+10;
						intBlocYPos[1] = intBlocYPos[0];
						intBlocXPos[2] = intBlocXPos[0]-10;
						intBlocYPos[2] = intBlocYPos[0];
						intBlocXPos[3] = intBlocXPos[0]+10;
						intBlocYPos[3] = intBlocYPos[0]+10;
						break;
					case 4:
						intBlocXPos[0] = intBlocXPos[0];
						intBlocYPos[0] = intBlocYPos[0];
						intBlocXPos[1] = intBlocXPos[0];
						intBlocYPos[1] = intBlocYPos[0]+10;
						intBlocXPos[2] = intBlocXPos[0];
						intBlocYPos[2] = intBlocYPos[0]-10;
						intBlocXPos[3] = intBlocXPos[0]-10;
						intBlocYPos[3] = intBlocYPos[0]+10;
						break;
					default:
						break;
				}
					break;
				case 5:
				switch(intCurrentShapePosition)
				{
					case 1:
						intBlocXPos[0] = intBlocXPos[0];
						intBlocYPos[0] = intBlocYPos[0];
						intBlocXPos[1] = intBlocXPos[0];
						intBlocYPos[1] = intBlocYPos[0]-10;
						intBlocXPos[2] = intBlocXPos[0];
						intBlocYPos[2] = intBlocYPos[0]-20;
						intBlocXPos[3] = intBlocXPos[0];
						intBlocYPos[3] = intBlocYPos[0]-30;
						break;
					case 2:
						intBlocXPos[0] = intBlocXPos[0];
						intBlocYPos[0] = intBlocYPos[0];
						intBlocXPos[1] = intBlocXPos[0]+10;
						intBlocYPos[1] = intBlocYPos[0];
						intBlocXPos[2] = intBlocXPos[0]+20;
						intBlocYPos[2] = intBlocYPos[0];
						intBlocXPos[3] = intBlocXPos[0]+30;
						intBlocYPos[3] = intBlocYPos[0];
						break;
					case 3:
						intBlocXPos[0] = intBlocXPos[0];
						intBlocYPos[0] = intBlocYPos[0];
						intBlocXPos[1] = intBlocXPos[0];
						intBlocYPos[1] = intBlocYPos[0]+10;
						intBlocXPos[2] = intBlocXPos[0];
						intBlocYPos[2] = intBlocYPos[0]+20;
						intBlocXPos[3] = intBlocXPos[0];
						intBlocYPos[3] = intBlocYPos[0]+30;
						break;
					case 4:
						intBlocXPos[0] = intBlocXPos[0];
						intBlocYPos[0] = intBlocYPos[0];
						intBlocXPos[1] = intBlocXPos[0]-10;
						intBlocYPos[1] = intBlocYPos[0];
						intBlocXPos[2] = intBlocXPos[0]-20;
						intBlocYPos[2] = intBlocYPos[0];
						intBlocXPos[3] = intBlocXPos[0]-30;
						intBlocYPos[3] = intBlocYPos[0];
						break;
					default:
						break;
				}
					break;
				default:
					break;
			}
		}
	}
}
