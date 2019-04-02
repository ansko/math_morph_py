import sys
from PIL import Image

from generate_image import spots_binary
from operations import dilate, erose, opening, closing
from utils import ll2Image_binary, write_svg
from structural_element import box


def difference(img1, img2, diff_color=0):
    assert(img1.size == img2.size)
    img = Image.new(size=img1.size, mode='1', color=1-diff_color)
    pixels = img.load()
    pixels1 = img1.load()
    pixels2 = img2.load()
    for idx_x in range(img.size[0]):
        for idx_y in range(img.size[1]):
            if pixels1[idx_x,idx_y] != pixels2[idx_x, idx_y]:
                pixels[idx_x, idx_y] = diff_color
    return img


def find_borders(img, el_radius=1, bg_color=1):
    el = ll2Image_binary([[1 if idx_y != el_radius and idx_x != el_radius else 0
        for idx_y in range(1 + 2*el_radius)]
            for idx_x in range(1 + 2*el_radius)])
    write_svg(el, 'tmp/el.svg')
    bg_color = 1
    erosed = erose(img, el, bg_color)
    d_img = difference(img, erosed)
    d_img.save('tmp/borders_found.png')


def test():
    if len(sys.argv) > 2:
        img = Image.open(sys.argv[1]).convert(mode='1')
        img.save('tmp/borders_init.png')
        bg_color = 1 if sys.argv[2] in ['w', 'white', 1] else 0
        #img_no_white_noise = closing(img, box(3, 3))
        #img_no_white_noise.save('tmp/borders_init_nown.png')
        img = opening(img, box(3, 3))
        img.save('tmp/borders_init_nobn.png')
        find_borders(img, 15, 1)
    else:
        img = spots_binary(square_side=500)
        bg_color = 1
        img.save('tmp/borders_init.png')
        find_borders(img, 15, 1)


if __name__ == '__main__':
    test()
