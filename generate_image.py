#!/usr/bin/env python3


import os
from PIL import Image
import math
import random
import time

from utils import ll2Image_binary


def random_binary(square_side, **kwargs):
    out_fname = 'tmp/random_bw.png'
    save = False
    if 'out_fname' in kwargs.keys():
        out_fname = kwargs['out_fname']
    if 'save' in kwargs.keys():
        save = kwargs['save']
    random.seed(int(time.time()))
    img = ll2Image_binary(
        [[random.choice((0, 1)) for idx_y in range(square_side)]
            for idx_x in range(square_side)])
    if save:
        if 'tmp' not in os.listdir() and 'tmp/' in out_fname:
            os.mkdir('tmp')
        img.save(out_fname)
    return img


def spots_binary(square_side, **kwargs):
    out_fname = 'tmp/spots_bw.png'
    save = False
    if 'out_fname' in kwargs.keys():
        out_fname = kwargs['out_fname']
    if 'save' in kwargs.keys():
        save = kwargs['save']
    random.seed(int(time.time()))
    #img = Image.new(mode=color_mode, size=(square_side, square_side), color=1)
    #pixels = img.load()
    # Find spots' coordintates
    spots_count = 20
    spots = []
    fails_done = 0
    fails_allowed = spots_count * 10
    while len(spots) < spots_count and fails_done < fails_allowed:
        r = random.randint(1, square_side//10)
        x = random.randint(r, square_side - r)  # do not cross borders
        y = random.randint(r, square_side - r)
        is_close = False
        for spot in spots:
            dx = spot['x'] - x
            dy = spot['y'] - y
            if dx**2 + dy**2 < (r + spot['r'])**2:
                is_close = True
                break
        if is_close:
            fails_done += 1
        else:
            spots.append({'x': x, 'y': y, 'r': r})
    ll = [[1 for idx_y in range(square_side)] for idx_x in range(square_side)]
    # Draw spots
    for spot in spots:
        for dx in range(-spot['r'], spot['r'] + 1):
            for dy in range(-spot['r'], spot['r'] + 1):
                if dx**2 + dy**2 < spot['r']**2:
                    ll[spot['x'] + dx][spot['y'] + dy] = 0
    img = ll2Image_binary(ll)
    if save:
        if 'tmp' not in os.listdir() and 'tmp/' in out_fname:
            os.mkdir('tmp')
        img.save(out_fname)
        with open(out_fname + '_info', 'w') as f:
            for spot in spots:
                print(spot['x'], spot['y'], spot['r'], file=f)
    return img


def segments(square_side):
    length = square_side // 10
    out_fname = 'tmp/spots_bw.png'
    random.seed(int(time.time()))

    segments_count = 20
    segments = []
    fails_done = 0
    fails_allowed = segments_count * 10
    while len(segments) < segments_count and fails_done < fails_allowed:
        x = random.randint(length // 2, square_side - length // 2)  # do not cross
        y = random.randint(length // 2, square_side - length // 2)  # borders
        alpha = random.random() * 2 * math.pi
        segments.append({'x': x, 'y': y, 'alpha': alpha})
    ll = [[1 for idx_y in range(square_side)] for idx_x in range(square_side)]
    for segment in segments:
        x = int(segment['x'])
        y = segment['y']
        alpha = segment['alpha']
        x1 = int(segment['x'] + length * math.cos(alpha))
        for coord in range(x, x1):
            y1 = int(y + (coord - x) / math.cos(alpha) * math.sin(alpha))
            ll[coord][y1] = 0
    return ll2Image_binary(ll)


if __name__ == '__main__':
    square_side = 1000
    '''
    out_fname_random_bw = 'random_bw.png'
    out_fname_spots_bw = 'spots_bw.png'

    print('random_binary() from {0}: square {1}x{1} in file {2}'.format(
        __file__, square_side, out_fname_random_bw))
    random_binary(square_side, save=True)

    print('spots_binary() from {0}: square {1}x{1} in file {2}'.format(
        __file__, square_side, out_fname_spots_bw))
    spots_binary(square_side, save=True)
    '''
    img = segments(1000)
    img.save('segments.png')
