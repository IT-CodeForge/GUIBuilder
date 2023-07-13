using System;
using System.Drawing;
using System.Collections;
using System.ComponentModel;
using System.Windows.Forms;
using System.Data.SqlTypes;

namespace CSharp_Tetris
{
	/// <summary>
	/// GUI.
	/// </summary>
	public class LayoutForm : System.Windows.Forms.Form
	{
		private System.Windows.Forms.Panel animationCanvas;
		private System.ComponentModel.IContainer components;


		int animCanvasWidth;
		int animCanvasHeight;
		
		Rectangle r;
		Rectangle[] rctShape;
		Shape shpShape;
		Shape shpNextShape;
		private SolidBrush[][] arrBrushes = new SolidBrush[30][];
		private SolidBrush[] arrBrushColors = new SolidBrush[5];
		private int intShapeType;
		private int intNextShapeType;
		private Random rndShapeType = new Random();
		private bool bolIsRowFull;
		private bool bolIsDropped = false;


		// make a reference to our GameGrid
		private GameGrid grdGameGrid;
		private int intNumberOfRows;
		private int intNumberOfCols;
		private SolidBrush[][] arrGameGridBrushes;
		private SolidBrush[] arrBrushColours;
		private System.Windows.Forms.Timer GameTimer;
		private Rectangle[][] rctGameGrid;
		private int intDropRate;
		private System.Windows.Forms.Panel bonusCanvas;
		private int intGameSpeed;
		private int intBonusHeight;
		private Screen scrMainScreen;
		private Screen scrBonusScreen;
		private Screen scrStartScreen;
		private Screen scrNextShape;
		private System.Windows.Forms.Label label1;
		private System.Windows.Forms.Label lblScore;
		private System.Windows.Forms.Label label2;
		private System.Windows.Forms.Label lblLevel;
		private int intBonusStep;
		private long lngScore;
		private int intLevel;
		private System.Windows.Forms.Label label3;
		private System.Windows.Forms.Label lblRows;
		private int intLevelRowsCompleted;
		private System.Windows.Forms.Panel panel1;
		private System.Windows.Forms.Label label5;
		private System.Windows.Forms.Label label6;
		private System.Windows.Forms.Label label7;
		private System.Windows.Forms.Label label8;
		private System.Windows.Forms.Label label9;
		private System.Windows.Forms.Label label10;
		private System.Windows.Forms.Label label11;
		private int intTotalRowsCompleted;
		private System.Windows.Forms.Label label12;
		private System.Windows.Forms.Panel nextShape;
		private bool bolIsGameOver;
		private System.Windows.Forms.Label label4;
		private bool bolIsGamePaused;

		public LayoutForm()
		{
			//
			// Required for Windows Form Designer support
			//
			InitializeComponent();

			//
			// TODO: Add any constructor code after InitializeComponent call
			//

			SetUpGame();
		}

		/// <summary>
		/// Clean up any resources being used.
		/// </summary>
		protected override void Dispose( bool disposing )
		{
			if( disposing )
			{
				if(components != null)
				{
					components.Dispose();
				}
			}
			base.Dispose( disposing );
		}

