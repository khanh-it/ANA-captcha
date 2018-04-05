from __future__ import print_function
import os
import sys
import json
import urllib
import random
import time
import hashlib
from PIL import Image as Img, ImageFilter  as ImgFilter

# captcha url
CAPTCHA_URL = 'https://aswbe-d.ana.co.jp/9Eile48/dms/red21o/dyc/be/kaptcha.jpg'

#
md5 = hashlib.md5()

# 
COLOR_WHITE = 255
# Input image crop specs
IMG_CROP = {'L' : 100, 'T' : 25, 'R' : 330, 'B' : 85}
IMG_CHAR = {
    'CNT' : 5,
    'MIN_WIDTH': 26,
    'MAX_WIDTH': 38
}
    
def dirname():
    '''  '''
    # return os.path.dirname(os.path.realpath(sys.argv[0]))
    return os.path.dirname(__file__)
#endef

def current_milli_time():
    ''' Current miliseconds!  '''
    return int(round(time.time() * 1000))
#endef

def rand_digit_str():
    ''' Random digit string! '''
    mili = current_milli_time()
    rstr = str(random.randrange(1, 1000))
    return str(mili) + '_' + rstr
#endef

def captcha_download(folder='./data/captcha'):
    ''' Download captcha helper!
    '''
    file_name = rand_digit_str() + '.jpg'
    full_file_name = str(folder) + '/' + file_name
    urllib.urlretrieve(CAPTCHA_URL, full_file_name)
#endef
    
def img_save(img, filename=None, mode='bmp'):
    ''' Save output image!
    '''
    mode = str(mode).lower()
    filename = filename + ('.'  + mode)
    img.save(filename, mode)
    return filename
#endef

def img_normalizer(filename, save_filename=None, debug=False):
    ''' Normalize input image (remove symbols, effects)!
    '''
    # open image file
    img = filename if isinstance(filename, Img.Image) else Img.open(filename)
    # convert image to black/white mode
    img = img.convert('1')
    # remove image effects
    img = img.filter(ImgFilter.BLUR)
    # img = img.filter(ImgFilter.SMOOTH)
    # black or white only
    mincolor, maxcolor = img.getextrema()
    for x in range(img.width):
        for y in range(img.height):
            pixel = (x, y)
            color = img.getpixel(pixel)
            if color > mincolor:
                img.putpixel(pixel, COLOR_WHITE)
    #endfor
    # crop blank spaces
    img = img.crop((
        IMG_CROP['L'], # left
        IMG_CROP['T'], # upper
        IMG_CROP['R'], # right
        IMG_CROP['B'] # lower
    ))
    #
    img = img_remove_lines(img)
    # Save image?
    if save_filename is not None: img_save(save_filename)
    # Return
    return img
#endef

def img_spaces_inline(img, x):
    nonwhite_y = None
    spaces = []
    for y in range(img.height):
        pixel = (x, y)
        color = img.getpixel(pixel)
        if color != COLOR_WHITE:
            if nonwhite_y is None:
                spaces.append([])
                nonwhite_y = y
            #endif
            space = len(spaces) and spaces[len(spaces) - 1]
            if isinstance(space, list):
                space.append(y)
        else:
            nonwhite_y = None
        #endif
    #endfor
    return spaces
#endef

def img_cal_char_cords(filename, debug=False,maxpixel=0):
    ''' Calculate characters cordinates from input image!
    '''
    lines = {}
    cords = []
    char_x = None
    # open image file
    img = filename if isinstance(filename, Img.Image) else Img.open(filename)
    for x in range(img.width):
        lines[x] = 0
        for y in range(img.height):
            color = img.getpixel((x, y))
            lines[x] += 1 if (color != COLOR_WHITE) else 0
        #endfor
        #
        line_empty = lines[x] <= maxpixel
        if not line_empty:
            if char_x is None: char_x = x
        else:
            if char_x is not None:
                width = x - char_x
                if (width >= IMG_CHAR['MIN_WIDTH']):
                    cords.append((char_x, x, width))
                    char_x = None
    #endfor
    if debug: print(cords)
    return cords
#endef

def img_remove_lines(img, debug=False):
    ''' '''
    cords = img_cal_char_cords(img)
    print(cords)
    for x1, x2, wi in cords:
        if wi > IMG_CHAR['MAX_WIDTH']:
            for x in range(x1, x2 + 1):
                width = x - x1
                if width <= IMG_CHAR['MIN_WIDTH']: continue
                spaces = img_spaces_inline(img, x)
                slen = len(spaces)
                if slen != 1: continue
                ylist = spaces[0]
                slen = len(ylist)
                if slen >= 10: continue
                if ylist[0] <= (img.height / 2): continue
                if debug: print('x: ' + str(x) + ' has spaces: ', len(ylist), ylist)
                for y in ylist:
                    img.putpixel((x, y), COLOR_WHITE)
            #endfor
        #endif
    #endfor
    return img
