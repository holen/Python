#!/usr/bin/python
#-* coding: utf-8 -*

import cairo
def main():
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, 390, 60)
    cr = cairo.Context(ims)
 
    cr.set_source_rgb(0, 0, 0)
    cr.select_font_face("WenQuanYi Micro Hei Mono", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    cr.set_font_size(40)
         
    cr.move_to(10, 50)
    cr.show_text("我在厦门,hello !!")
    ims.write_to_png("image.png")
      
if __name__ == "__main__":
    main()    