		#region Windows Form Designer generated code
		/// <summary>
		/// Required method for Designer support - do not modify
		/// the contents of this method with the code editor.
		/// </summary>
		private void InitializeComponent()
		{
			this.components = new System.ComponentModel.Container();
			this.GameTimer = new System.Windows.Forms.Timer(this.components);
			this.lblScore = new System.Windows.Forms.Label();
			this.bonusCanvas = new System.Windows.Forms.Panel();
			this.nextShape = new System.Windows.Forms.Panel();
			this.label11 = new System.Windows.Forms.Label();
			this.label10 = new System.Windows.Forms.Label();
			this.label12 = new System.Windows.Forms.Label();
			this.label8 = new System.Windows.Forms.Label();
			this.label9 = new System.Windows.Forms.Label();
			this.label4 = new System.Windows.Forms.Label();
			this.label5 = new System.Windows.Forms.Label();
			this.label6 = new System.Windows.Forms.Label();
			this.label7 = new System.Windows.Forms.Label();
			this.lblLevel = new System.Windows.Forms.Label();
			this.label1 = new System.Windows.Forms.Label();
			this.label2 = new System.Windows.Forms.Label();
			this.label3 = new System.Windows.Forms.Label();
			this.lblRows = new System.Windows.Forms.Label();
			this.panel1 = new System.Windows.Forms.Panel();
			this.animationCanvas = new System.Windows.Forms.Panel();
			this.panel1.SuspendLayout();
			this.SuspendLayout();
			// 
			// GameTimer
			// 
			this.GameTimer.Tick += new System.EventHandler(this.GameTimer_Tick);
			// 
			// lblScore
			// 
			this.lblScore.AutoSize = true;
			this.lblScore.Location = new System.Drawing.Point(248, 8);
			this.lblScore.Name = "lblScore";
			this.lblScore.Size = new System.Drawing.Size(10, 13);
			this.lblScore.TabIndex = 3;
			this.lblScore.Text = "0";
			// 
			// bonusCanvas
			// 
			this.bonusCanvas.BackColor = System.Drawing.SystemColors.WindowText;
			this.bonusCanvas.Location = new System.Drawing.Point(176, 8);
			this.bonusCanvas.Name = "bonusCanvas";
			this.bonusCanvas.Size = new System.Drawing.Size(10, 301);
			this.bonusCanvas.TabIndex = 1;
			// 
			// nextShape
			// 
			this.nextShape.BackColor = System.Drawing.SystemColors.ControlText;
			this.nextShape.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
			this.nextShape.Location = new System.Drawing.Point(248, 96);
			this.nextShape.Name = "nextShape";
			this.nextShape.Size = new System.Drawing.Size(61, 67);
			this.nextShape.TabIndex = 7;
			// 
			// label11
			// 
			this.label11.Font = new System.Drawing.Font("Tahoma", 6.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((System.Byte)(0)));
			this.label11.Location = new System.Drawing.Point(8, 104);
			this.label11.Name = "label11";
			this.label11.Size = new System.Drawing.Size(104, 11);
			this.label11.TabIndex = 1;
			this.label11.Text = "<P> - Pause/Un-pause";
			// 
			// label10
			// 
			this.label10.Font = new System.Drawing.Font("Tahoma", 6.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((System.Byte)(0)));
			this.label10.Location = new System.Drawing.Point(8, 120);
			this.label10.Name = "label10";
			this.label10.Size = new System.Drawing.Size(96, 11);
			this.label10.TabIndex = 1;
			this.label10.Text = "<Q> - Restart";
			// 
			// label12
			// 
			this.label12.Location = new System.Drawing.Point(192, 112);
			this.label12.Name = "label12";
			this.label12.Size = new System.Drawing.Size(48, 32);
			this.label12.TabIndex = 8;
			this.label12.Text = "NEXT SHAPE";
			this.label12.TextAlign = System.Drawing.ContentAlignment.MiddleRight;
			// 
			// label8
			// 
			this.label8.AutoSize = true;
			this.label8.Font = new System.Drawing.Font("Tahoma", 6.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((System.Byte)(0)));
			this.label8.Location = new System.Drawing.Point(8, 72);
			this.label8.Name = "label8";
			this.label8.Size = new System.Drawing.Size(77, 11);
			this.label8.TabIndex = 1;
			this.label8.Text = "<A> - Rotate Left";
			// 
			// label9
			// 
			this.label9.Font = new System.Drawing.Font("Tahoma", 6.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((System.Byte)(0)));
			this.label9.Location = new System.Drawing.Point(8, 88);
			this.label9.Name = "label9";
			this.label9.Size = new System.Drawing.Size(96, 11);
			this.label9.TabIndex = 1;
			this.label9.Text = "<K> - Rotate Right";
			// 
			// label4
			// 
			this.label4.Font = new System.Drawing.Font("Tahoma", 6.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((System.Byte)(0)));
			this.label4.Location = new System.Drawing.Point(8, 24);
			this.label4.Name = "label4";
			this.label4.Size = new System.Drawing.Size(104, 16);
			this.label4.TabIndex = 1;
			this.label4.Text = "<SPACE> - Drop Shape";
			// 
			// label5
			// 
			this.label5.Font = new System.Drawing.Font("Tahoma", 6.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((System.Byte)(0)));
			this.label5.Location = new System.Drawing.Point(8, 8);
			this.label5.Name = "label5";
			this.label5.Size = new System.Drawing.Size(104, 16);
			this.label5.TabIndex = 1;
			this.label5.Text = "<ENTER> - Start Game";
			// 
			// label6
			// 
			this.label6.AutoSize = true;
			this.label6.Font = new System.Drawing.Font("Tahoma", 6.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((System.Byte)(0)));
			this.label6.Location = new System.Drawing.Point(8, 40);
			this.label6.Name = "label6";
			this.label6.Size = new System.Drawing.Size(71, 11);
			this.label6.TabIndex = 1;
			this.label6.Text = "<Z> - Move Left";
			// 
			// label7
			// 
			this.label7.Font = new System.Drawing.Font("Tahoma", 6.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((System.Byte)(0)));
			this.label7.Location = new System.Drawing.Point(8, 56);
			this.label7.Name = "label7";
			this.label7.Size = new System.Drawing.Size(104, 16);
			this.label7.TabIndex = 1;
			this.label7.Text = "<M> - Move Right";
			// 
			// lblLevel
			// 
			this.lblLevel.AutoSize = true;
			this.lblLevel.Location = new System.Drawing.Point(248, 40);
			this.lblLevel.Name = "lblLevel";
			this.lblLevel.Size = new System.Drawing.Size(10, 13);
			this.lblLevel.TabIndex = 3;
			this.lblLevel.Text = "1";
			// 
			// label1
			// 
			this.label1.AutoSize = true;
			this.label1.Location = new System.Drawing.Point(200, 8);
			this.label1.Name = "label1";
			this.label1.Size = new System.Drawing.Size(48, 13);
			this.label1.TabIndex = 2;
			this.label1.Text = "SCORE:";
			// 
			// label2
			// 
			this.label2.AutoSize = true;
			this.label2.Location = new System.Drawing.Point(205, 40);
			this.label2.Name = "label2";
			this.label2.Size = new System.Drawing.Size(43, 13);
			this.label2.TabIndex = 4;
			this.label2.Text = "LEVEL:";
			// 
			// label3
			// 
			this.label3.AutoSize = true;
			this.label3.Location = new System.Drawing.Point(205, 72);
			this.label3.Name = "label3";
			this.label3.Size = new System.Drawing.Size(43, 13);
			this.label3.TabIndex = 5;
			this.label3.Text = "ROWS:";
			// 
			// lblRows
			// 
			this.lblRows.AutoSize = true;
			this.lblRows.Location = new System.Drawing.Point(248, 72);
			this.lblRows.Name = "lblRows";
			this.lblRows.Size = new System.Drawing.Size(10, 13);
			this.lblRows.TabIndex = 6;
			this.lblRows.Text = "0";
			// 
			// panel1
			// 
			this.panel1.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
			this.panel1.Controls.AddRange(new System.Windows.Forms.Control[] {
																				 this.label4,
																				 this.label11,
																				 this.label10,
																				 this.label9,
																				 this.label8,
																				 this.label7,
																				 this.label6,
																				 this.label5});
			this.panel1.Location = new System.Drawing.Point(192, 165);
			this.panel1.Name = "panel1";
			this.panel1.Size = new System.Drawing.Size(120, 144);
			this.panel1.TabIndex = 7;
			// 
			// animationCanvas
			// 
			this.animationCanvas.BackColor = System.Drawing.SystemColors.WindowText;
			this.animationCanvas.Location = new System.Drawing.Point(8, 8);
			this.animationCanvas.Name = "animationCanvas";
			this.animationCanvas.Size = new System.Drawing.Size(161, 301);
			this.animationCanvas.TabIndex = 0;
			// 
			// LayoutForm
			// 
			this.AutoScaleBaseSize = new System.Drawing.Size(5, 13);
			this.ClientSize = new System.Drawing.Size(320, 325);
			this.Controls.AddRange(new System.Windows.Forms.Control[] {
																		  this.bonusCanvas,
																		  this.label12,
																		  this.nextShape,
																		  this.panel1,
																		  this.lblRows,
																		  this.label3,
																		  this.lblLevel,
																		  this.label2,
																		  this.lblScore,
																		  this.label1,
																		  this.animationCanvas});
			this.MaximizeBox = false;
			this.MinimizeBox = false;
			this.Name = "LayoutForm";
			this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
			this.Text = "C#RIS";
			this.KeyDown += new System.Windows.Forms.KeyEventHandler(this.LayoutForm_KeyDown);
			this.Load += new System.EventHandler(this.LayoutForm_Load);
			this.Paint += new System.Windows.Forms.PaintEventHandler(this.LayoutForm_Paint);
			this.panel1.ResumeLayout(false);
			this.ResumeLayout(false);

		}
		#endregion

