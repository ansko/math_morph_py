from PIL import Image
from structural_element import disk
from operations import opening, closing


if __name__ == '__main__':
    img = Image.open('tmp/new_1.png').convert(mode='1')
    img = closing(img, disk(3))
    img.save('tmp/close.png')
    img = opening(img, disk(150))
    img.save('tmp/result.png')
