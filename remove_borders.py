from PIL import Image
from operations import opening, closing, erose, dilate
from structural_element import disk


if __name__ == '__main__':
    img = Image.open('reverse.png').convert(mode='1')
    img_er = erose(img, disk(25), bg_color=1)
    img_er.save('contacting_reverse_erosed.png')
    img_op = dilate(img_er, disk(25), bg_color=1)
    img_op.save('contacting_reverse_opened.png')
    img_di = dilate(img_op, disk(10), bg_color=1)
    img_di.save('contacting_reverse_di.png')
    img_or = erose(img_di, disk(10), bg_color=1)
    img_or.save('contacting_reverse_cycled.png')
