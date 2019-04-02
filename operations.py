from put_on import put_on
from utils import write_svg


def erose(img, el, bg_color=1):
    return put_on(img, el, 'all', bg_color)


def dilate(img, el, bg_color=1):
    return put_on(img, el, 'any', bg_color)


def opening(img, el, bg_color=1, writeout=False):
    erosed = put_on(img, el, 'all', bg_color=bg_color)
    dilated = put_on(erosed, el, 'any', bg_color=bg_color)
    if writeout:
        write_svg(img, 'tmp/opening_0_initial.svg')
        write_svg(erosed, 'tmp/opening_1_erosed.svg')
        write_svg(dilated, 'tmp/opening_2_dilatated.svg')
    return dilated


def closing(img, el, bg_color=1, writeout=False):
    dilated = put_on(img, el, 'any', bg_color=bg_color)
    erosed = put_on(dilated, el, 'all', bg_color=bg_color)
    if writeout:
        write_svg(img, 'tmp/closening_0_initial.svg')
        write_svg(dilated, 'tmp/closeining_1_dilatated.svg')
        write_svg(erosed, 'tmp/closening_2_erosed.svg')
    return erosed


def test():
    from PIL import Image
    from structural_element import box

    size = 7
    img = Image.open('noisy_spoon_black.png').convert(mode='1')
    erose(img, box(size, size), bg_color=1)
    dilate(img, box(size, size), bg_color=1)
    opening(img, box(size, size), bg_color=1, writeout=True)
    closing(img, box(size, size), bg_color=1, writeout=True)


if __name__ == '__main__':
    test()
