from PIL import Image

from utils import ll2Image_binary, Image2ll_binary, expand, cut, write_svg


def put_on(img, el, condition, bg_color=1):
    # Center of the structural element
    x_c = el.size[0] // 2
    y_c = el.size[1] // 2

    # Additional emptiness to add to img along x and y
    dx_min = x_c
    dx_max = el.size[0] - x_c - 1
    dy_min = y_c
    dy_max = el.size[1] - y_c - 1


    element_pixels = Image2ll_binary(el)
    image_pixels = expand(Image2ll_binary(img),
        dx_min, dx_max, dy_min, dy_max, bg_color)
    new_image_pixels = [[
        1 for idx_y in range(img.size[1] + dy_min + dy_max)]
            for idx_x in range(img.size[0] + dx_min + dx_max)]

    black_count = 0
    for idx_x in range(dx_min, dx_min + img.size[0]):
        for idx_y in range(dy_min, dy_min + img.size[1]):
            if condition == 'any' and image_pixels[idx_x][idx_y] == 0:
                for dx in range(-dx_min, dx_max + 1):
                    for dy in range(-dy_min, dy_max + 1):
                        if element_pixels[x_c + dx][y_c + dy] == 0:
                            if new_image_pixels[idx_x + dx][idx_y + dy] != 0:
                                black_count += 1
                            new_image_pixels[idx_x + dx][idx_y + dy] = 0
            elif condition == 'all':
                if image_pixels[idx_x][idx_y] == 0:
                    all_match = True
                    for dx in range(-dx_min, dx_max + 1):
                        for dy in range(-dy_min, dy_max + 1):
                            if (image_pixels[idx_x + dx][idx_y + dy] != 0
                                and element_pixels[x_c + dx][y_c + dy] == 0):
                                    all_match = False
                                    break
                        if not all_match:
                            break
                    if all_match:
                        new_image_pixels[idx_x][idx_y] = 0
                        black_count += 1
    print('black:', black_count,
          'white:', img.size[0] * img.size[1] - black_count)
    return ll2Image_binary(cut(new_image_pixels, dx_min, dx_max, dy_min, dy_max))


def test():
    from structural_element import box, disk, ring
    from operations import opening, closing

    img = Image.open('noisy_spoon_black.png').convert(mode='1')
    size = 7
    bg_color = 0
    opened = opening(img, disk(size), bg_color, writeout=False)
    opened.save('tmp/opened.png')
    closed = closing(img, disk(size), bg_color, writeout=False)
    closed.save('tmp/closed.png')


if __name__ == '__main__':
    test()