#endef

def img_split_chars(filename, debug=False):
    ''' Find (and split) chars from input image!
    '''
    img = img_normalizer(filename)
    #
    for maxpixel in range(3):
        chars = []
        cords = img_cal_char_cords(img, debug,maxpixel)
        for x1, x2, w in cords:
            char = img.crop((
                x1, # left
                0, # upper
                x2, # right
                img.height # lower
            ))
            chars.append(char)
        #endfor
        if len(chars) == IMG_CHAR['CNT']: break
    else:
        chars = []
    #endfor
    if debug:
        for char in chars:
            char.show()
        #endfor
        img.show()
    return chars
#endef

def img_to_trained_json(filename, debug=False):
    ''' Convert inpurt image to json data!
    '''
    pixels = {}
    img = filename if isinstance(filename, Img.Image) else Img.open(filename)
    if debug: print(filename)
    for x in range(img.width):
        if debug: print('[', end='')
        for y in range(img.height):
            color = img.getpixel((x, y))
            if debug: print('o' if color >= 100 else '#', end='')
            if color != COLOR_WHITE:
                pixels['%s:%s' % (x, y)] = color
            #endif
        #endfor
        if debug: print(']')
    #endfor
    return pixels
#end

def make_trained_data(datadir=dirname() + '/data/trainning/', trained_filename=dirname() + '/data/trained.json', debug=False, jsonpindent=None):
    ''' Read all trainning images and make trained data! '''
    trained_data = {}
    lsdir = os.listdir(datadir)
    for childir in lsdir:
        if not childir.isdigit(): continue
        trained_data.setdefault(childir, {})
        cdatadir = datadir + childir + '/'
        # 
        clsdir = os.listdir(cdatadir)
        if debug: print(clsdir)
        for imgfile in clsdir:
            if not (imgfile.endswith('.png') or imgfile.endswith('.bmp')): continue
            filename = cdatadir + imgfile
            pixels = img_to_trained_json(filename, debug)
            md5.update(''.join(sorted(list(pixels))))
            key = md5.hexdigest()
            trained_data[childir][key] = pixels
        #endfor
        trained_data[childir] = trained_data[childir].values()
    #endfor
    # print(trained_data_json)
    # write result to file
    trained_data_json = json.dumps(trained_data, indent=jsonpindent)
    trained_file = open(trained_filename, "w")
    trained_file.write(trained_data_json)
    trained_file.close()
    # Return
    return trained_data
#endef

def get_trained_data(trained_filename=dirname() + '/data/trained.json', char=None):
    ''' Get trained data! '''
    # print('trained_filename: ', trained_filename)
    try:
        with open(trained_filename, 'r') as content_file:
            content = content_file.read()
            content = json.loads(content)
            content = content.get(char) if char else content
            return content
    except:
        return {}
#endef

def ocr_pixels_cmp(from_pixels, to_pixels):
    total = len(from_pixels)
    total2 = len(to_pixels)
    color_cnt = 0
    for key in from_pixels:
        color = to_pixels.get(key)
        if color is not None:
            color_cnt += 1
        #endif
    #endfor
    percent_1 = float(color_cnt) / float(max(total, total2))
    percent_2 = 0.1 * float(color_cnt) / float(min(total, total2))
    percent_3 = 0.025 * abs(total - total2)
    percent_1 -= percent_3
    rank = percent_1 + percent_2
    return (
        rank
        , '%s(%s)%s' % (total, color_cnt, total2)
        , '%f5' % (percent_1)
        , '%f5' % (percent_2)
        , '%f5' % (percent_3)
    )
#endef
        
def ocr(img, debug=False, show_img=False):
    ''' '''
    pixels = img_to_trained_json(img, debug=False)
    #
    trained_data = get_trained_data()
    # print('trained_data: ', trained_data)
    cnt_max_by_char = (0.0, 0, 0, 0.0, '')
    for char in trained_data:
        if debug: print('----- %s ----- ' % (char))
        cnt_max = (0, 0, 0.0)
        for data in trained_data[char]:
            pixcels_cmp = ocr_pixels_cmp(pixels, data)
            if debug == 0: # debug
                if pixcels_cmp[0] >= 0.5 and (char == 'O' or char == 'G'):
                   print(pixcels_cmp + (char,))
            #endif
            if debug: print(pixcels_cmp)
            if pixcels_cmp[0] > cnt_max[0]:
                cnt_max = pixcels_cmp
        #endfor
        if debug: print('----- end#%s ----- ' % (char))
        if cnt_max[0] > cnt_max_by_char[0]:
            cnt_max_by_char = cnt_max + (char,)
    #endfor
    if show_img: img.show()
    return cnt_max_by_char
#endif
