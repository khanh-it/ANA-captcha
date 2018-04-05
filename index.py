from __future__ import print_function
import os
import sys
from PIL import Image as Img, ImageFilter  as ImgFilter
#
from pyocr.helpers import *

def pyocr(imgfile, debug=False):
    ''' Python OCR  '''
    # print(sys.argv, imgfile, os.path.isfile(imgfile))
    #
    if not os.path.isfile(imgfile):
        raise 'Image filename not found!'
    #
    chars = img_split_chars(imgfile)
    #
    digits = ''
    charcnt = 0
    for char in chars:
        charcnt += 1
        if  debug: char.show()
        cnt_max_by_char = ocr(char, debug=False)
        print(str(charcnt) +  '#cnt_max_by_char: ', cnt_max_by_char)
        digits += cnt_max_by_char[-1]
    #endfor
    return digits
#endef

#
imgfile = sys.argv[1] if len(sys.argv[1]) >= 1 else ''
if imgfile:
    digits = pyocr(imgfile, debug=False)
    print(digits)
#endif
