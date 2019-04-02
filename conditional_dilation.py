from PIL import Image
from utils import ll2Image_binary
from structural_element import box
from operations import erose, dilate


if __name__ == '__main__':
    ll = [
        [1,1,1,1,1,1,1,1,1,1],
        [1,0,1,1,1,1,1,0,1,1],
        [1,0,1,1,1,1,1,1,1,1],
        [1,0,1,1,0,0,0,1,1,1],
        [1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,0,0,0,1,1],
        [1,1,1,1,1,0,0,0,1,1],
        [1,1,0,1,1,0,0,0,1,1],
        [1,0,0,0,1,1,1,1,1,1],
        [1,1,0,1,1,1,1,1,1,1],
    ]
    s_erose = box(3, 1)
    s_dilate = box(3, 3)
    img_init = ll2Image_binary(ll)
    img_init.save('cond_init.png')
    img_er = erose(img_init, s_erose)
    img_er.save('cond_erosed.png')
    img_result = dilate(img_er, s_dilate)
    img_result.save('cond_temp.png')
    img = Image.new(size=img_result.size, mode='1', color=1)
    pixels = img.load()
    pixels1 = img_init.load()
    pixels2 = img_result.load()
    for idx_x in range(img.size[0]):
        for idx_y in range(img.size[1]):
            if pixels1[idx_x,idx_y] == pixels2[idx_x, idx_y] == 0:
                pixels[idx_x, idx_y] = 0
    img.save('cond_result.png')
