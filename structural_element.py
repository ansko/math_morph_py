#from PIL import Image

from utils import ll2Image_binary


def box(width, height, color=0):
    return ll2Image_binary([[
        color for _ in range(width)] for _ in range(height)])


def disk(diameter):
    d = diameter
    # Additions of 0.5 are made for the disk
    # to be symmetric around the picture center
    return ll2Image_binary([[{True: 0, False: 1}[
        (x_idx + 0.5 - d/2)**2 + (y_idx + 0.5 - d/2)**2 < d**2/4]
            for y_idx in range(diameter)] for x_idx in range(diameter)])


def ring(diameter):
    d = diameter
    # Additions of 0.5 are made for the ring
    # to be symmetric around the picture center
    d_in = d - 2 # inner emptiness diameter
    result = [[{True: 0, False: 1}[
        int((x_idx + 0.5 - d/2)**2 + (y_idx + 0.5 - d/2)**2) < int(d**2/4) and
        int((x_idx + 0.5 - d/2)**2 + (y_idx + 0.5 - d/2)**2) >= int((d_in)**2/4)]
            for y_idx in range(diameter)] for x_idx in range(diameter)]
    # To remove too dense filling like this:
    #   0010      0010
    #   0110  ->  0100
    #   0100      0100
    for x_idx in range(1, diameter-1):
        for y_idx in range(1, diameter-1):
            if any((not result[y_idx-1][x_idx] + result[y_idx][x_idx-1],
                    not result[y_idx-1][x_idx] + result[y_idx][x_idx+1],
                    not result[y_idx+1][x_idx] + result[y_idx][x_idx-1],
                    not result[y_idx+1][x_idx] + result[y_idx][x_idx+1])):
                result[y_idx][x_idx] = 1
    return ll2Image_binary(result)

def test_all():
    import os

    if 'tmp' not in os.listdir():
        os.mkdir('tmp')

    # boxes of different size and shape:
    height = 10
    width = 20
    box(width, height).save('tmp/structural_box_{0}_{1}.png'.format(width, height))
    box(width, width).save('tmp/structural_box_{0}_{0}.png'.format(width))
    box(height, height).save('tmp/structural_box_{0}_{0}.png'.format(height))

    # disks of different size
    for diameter in [6, 7, 100, 101]:
        disk(diameter).save('tmp/structural_disk_{0}.png'.format(diameter))

    # rings of different size
    for diameter in [6, 7, 100, 101]:
        ring(diameter).save('tmp/structural_ring_{0}.png'.format(diameter))


if __name__ == '__main__':
    test_all()
