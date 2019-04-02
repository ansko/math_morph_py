#!/usr/bin/env python3


import sys
from PIL import Image


old_img = Image.open(sys.argv[1])
new_img = old_img.convert(mode='1')
new_img.save('new.png')
