import ctypes
import os
from PIL import Image

LibName = 'prtscn.so'
AbsLibPath = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + LibName
grab = ctypes.CDLL(AbsLibPath)

def grab_screen(x1,y1,x2,y2):
    w, h = x2-x1, y2-y1
    size = w * h
    objlength = size * 3

    grab.getScreen.argtypes = []
    result = (ctypes.c_ubyte*objlength)()

    grab.getScreen(x1,y1, w, h, result)
    return Image.frombuffer('RGB', (w, h), result, 'raw', 'RGB', 0, 1)

if __name__ == '__main__':
  im = grab_screen(0,0,1440,900)
  im.show()

  '''
  #include <stdio.h>
#include <X11/X.h>
#include <X11/Xlib.h>
//Compile hint: gcc -shared -O3 -lX11 -fPIC -Wl,-soname,prtscn -o prtscn.so prtscn.c

void getScreen(const int, const int, const int, const int, unsigned char *);
void getScreen(const int xx,const int yy,const int W, const int H, /*out*/ unsigned char * data) 
{
   Display *display = XOpenDisplay(NULL);
   Window root = DefaultRootWindow(display);

   XImage *image = XGetImage(display,root, xx,yy, W,H, AllPlanes, ZPixmap);

   unsigned long red_mask   = image->red_mask;
   unsigned long green_mask = image->green_mask;
   unsigned long blue_mask  = image->blue_mask;
   int x, y;
   int ii = 0;
   for (y = 0; y < H; y++) {
       for (x = 0; x < W; x++) {
         unsigned long pixel = XGetPixel(image,x,y);
         unsigned char blue  = (pixel & blue_mask);
         unsigned char green = (pixel & green_mask) >> 8;
         unsigned char red   = (pixel & red_mask) >> 16;

         data[ii + 2] = blue;
         data[ii + 1] = green;
         data[ii + 0] = red;
         ii += 3;
      }
   }
   XDestroyImage(image);
   XDestroyWindow(display, root);
   XCloseDisplay(display);
}
  
  
  '''