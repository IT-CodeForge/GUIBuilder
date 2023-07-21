#ifndef _TGWBitmap_h_
#define _TGWBitmap_h_

#include <windows.h>
#include "UString.h"

#include "TGW_AllClassDeclarations.h"
struct TGWPixel
{
  BYTE b;
  BYTE g;
  BYTE r;
  BYTE unused;
};

class TGWBitmapData
{
public:
  TGWPixel* pixel;
  int       width;
  int       height;
 
  TGWBitmapData()
  {
    pixel       = 0;
    width       = 0;
    height      = 0;
  };

/*  No no no no no no no no no no no no no no no no no !
  TGWBitmapData(const TGWBitmapData & bd)
  {
    pixel = bd.pixel; // No copy of data at this point!
    width = bd.width;
    height = bd.height;
  };
*/

  TGWBitmapData(const TGWBitmapData & bd, UString cmd)
  {
    if(cmd != "copy") throw "Should be 'copy'!";
    this->copyFrom(bd);
  };

  TGWPixel& at(int x, int y){return pixel[x+y*width];};

  void copyFrom( const TGWBitmapData & bd)
  {
    if(pixel!=0) deletePixelData();
    pixel = 0;
    if(bd.pixel!=0)
    {
      pixel = new TGWPixel[bd.height*bd.width]; 
      memcpy(pixel, bd.pixel, bd.height*bd.width*sizeof(TGWPixel));
    }

    width=bd.width;
    height = bd.height;
  }

  void deletePixelData()
  {
    delete[] (BYTE*)pixel;
    pixel       = 0;
    width       = 0;
    height      = 0;
  }
};

class TGWBitmap
{
  HBITMAP     hBitmap;
  BITMAP      bitmapAttributes;
  BITMAPINFO  bitmapInfo;
  HDC         screenCompatibleMemDC;

public:
  TGWBitmap();
  virtual ~TGWBitmap();

  static BITMAPINFO getBITMAPINFOfromBITMAP(BITMAP& bitmap);

  int   getWidth();
  int   getHeight();
  bool  loadFromFile(UString filename);  // Returns success
  void  paintBitmapToCanvas(TGWCanvas* einCanvas, int x , int y, bool transparent=false, int tansparantColor = 0x000000);
  TGWBitmapData getTGWBitmapData(); // Allocates pixelData 
  void  setTGWBitmapData(TGWBitmapData tgwBitmapData);
  bool  getBMAttributesAndBMInfoFromHBitmap();
};

#endif