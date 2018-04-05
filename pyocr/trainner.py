'''
o Get and store ANA captcha images..!
o Make tranning data from captcha images!
'''
import os
import time
from helpers import *

def go_download_captcha(folder, img_cnt):
    ''' ''' 
    # try to make dir
    if not os.path.exists(folder):
        os.makedirs(folder)
    # download captcha
    for i in range(img_cnt):
        captcha_download(folder)
        time.sleep(1) # 1 second
    #endfor
#endef
# download ANA captcha images
folder = './data/captcha/0004'
# go_download_captcha(folder, 100)
# ----- . ----- ----- . ----- ----- . ----- ----- . ----- ----- . ----- ----- . -----

def make_char_imgs(scan_folder, ouput_folder):
    ''' Scan all captchas and make char images!
    '''
    cnt = 0
    listdir = os.listdir(scan_folder)
    for filename in listdir:
        scan_filename = scan_folder + '/' + filename
        if filename.lower().endswith('.jpg') and os.path.exists(scan_filename):
            cnt += 1
            print(str(cnt) + ': ' + scan_filename)
            #
            chars = img_split_chars(scan_filename)
            if not chars: continue
            for char in chars:
                ouput_filename = rand_digit_str()
                cnt_max_by_char = ocr(char, debug=False)
                if cnt_max_by_char:
                    ouput_filename = str(cnt_max_by_char[-1]) + '_' + ouput_filename
                ouput_filename = img_save(char, str(ouput_folder) + '/' + ouput_filename)
                print(ouput_filename)
            #endfor
            print('#end')
    #endfor
#endef
scan_folder = './data/captcha/0004'
ouput_folder = './data/trainning'
# make_char_imgs(scan_folder, ouput_folder)
# ----- . ----- ----- . ----- ----- . ----- ----- . ----- ----- . ----- ----- . -----

#
make_trained_data(debug=False, jsonpindent=None)
# ----- . ----- ----- . ----- ----- . ----- ----- . ----- ----- . ----- ----- . -----
