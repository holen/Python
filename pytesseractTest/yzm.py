#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-11-27 14:40:01
# @Author  : zhl (zhl@qianbitou.cn)

# require
# https://github.com/tesseract-ocr/tesseract
# yum install tesseract
# pip install pytesseract

import pytesseract
from PIL import Image

image = Image.open("test.png")
code = pytesseract.image_to_string(image)
print(code)
