#!/usr/bin/env python3


import sys
from PIL import Image


old_img = Image.open(sys.argv[1])
new_img = old_img.convert(mode='1')
pixels = new_img.load()
for idx_x in range(new_img.size[0]):
    for idx_y in range(new_img.size[1]):
        pixels[idx_x, idx_y] = 0 if pixels[idx_x, idx_y] != 0 else 1
new_img.save('reverse.png')