		private void LayoutForm_Load(object sender, System.EventArgs e)
		{
		}
		public static void Main(string[] args)
		{
			Application.Run(new LayoutForm());
		}
		private void DrawScreen()
		{
			Graphics g = scrMainScreen.GetGraphics();
			arrGameGridBrushes = grdGameGrid.GetGameGridBrushes();
			arrBrushColours = grdGameGrid.GetShapeColours();
			rctGameGrid = grdGameGrid.GetGameGrid();
			scrMainScreen.erase();
			// draw the stationary shapes first
			for (int i=0;i<intNumberOfRows;i++)
			{
				for (int k=0;k<intNumberOfCols;k++)
				{
					if (!grdGameGrid.IsGridLocationEmpty(i,k))
					{
						g.FillRectangle(arrGameGridBrushes[i][k],rctGameGrid[i][k]);
						g.DrawRectangle(new Pen(Color.White,1),rctGameGrid[i][k]);
					}
				}
			}
			// now draw the moving shape
			for (int j=0;j<rctShape.Length;j++)
			{
				g.FillRectangle(arrBrushColours[intShapeType-1],rctShape[j]);
				g.DrawRectangle(new Pen(Color.White,1),rctShape[j]);
			}

			
			scrMainScreen.flip();
			intBonusStep--;
			if (intBonusStep == 0) 
			{
				intBonusStep = 5;
				if (!bolIsDropped)
				{
					DrawBonus(intBonusHeight -= 2);
				}
			}
		}
		private void LayoutForm_Paint(object sender, System.Windows.Forms.PaintEventArgs e)
		{
			DrawBonus(300);
			DrawStart();
		}
		private void LayoutForm_KeyDown(object sender, System.Windows.Forms.KeyEventArgs e)
		{
			string strKeyPress = null;
			strKeyPress = e.KeyCode.ToString();
			if (!bolIsGameOver)
			{
				switch(strKeyPress.ToUpper())
				{
					case "Z":
						if (shpShape.bolShapeMoving) rctShape = shpShape.moveShapeLeft(10, grdGameGrid.GetGameGrid());
						break;
					case "M":
						if (shpShape.bolShapeMoving) rctShape = shpShape.moveShapeRight(10, grdGameGrid.GetGameGrid());
						break;
					case "K":
						if (shpShape.bolShapeMoving) rctShape = shpShape.FlipShape("right", grdGameGrid.GetGameGrid());
						break;
					case "A":
						if (shpShape.bolShapeMoving) rctShape = shpShape.FlipShape("left", grdGameGrid.GetGameGrid());
						break;
					case "Q":
						GameTimer.Stop();
						SetUpGame();
						DrawBonus(300);
						DrawStart();
						break;
					case "P":
						if (!bolIsGamePaused)
						{
							GameTimer.Stop();
							bolIsGamePaused = true;
						}
						else
						{
							GameTimer.Start();
							bolIsGamePaused = false;
						}
						break;
					case "SPACE":
						if (shpShape.bolShapeMoving)
						{
							GameTimer.Interval = intDropRate;
							bolIsDropped = true;
						}
						break;
					default:
						break;
				}
			}
			else
			{
				switch(strKeyPress.ToUpper())
				{
					// for Beta 2, this is case "RETURN"
					case "ENTER":
						// create a shape to start with
						SetUpGame();
						intShapeType = GetShapeType();
						shpShape = new Shape(intShapeType,scrMainScreen.screenWidth, scrMainScreen.screenHeight, false);
						intNextShapeType = GetShapeType();
						shpNextShape = new Shape(intNextShapeType,scrNextShape.screenWidth, scrNextShape.screenHeight, true);
						shpShape.bolShapeMoving = true;
						bolIsGameOver = false;
						GameTimer.Interval = intGameSpeed;
						GameTimer.Enabled = true;
						GameTimer.Start();
						DrawNextShape();
						break;
					default:
						break;
				}
			}
		}

