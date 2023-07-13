

namespace CSharp_Tetris
{
	using System;
	using System.Drawing;
	using System.Windows.Forms;
	/// <summary>
	/// Screen class manages offscreen graphics.
	/// Code reused and morphed from examples at www.extremetech.com
	/// </summary>
	public class Screen
	{
		protected Graphics g = null;
		protected Image imageOffScreen = null;
		protected Graphics graphicsOffScreen = null;

		public int screenX = 0;
		public int screenY = 0;
		public int screenWidth = 0;
		public int screenHeight = 0;

		public Screen(Panel p, Rectangle r)
		{
			//
			// TODO: Add constructor logic here
			//

			// get a visible screen
			g = p.CreateGraphics();
			screenX = r.X;
			screenY = r.Y;
			screenWidth = r.Width;
			screenHeight = r.Height;

			// get offscreen buffer context
			imageOffScreen = new Bitmap(screenWidth, screenHeight);
			graphicsOffScreen = Graphics.FromImage(imageOffScreen);
		}
		public Graphics GetGraphics()
		{
			return graphicsOffScreen;
		}
		public void erase()
		{
			// erase all content in back buffer by using background color
			if (!isValidGraphics())
			{
				return;
			}
			SolidBrush blackBrush = new SolidBrush(Color.Black);
			graphicsOffScreen.FillRectangle(blackBrush,0,0,screenWidth,screenHeight);
		}
		public void flip()
		{
			// flip buffers for smooth animation
			g.DrawImage(imageOffScreen,screenX,screenY);
		}
		public bool isValidGraphics()
		{
			if (g != null && graphicsOffScreen != null)
			{
				return true;
			}
			else
			{
				return false;
			}
		}
		public Screen()
		{
		}
	}
}


