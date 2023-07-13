
using System;
using System.Drawing;
using System.Windows.Forms;

namespace CSharpXXRIS
{
	/// <summary>
	/// Die Klasse Screen steuert die momentan nicht angezeigten Grafiken.
	/// Der Code stammt aus Beispielen von www.extremetech.com
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
		
		public Screen()
		{
		}

		public Screen(Panel p, Rectangle r)
		{
			
			// holen des sichtbaren Screens
			g = p.CreateGraphics();
			screenX = r.X;
			screenY = r.Y;
			screenWidth = r.Width;
			screenHeight = r.Height;

			// holen des Kontextes
			imageOffScreen = new Bitmap(screenWidth, screenHeight);
			graphicsOffScreen = Graphics.FromImage(imageOffScreen);
		}
		
		public Graphics GetGraphics()
		{
			return graphicsOffScreen;
		}
		
		public void erase()
		{
			if (!isValidGraphics())
			{
				return;
			}
			
			SolidBrush blackBrush = new SolidBrush(Color.Black);
			graphicsOffScreen.FillRectangle(blackBrush,0,0,screenWidth,screenHeight);
		}
		
		public void flip()
		{
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
	}
}