		private void GameTimer_Tick(object sender, System.EventArgs e)
		{
			if (shpShape.bolShapeMoving) 
			{
				rctShape = shpShape.moveShapeDown(intDropRate, grdGameGrid.GetGameGrid());
				DrawScreen();
			}
			else
			{
				int intXCoordinate;
				int intYCoordinate;
				// the current shape has stopped moving
				// is the shape within the game area? If not, then the game is over
				for (int i=0;i<4;i++)
				{
					if (!r.Contains(rctShape[i]))
					{
						bolIsGameOver = true;
						break;
					}
				}
				if (!bolIsGameOver)
				{
					int[] intYCoordinates = new int[4];
					// paint the shape's final position
					for (int i=0;i<4;i++)
					{
						intXCoordinate = rctShape[i].X;
						intYCoordinate = rctShape[i].Y;
						intYCoordinates[i] = intYCoordinate/10;
						// copy the shape's position into the game grid array
						grdGameGrid.SetShapeLocation(intYCoordinate/10,intXCoordinate/10,rctShape[i],intShapeType);
					}
					// this sorts the array of our Y coordinates so that we go from small to large
					// this enures that we drop rwos sequentially
					Array.Sort(intYCoordinates);
					for (int i=0;i<4;i++)
					{
						bolIsRowFull = true;
						// check to see if the shape causes an entire row to fill
						// if it does then we need to eliminate the row and drop the rest down
						for (int j=0;j<intNumberOfCols;j++)
						{
							if (grdGameGrid.IsGridLocationEmpty(intYCoordinates[i],j))
							{
								bolIsRowFull = false;
								break;
							}
						}
						if (bolIsRowFull)
						{
							// drop the row and fill from the next row down
							for (int k=intYCoordinates[i];k>0;k--)
							{
								// need to update all the coordinates of our shapes
								for (int l=0;l<intNumberOfCols;l++)
								{
									// set the value into the row below
									grdGameGrid.DropRowsDown(k,l);
								}
							}
							// need to do row 0
							grdGameGrid.SetTopRow();
							// update the score
							UpdateScore(intYCoordinates[i]);
							intBonusHeight = animationCanvas.Height-1;
							intBonusStep = 5;
							DrawBonus(intBonusHeight);
						}
					}
					intShapeType = intNextShapeType;
					shpShape = new Shape(intShapeType,scrMainScreen.screenWidth, scrMainScreen.screenHeight, false);
					intNextShapeType = GetShapeType();
					shpNextShape = new Shape(intNextShapeType,scrNextShape.screenWidth, scrNextShape.screenHeight, true);
					shpShape.bolShapeMoving = true;
					DrawNextShape();
					// reset the game speed
					GameTimer.Interval = intGameSpeed;
					bolIsDropped = false;
				}
				else
				{
					GameTimer.Stop();
				//	SetUpGame();
					DrawGameOver();
				}
			}
		}

