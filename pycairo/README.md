# ubuntu install cairo
apt-get install libcairo2-dev -y

# download py2cairo for python2.7
Download [py2cairo](http://cairographics.org/releases/py2cairo-1.10.0.tar.bz2) 
## install py2cairo

    tar jxvf py2cairo-1.10.0.tar.bz2  
    cd py2cairo-1.10.0  
    ./waf configure  
    ./waf configure  
    ./waf build  
    ./waf install

# test

    root@abc:/data/opensoft/py2cairo-1.10.0# python
    Python 2.7.3 (default, Sep 26 2013, 20:03:06) 
    [GCC 4.6.3] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import cairo
    >>> dir(cairo)
    ['ANTIALIAS_DEFAULT', 'ANTIALIAS_GRAY', 'ANTIALIAS_NONE', 'ANTIALIAS_SUBPIXEL', 'CAPI', 'CONTENT_ALPHA', 'CONTENT_COLOR', 'CONTENT_COLOR_ALPHA', 'Context', 'EXTEND_NONE', 'EXTEND_PAD', 'EXTEND_REFLECT', 'EXTEND_REPEAT', 'Error', 'FILL_RULE_EVEN_ODD', 'FILL_RULE_WINDING', 'FILTER_BEST', 'FILTER_BILINEAR', 'FILTER_FAST', 'FILTER_GAUSSIAN', 'FILTER_GOOD', 'FILTER_NEAREST', 'FONT_SLANT_ITALIC', 'FONT_SLANT_NORMAL', 'FONT_SLANT_OBLIQUE', 'FONT_WEIGHT_BOLD', 'FONT_WEIGHT_NORMAL', 'FORMAT_A1', 'FORMAT_A8', 'FORMAT_ARGB32', 'FORMAT_RGB24', 'FontFace', 'FontOptions', 'Gradient', 'HAS_ATSUI_FONT', 'HAS_FT_FONT', 'HAS_GLITZ_SURFACE', 'HAS_IMAGE_SURFACE', 'HAS_PDF_SURFACE', 'HAS_PNG_FUNCTIONS', 'HAS_PS_SURFACE', 'HAS_QUARTZ_SURFACE', 'HAS_SVG_SURFACE', 'HAS_USER_FONT', 'HAS_WIN32_FONT', 'HAS_WIN32_SURFACE', 'HAS_XCB_SURFACE', 'HAS_XLIB_SURFACE', 'HINT_METRICS_DEFAULT', 'HINT_METRICS_OFF', 'HINT_METRICS_ON', 'HINT_STYLE_DEFAULT', 'HINT_STYLE_FULL', 'HINT_STYLE_MEDIUM', 'HINT_STYLE_NONE', 'HINT_STYLE_SLIGHT', 'ImageSurface', 'LINE_CAP_BUTT', 'LINE_CAP_ROUND', 'LINE_CAP_SQUARE', 'LINE_JOIN_BEVEL', 'LINE_JOIN_MITER', 'LINE_JOIN_ROUND', 'LinearGradient', 'Matrix', 'OPERATOR_ADD', 'OPERATOR_ATOP', 'OPERATOR_CLEAR', 'OPERATOR_DEST', 'OPERATOR_DEST_ATOP', 'OPERATOR_DEST_IN', 'OPERATOR_DEST_OUT', 'OPERATOR_DEST_OVER', 'OPERATOR_IN', 'OPERATOR_OUT', 'OPERATOR_OVER', 'OPERATOR_SATURATE', 'OPERATOR_SOURCE', 'OPERATOR_XOR', 'PATH_CLOSE_PATH', 'PATH_CURVE_TO', 'PATH_LINE_TO', 'PATH_MOVE_TO', 'PDFSurface', 'PSSurface', 'PS_LEVEL_2', 'PS_LEVEL_3', 'Pattern', 'RadialGradient', 'SUBPIXEL_ORDER_BGR', 'SUBPIXEL_ORDER_DEFAULT', 'SUBPIXEL_ORDER_RGB', 'SUBPIXEL_ORDER_VBGR', 'SUBPIXEL_ORDER_VRGB', 'SVGSurface', 'ScaledFont', 'SolidPattern', 'Surface', 'SurfacePattern', 'ToyFontFace', 'XlibSurface', '__builtins__', '__doc__', '__file__', '__name__', '__package__', '__path__', '_cairo', 'cairo_version', 'cairo_version_string', 'version', 'version_info']

