using System;
using System.Drawing;

namespace CSharp_Tetris
{
	/// <summary>
	/// Layout of the game area. Divided into 10x10 blocks within a rows x cols array
	/// </summary>
	public class GameGrid
	{
		private Rectangle[][] arrGameGrid;
		private SolidBrush[][] arrGameGridBrushes;
		private SolidBrush[] arrBrushColours;

		public GameGrid(int intGameGridRows, int intGameGridColumns)
		{
			//
			// TODO: Add constructor logic here
			//
			arrGameGrid			= new Rectangle [intGameGridRows][];
			arrGameGridBrushes	= new SolidBrush[intGameGridRows][];
			arrBrushColours		= new SolidBrush[5];

			// create the GameGrid array and GameGridBrushes array
			for (int i=0;i<intGameGridRows;i++)
			{
				arrGameGrid[i]			= new Rectangle[intGameGridColumns];
				arrGameGridBrushes[i]	= new SolidBrush[intGameGridColumns];
			}
			// create the BrushColours array
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