		private void DrawBonus(int intHeight)
		{
			Graphics g2 = scrBonusScreen.GetGraphics();
			scrBonusScreen.erase();
			// draw bonus window
			g2.FillRectangle(new SolidBrush(Color.CornflowerBlue),0,0,9,intHeight);
			g2.DrawRectangle(new Pen(Color.White,1),0,0,9,300);
			g2.DrawString("B",new Font("Courier",6),new SolidBrush(Color.Red),1,5);
			g2.DrawString("O",new Font("Courier",6),new SolidBrush(Color.Red),1,15);
			g2.DrawString("N",new Font("Courier",6),new SolidBrush(Color.Red),1,25);
			g2.DrawString("U",new Font("Courier",6),new SolidBrush(Color.Red),1,35);
			g2.DrawString("S",new Font("Courier",6),new SolidBrush(Color.Red),1,45);
			g2.DrawString("S",new Font("Courier",6),new SolidBrush(Color.Red),1,60);
			g2.DrawString("C",new Font("Courier",6),new SolidBrush(Color.Red),1,70);
			g2.DrawString("O",new Font("Courier",6),new SolidBrush(Color.Red),1,80);
			g2.DrawString("R",new Font("Courier",6),new SolidBrush(Color.Red),1,90);
			g2.DrawString("E",new Font("Courier",6),new SolidBrush(Color.Red),1,100);
			scrBonusScreen.flip();
		}
		private void DrawStart()
		{
			Graphics gStart = scrStartScreen.GetGraphics();
			scrStartScreen.erase();
			// draw "C#RIS"
			// draw "C"
			gStart.FillRectangle(new SolidBrush(Color.Blue),34,100,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),34,100,5,5);
			gStart.FillRectangle(new SolidBrush(Color.Blue),39,100,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),39,100,5,5);

