from __future__ import print_function
from PIL import Image, ImageFilter
from helpers import *

# print(rand_digit_str())
#
fn = '1522740391119_77'
fn = '1522740066804_355'
fn = '1522740067213_512'
fn = '1522740068132_386'
fn = '1522740401376_416' # failed
fn = '1522740402776_43'
fn = '1522740408419_494'
fn = '1522740422893_909'
fn = '1522740065649_819'
fn = '1522740065649_819'
fn = '1522916465555_371'
img = Image.open('./data/captcha/0002/' + fn + '.jpg')
img.show()
chars = img_split_chars(img, debug=True)
# ----- . ----- ----- . ----- ----- . ----- ----- . ----- ----- . ----- ----- . -----

''' # 
fn = '1522740518131_196'
fn = '1522740522445_99'
fn = '1522740525446_521'
fn = '1522740527201_793'
fn = '1522740528651_842'
fn = '1522740530036_322'
fn = '1522740531426_664'
fn = '1522740523956_59'
fn = '1522740521048_126'
fn = '1522740519621_353'
img = Image.open('./data/captcha/test/' + fn + '')
chars = img_split_chars(img)
#
charcnt = 0
for char in chars:
    charcnt += 1
    char.show()
    cnt_max_by_char = ocr(char, debug=False)
    print(str(charcnt) +  '#cnt_max_by_char: ', cnt_max_by_char)
#endfor
# ----- . ----- ----- . ----- ----- . ----- ----- . ----- ----- . ----- ----- . -----
'''
