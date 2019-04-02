from PIL import Image


def ll2Image_binary(ll):
    '''list of lists to binary PIL.Image
    '''
    width = len(ll)
    height = len(ll[0])
    img = Image.new(mode='1', size=(width, height))
    pixels = img.load()
    for idx_x in range(width):
        for idx_y in range(height):
            pixels[idx_x, idx_y] = ll[idx_x][idx_y]
    return img


def Image2ll_binary(img):
    '''binary PIL.Image to list of lists
    '''
    width = img.size[0]
    height = img.size[1]
    ll = [[0 for idx_y in range(height)] for idx_x in range(width)]
    pixels = img.load()
    for idx_x in range(width):
        for idx_y in range(height):
            ll[idx_x][idx_y] = pixels[idx_x, idx_y]
    return ll


def expand(obj, dx_min, dx_max, dy_min, dy_max, bg_color):
    '''Add empty borders to the image
    '''
    if type(obj) == list:
        x_size = len(obj)
        y_size = len(obj[0])
        new_x_size = len(obj) + dx_min + dx_max
        new_y_size = len(obj[0]) + dy_min + dy_max
        pixels = obj
    elif type(obj) == Image.Image:
        x_size = obj.size[0]
        y_size = obj.size[1]
        new_x_size = obj.size[0] + dx_min + dx_max
        new_y_size = obj.size[1] + dy_min + dy_max
        pixels = Image2ll_binary(obj)
    else:
        raise ValueError('arg 1 should be list or PIL.Image.Image')
    new_pixels = [[bg_color for idx_y in range(new_y_size)]
        for idx_x in range(new_x_size)]
    for idx_x in range(x_size):
        for idx_y in range(y_size):
            new_pixels[dx_min + idx_x][dy_min + idx_y] = pixels[idx_x][idx_y]
    if type(obj) == list:
        return new_pixels
    return ll2Image_binary(new_pixels)


def cut(obj, dx_min, dx_max, dy_min, dy_max):
    '''Remove borders from the image
    '''
    if type(obj) == list:
        if dx_max != 0 and dy_max != 0:
            return [line[dy_min:-dy_max] for line in obj[dx_min:-dx_max]]
        elif dx_max == 0 and dy_max != 0:
            return [line[dy_min:-dy_max] for line in obj[dx_min:]]
        elif dx_max !=0 and dy_max == 0:
            return [line[dy_min:] for line in obj[dx_min:-dx_max]]
        elif dx_max == 0 and dy_max == 0:
            return [line[dy_min:] for line in obj[dx_min:]]
    elif type(obj) == Image.Image:
        new_x_size = obj.size[0] + dx_min + dx_max
        new_y_size = obj.size[1] + dy_min + dy_max
        return ll2Image_binary([line[dy_min:-dy_max]
            for line in Image2ll_binary(obj)[dx_min:-dx_max]])
    else:
        raise ValueError('arg 1 should be list or PIL.Image.Image')


def write_svg(obj, out_fname='out.svg'):
    rect_str = ('<rect x="{0}" y="{1}" width="50" height="50" '
                'style="fill:rgb({2},{2},{2});stroke-width:3;'
                'stroke:rgb({3},{3},{3})" />')
    if type(obj) == list:
        x_size = len(obj)
        y_size = len(obj[0])
        pixels = obj
    elif type(obj) == Image.Image:
        x_size = obj.size[0]
        y_size = obj.size[1]
        pixels = Image2ll_binary(obj)
    with open(out_fname, 'w') as f:
        print('<svg>', file=f)
        for idx_x in range(x_size):
            for idx_y in range(y_size):
                color = 0 if not pixels[idx_x][idx_y] else 255
                print(rect_str.format(idx_x*50, idx_y*50, color, 255-color), file=f)
        print('</svg>', file=f)

def test():
    import os

    img_1 = ll2Image_binary([[0]])
    img_3 = ll2Image_binary([[0, 1, 1],
                           [1, 0, 1],
                           [1, 1, 0]])
    img_exp = expand(img_3, 2, 2, 2, 2)
    img_cut = cut(img_exp, 2, 2, 2, 2)
    ll = Image2ll_binary(img_3)
    print(ll)

    if 'tmp' not in os.listdir():
        os.mkdir('tmp')
    img_1.save('tmp/test_1.png')
    img_3.save('tmp/test_3.png')
    img_exp.save('tmp/test_3_expanded.png')
    img_cut.save('tmp/test_3_cut.png')


if __name__ == '__main__':
    test()