			gStart.FillRectangle(new SolidBrush(Color.Blue),29,105,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),29,105,5,5);

			gStart.FillRectangle(new SolidBrush(Color.Blue),29,110,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),29,110,5,5);

			gStart.FillRectangle(new SolidBrush(Color.Blue),29,115,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),29,115,5,5);

			gStart.FillRectangle(new SolidBrush(Color.Blue),34,120,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),34,120,5,5);
			gStart.FillRectangle(new SolidBrush(Color.Blue),39,120,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),39,120,5,5);
			
			//draw "#"
			gStart.FillRectangle(new SolidBrush(Color.Blue),54,100,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),54,100,5,5);
			gStart.FillRectangle(new SolidBrush(Color.Blue),64,100,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),64,100,5,5);

			gStart.FillRectangle(new SolidBrush(Color.Blue),49,105,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),49,105,5,5);
			gStart.FillRectangle(new SolidBrush(Color.Blue),54,105,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),54,105,5,5);
			gStart.FillRectangle(new SolidBrush(Color.Blue),59,105,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),59,105,5,5);
			gStart.FillRectangle(new SolidBrush(Color.Blue),64,105,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),64,105,5,5);
			gStart.FillRectangle(new SolidBrush(Color.Blue),69,105,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),69,105,5,5);
			
			gStart.FillRectangle(new SolidBrush(Color.Blue),54,110,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),54,110,5,5);
			gStart.FillRectangle(new SolidBrush(Color.Blue),64,110,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),64,110,5,5);

			gStart.FillRectangle(new SolidBrush(Color.Blue),49,115,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),49,115,5,5);
			gStart.FillRectangle(new SolidBrush(Color.Blue),54,115,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),54,115,5,5);
			gStart.FillRectangle(new SolidBrush(Color.Blue),59,115,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),59,115,5,5);
			gStart.FillRectangle(new SolidBrush(Color.Blue),64,115,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),64,115,5,5);
			gStart.FillRectangle(new SolidBrush(Color.Blue),69,115,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),69,115,5,5);

			gStart.FillRectangle(new SolidBrush(Color.Blue),54,120,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),54,120,5,5);
			gStart.FillRectangle(new SolidBrush(Color.Blue),64,120,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),64,120,5,5);

			// draw "R"
			gStart.FillRectangle(new SolidBrush(Color.Red),79,100,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),79,100,5,5);
			gStart.FillRectangle(new SolidBrush(Color.Red),84,100,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),84,100,5,5);
			gStart.FillRectangle(new SolidBrush(Color.Red),89,100,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),89,100,5,5);

			gStart.FillRectangle(new SolidBrush(Color.Red),79,105,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),79,105,5,5);
			gStart.FillRectangle(new SolidBrush(Color.Red),89,105,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),89,105,5,5);

			gStart.FillRectangle(new SolidBrush(Color.Red),79,110,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),79,110,5,5);
			gStart.FillRectangle(new SolidBrush(Color.Red),84,110,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),84,110,5,5);

			gStart.FillRectangle(new SolidBrush(Color.Red),79,115,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),79,115,5,5);
			gStart.FillRectangle(new SolidBrush(Color.Red),89,115,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),89,115,5,5);

			gStart.FillRectangle(new SolidBrush(Color.Red),79,120,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),79,120,5,5);
			gStart.FillRectangle(new SolidBrush(Color.Red),89,120,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),89,120,5,5);

			// draw "I"
			gStart.FillRectangle(new SolidBrush(Color.Red),99,100,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),99,100,5,5);
			gStart.FillRectangle(new SolidBrush(Color.Red),104,100,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),104,100,5,5);
			gStart.FillRectangle(new SolidBrush(Color.Red),109,100,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),109,100,5,5);

			gStart.FillRectangle(new SolidBrush(Color.Red),104,105,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),104,105,5,5);

			gStart.FillRectangle(new SolidBrush(Color.Red),104,110,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),104,110,5,5);

			gStart.FillRectangle(new SolidBrush(Color.Red),104,115,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),104,115,5,5);

			gStart.FillRectangle(new SolidBrush(Color.Red),99,120,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),99,120,5,5);
			gStart.FillRectangle(new SolidBrush(Color.Red),104,120,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),104,120,5,5);
			gStart.FillRectangle(new SolidBrush(Color.Red),109,120,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),109,120,5,5);

			//draw "S"
			gStart.FillRectangle(new SolidBrush(Color.Red),119,100,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),119,100,5,5);
			gStart.FillRectangle(new SolidBrush(Color.Red),124,100,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),124,100,5,5);
			gStart.FillRectangle(new SolidBrush(Color.Red),129,100,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),129,100,5,5);

			gStart.FillRectangle(new SolidBrush(Color.Red),119,105,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),119,105,5,5);

			gStart.FillRectangle(new SolidBrush(Color.Red),119,110,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),119,110,5,5);
			gStart.FillRectangle(new SolidBrush(Color.Red),124,110,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),124,110,5,5);
			gStart.FillRectangle(new SolidBrush(Color.Red),129,110,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),129,110,5,5);

			gStart.FillRectangle(new SolidBrush(Color.Red),129,115,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),129,115,5,5);

			gStart.FillRectangle(new SolidBrush(Color.Red),119,120,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),119,120,5,5);
			gStart.FillRectangle(new SolidBrush(Color.Red),124,120,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),124,120,5,5);
			gStart.FillRectangle(new SolidBrush(Color.Red),129,120,5,5);
			gStart.DrawRectangle(new Pen(Color.White,1),129,120,5,5);

			scrStartScreen.flip();
		}
		private void UpdateScore(int intRowNum)
		{
			intLevelRowsCompleted++;
			intTotalRowsCompleted++;
			int intReverseRow = 30 - intRowNum;
			lngScore = lngScore + (intReverseRow * intLevelRowsCompleted * intLevel * 10) + (intBonusHeight * (intLevel * intLevelRowsCompleted));
			lblScore.Text = lngScore.ToString();
			if (intLevelRowsCompleted == 10)
			{
				UpdateLevel();
				intLevelRowsCompleted = 0;
			}
			lblRows.Text = intTotalRowsCompleted.ToString();
		}
		private void UpdateLevel()
		{
			intLevel++;
			if (intGameSpeed > 10) intGameSpeed -= 10;
			lblLevel.Text = intLevel.ToString();
		}
		private void SetUpGame()
		{
			// set initial variable values
			intGameSpeed = 100;
			intBonusHeight = animationCanvas.Height-1;
			intDropRate = 5;
			intBonusStep = 5;
			lngScore = 0;
			intLevel = 1;
			intLevelRowsCompleted = 0;
			intTotalRowsCompleted = 0;
			bolIsGameOver = true;
			bolIsDropped = false;

			lblScore.Text = lngScore.ToString();
			lblLevel.Text = intLevel.ToString();
			lblRows.Text = intTotalRowsCompleted.ToString();

			// create our main window
			r = new Rectangle(0,0,animationCanvas.Width, animationCanvas.Height);
			animCanvasWidth = r.Width;
			animCanvasHeight = r.Height;
			scrMainScreen = new Screen(animationCanvas, r);

			// create our bonus score window
			r = new Rectangle(0,0,bonusCanvas.Width, bonusCanvas.Height);
			scrBonusScreen = new Screen(bonusCanvas, r);

			//create our next shape window
			r = new Rectangle(0,0,nextShape.Width, nextShape.Height);
			scrNextShape = new Screen(nextShape, r);

			// create our start screen
			r = new Rectangle(0,0,animationCanvas.Width, animationCanvas.Height);
			scrStartScreen = new Screen(animationCanvas, r);

			// create the GameGrid
			intNumberOfRows = (animationCanvas.Height-1)/10;
			intNumberOfCols = (animationCanvas.Width-1)/10;
			grdGameGrid = new GameGrid(intNumberOfRows, intNumberOfCols);
		}
		private void DrawGameOver()
		{
			Graphics gOver = scrStartScreen.GetGraphics();
			scrStartScreen.erase();
			gOver.DrawString("GAME OVER",new Font("Courier",18),new SolidBrush(Color.Red),5,100);
			scrStartScreen.flip();
		}
		private void DrawNextShape()
		{
			Graphics g = scrNextShape.GetGraphics();
			Rectangle[] rctNextShape;
			rctNextShape = shpNextShape.GetShape();
			arrBrushColours = grdGameGrid.GetShapeColours();
			scrNextShape.erase();
			for (int j=0;j<4;j++)
			{
				g.FillRectangle(arrBrushColours[intNextShapeType-1],rctNextShape[j]);
				g.DrawRectangle(new Pen(Color.White,1),rctNextShape[j]);
			}
			scrNextShape.flip();
		}
		private int GetShapeType()
		{
			int intShapeType;
			do
			{
				intShapeType = rndShapeType.Next(6);
			}while (intShapeType == 0);
			return intShapeType;
		}
	}
}