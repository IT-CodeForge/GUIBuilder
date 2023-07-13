
using System;
using System.Drawing;

namespace CSharpXXRIS
{
	/// <summary>
	/// Layout des Spielfeldes, aufgeteilt in 10x10 Steine 
	/// </summary>
	
	public class GameGrid
	{
		private Rectangle[][] arrGameGrid;
		private SolidBrush[][] arrGameGridBrushes;
		private SolidBrush[] arrBrushColours;

		public GameGrid(int intGameGridRows, int intGameGridColumns)
		{
			arrGameGrid			= new Rectangle [intGameGridRows][];
			arrGameGridBrushes	= new SolidBrush[intGameGridRows][];
			arrBrushColours		= new SolidBrush[5];

			// erzeugen des GameGrid- und des GameGridBrush-Array
			for (int i=0;i<intGameGridRows;i++)
			{
				arrGameGrid[i]			= new Rectangle[intGameGridColumns];
				arrGameGridBrushes[i]	= new SolidBrush[intGameGridColumns];
			}
			// erzeugen des BrushColours-Array
			arrBrushColours[0] = new SolidBrush(Color.Blue);
			arrBrushColours[1] = new SolidBrush(Color.Red);
			arrBrushColours[2] = new SolidBrush(Color.Green);
			arrBrushColours[3] = new SolidBrush(Color.Yellow);
			arrBrushColours[4] = new SolidBrush(Color.Brown);
		}
		
		public Rectangle[][] GetGameGrid()
		{
			return arrGameGrid;
		}
		
		public SolidBrush[][] GetGameGridBrushes()
		{
			return arrGameGridBrushes;
		}
		
		public SolidBrush[] GetShapeColours()
		{
			return arrBrushColours;
		}
		
		public bool IsGridLocationEmpty(int intRowNumber, int intColNumber)
		{
			if (arrGameGrid[intRowNumber][intColNumber].IsEmpty)
			{
				return true;
			}
			else
			{
				return false;
			}
		}
		
		public void SetShapeLocation(int intRowNumber, int intColNumber, Rectangle rctSquare, int intShapeType)
		{
			arrGameGrid[intRowNumber][intColNumber] = rctSquare;
			SetShapeColourLocation(intRowNumber, intColNumber, intShapeType);
		}
		
		public void SetShapeColourLocation(int intRowNumber, int intColNumber, int intShapeType)
		{
			arrGameGridBrushes[intRowNumber][intColNumber] = arrBrushColours[intShapeType-1];
		}
		
		public void DropRowsDown(int intRowNumber, int intColNumber)
		{
			if (!IsGridLocationEmpty(intRowNumber-1, intColNumber))
			{
				arrGameGrid[intRowNumber][intColNumber] = new Rectangle(arrGameGrid[intRowNumber-1][intColNumber].X,
					arrGameGrid[intRowNumber-1][intColNumber].Y+10,10,10);
				arrGameGridBrushes[intRowNumber][intColNumber] = arrGameGridBrushes[intRowNumber-1][intColNumber];
			}
			else
			{
				arrGameGrid[intRowNumber][intColNumber] = arrGameGrid[intRowNumber-1][intColNumber];
			}
		}
		
		public void SetTopRow()
		{
			arrGameGrid[0] = new Rectangle[arrGameGrid[1].Length];
		}
	}
}

