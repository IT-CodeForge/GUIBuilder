#include "TGWBitmap.h"
#include "TGWindow.h"
#include "TGWCanvas.h"

TGWBitmap::TGWBitmap()
{
  hBitmap               = 0;
  bitmapAttributes      = {0};
  bitmapInfo            = {0};
  screenCompatibleMemDC = CreateCompatibleDC(NULL);  
}

TGWBitmap::~TGWBitmap()
{
  DeleteDC(screenCompatibleMemDC);
  
  if(hBitmap != 0) DeleteObject(hBitmap); 
  hBitmap = 0;
}

void TGWBitmap::paintBitmapToCanvas(TGWCanvas* einCanvas, int x , int y, bool transparent, int tansparantColor)
{
  // see http://www.winprog.org/tutorial/transparency.html
  if (hBitmap == 0) return;
  int cx = bitmapAttributes.bmWidth;
  int cy = bitmapAttributes.bmHeight;

  HDC actualDeviceContext     = einCanvas->getDeviceContext();
  HDC compatibleDeviceContext = CreateCompatibleDC(actualDeviceContext);

  if(transparent)
  { 
    SelectObject(compatibleDeviceContext, hBitmap);
    TransparentBlt(actualDeviceContext, x, y, cx, cy, compatibleDeviceContext,0,0, cx, cy, tansparantColor);
  }
  else
  {
    SelectObject(compatibleDeviceContext, hBitmap);
    BitBlt(actualDeviceContext, x, y, cx, cy, compatibleDeviceContext, 0, 0, SRCCOPY);
  }

  DeleteDC(compatibleDeviceContext);
}

TGWBitmapData TGWBitmap::getTGWBitmapData()
{
  if (hBitmap == 0) return TGWBitmapData();

  TGWBitmapData data;
  data.height      = bitmapAttributes.bmHeight;
  data.width       = bitmapAttributes.bmWidth;
  data.pixel       = new TGWPixel[data.width*data.height];

  // Kopieren des Bildinhalts in den Puffer
  GetDIBits(screenCompatibleMemDC, hBitmap, 0, bitmapAttributes.bmHeight, data.pixel, &bitmapInfo, DIB_RGB_COLORS);

  return data;
}

BITMAPINFO TGWBitmap::getBITMAPINFOfromBITMAP(BITMAP& bitmap)
{
  BITMAPINFO bmi = {0};
  bmi.bmiHeader.biSize = sizeof(BITMAPINFOHEADER);
  bmi.bmiHeader.biWidth = bitmap.bmWidth;
  bmi.bmiHeader.biHeight = -bitmap.bmHeight;  // Negative height to ensure top-down DIB
  bmi.bmiHeader.biPlanes = 1;
  bmi.bmiHeader.biBitCount = bitmap.bmBitsPixel;
  bmi.bmiHeader.biCompression = BI_RGB;
  return bmi;
}

int TGWBitmap::getWidth()
{
  if (hBitmap == 0) return 0;
  return bitmapAttributes.bmWidth;
}

int TGWBitmap::getHeight()
{
  if (hBitmap == 0) return 0;
  return bitmapAttributes.bmHeight;
}

bool TGWBitmap::getBMAttributesAndBMInfoFromHBitmap()
{
  if(!hBitmap) return false;
 
  GetObject(hBitmap, sizeof(bitmapAttributes), &bitmapAttributes); //The GetObject function retrieves information for the specified graphics object.
  bitmapInfo = getBITMAPINFOfromBITMAP(bitmapAttributes);

  return true;
}

bool TGWBitmap::loadFromFile(UString filename)
{
  //https://cboard.cprogramming.com/windows-programming/63546-[cplusplus-winapi]-changing-bitmap-contrast.html
  hBitmap = (HBITMAP) LoadImage( NULL, filename.c_str(),  IMAGE_BITMAP, 0, 0, LR_LOADFROMFILE);
  return getBMAttributesAndBMInfoFromHBitmap();
}

void TGWBitmap::setTGWBitmapData(TGWBitmapData tgwBitmapData)
{
  int bitPerPixel = sizeof(tgwBitmapData.pixel[0]) * 8; // AnzBytes * 8 Bit
  hBitmap = CreateBitmap(tgwBitmapData.width, tgwBitmapData.height, 1, bitPerPixel, tgwBitmapData.pixel);
  getBMAttributesAndBMInfoFromHBitmap();
}
