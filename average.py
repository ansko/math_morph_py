from PIL import Image
from structural_element import disk
from operations import opening, closing


if __name__ == '__main__':
    dr = 2
    img = Image.open('some.jpg').convert(mode='1')
    img.save('tmp/1_bw.png')
    w, h = img.size
    img_new = Image.new(size=(w,h), mode='1', color=1)
    pixels = img.load()
    new_pixels = img_new.load()
    for idx_x in range(w):
        for idx_y in range(h):
            s = 0
            for dx in range(-dr, dr):
                x = idx_x + dx
                if x < 0:
                    x += w
                elif x >= w:
                    x -= w
                for dy in range(-dr, dr):
                    y = idx_y + dy
                    if y < 0:
                        y += h
                    elif y >= h:
                        y -= h
                    #print(w, h, x, y)
                    s += pixels[x, y]
            if s > 0.5 * 3 * dr**2:
                new_pixels[x, y] = 0
    img_new.save('tmp/new_{0}.png'.format(dr))
