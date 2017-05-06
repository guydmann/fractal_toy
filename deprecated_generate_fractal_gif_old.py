from __future__ import division
import multiprocessing
import argparse
from progressbar import ProgressBar
from images2gif import writeGif
from PIL import Image
import os

from fractal_dwell import FractalDwell
from color_lib import ColorLib
from fractal_lib import FractalLib

"""
def create_test_mandelbrot(width, height, left_x, right_x, top_y, bottom_y, filename):
    img = Image.new('RGBA', (width, height))
    precision = 300

    x_inc = (right_x - left_x) / width
    y_inc = (top_y - bottom_y) / height
    for cx in range(width):
        for cy in range(height):
            img.putpixel((cx, cy), ColorLib.simple(FractalDwell.dwell_mandel((cx*x_inc)+left_x, top_y-(cy*y_inc), precision), precision))
    img.save('{}.bmp'.format(filename), 'BMP')


def create_test_julia(width, height, left_x, right_x, top_y, bottom_y, cr, ci, filename=None):
    img = Image.new('RGBA', (width, height))
    precision = 300

    x_inc = (right_x - left_x) / width
    y_inc = (top_y - bottom_y) / height
    for cx in range(width):
        for cy in range(height):
            img.putpixel((cx, cy), ColorLib.simple(FractalDwell.dwell_julia((cx*x_inc)+left_x, top_y-(cy*y_inc), precision, cr, ci), precision))

    if filename:
        img.save('{}.bmp'.format(filename), 'BMP')
        return '{}.bmp'.format(filename)
    else:
        return img

def create_test_buddha_fractal(width, height, left_x, right_x, top_y, bottom_y, filename):
    img = Image.new('RGBA', (width, height))
    precision = 300

    x_inc = (right_x - left_x) / width
    y_inc = (top_y - bottom_y) / height
    fractal_array = FractalLib.create_empty_fractal_array(width, height)
    calc_pbar = ProgressBar(maxval=width)
    color_pbar = ProgressBar(maxval=width)

    calc_pbar.start()
    print "Calculating Fractal"
    for cx in range(width):
        for cy in range(height):
            fractal_array = FractalDwell.dwell_buddha(
                (cx*x_inc)+left_x, top_y-(cy*y_inc),
                precision, width, height, x_inc, y_inc,
                fractal_array, left_x, top_y
            )
        calc_pbar.update(cx+1)
    calc_pbar.finish()

    color_pbar.start()
    print "Coloring Fractal"
    for cx in range(width):
        for cy in range(height):
            img.putpixel((cx, cy), ColorLib.simple(fractal_array[cx][cy], precision))
        color_pbar.update(cx+1)
    color_pbar.finish()

    img.save('{}.bmp'.format(filename), 'BMP')

def create_test_julia_buddha_fractal(width, height, left_x, right_x, top_y, bottom_y, cr, ci, filename):
    img = Image.new('RGBA', (width, height))
    precision = 300

    x_inc = (right_x - left_x) / width
    y_inc = (top_y - bottom_y) / height
    fractal_array = FractalLib.create_empty_fractal_array(width, height)
    calc_cols_pbar = ProgressBar(maxval=width)
    color_pbar = ProgressBar(maxval=width)

    calc_cols_pbar.start()
    print "Calculating Fractal"
    for cx in range(width):
        for cy in range(height):
            fractal_array = FractalDwell.dwell_buddha_julia(
                (cx*x_inc)+left_x, top_y-(cy*y_inc),
                precision, width, height, x_inc, y_inc,
                fractal_array, left_x, top_y,
                cr, ci
            )
        calc_cols_pbar.update(cx+1)
    calc_cols_pbar.finish()

    color_pbar.start()
    print "Coloring Fractal"
    for cx in range(width):
        for cy in range(height):
            img.putpixel((cx, cy), ColorLib.simple(fractal_array[cx][cy], precision))
        color_pbar.update(cx+1)
    color_pbar.finish()

    img.save('{}.bmp'.format(filename), 'BMP')

def generate_lots_of_julia_buddhas():
    inc = 100
    for r in range(inc):
        for i in range(inc):
            left_x = -1
            right_x = 1
            top_y = 1
            bottom_y = -1
            cr = left_x+(r*((right_x-left_x)/inc))
            ci = top_y-(i*((top_y-bottom_y)/inc))
            create_test_julia_buddha_fractal(100, 100, left_x, right_x, top_y, bottom_y, cr, ci, "test_julia_buddha_{}_{}".format(cr, ci))


def generate_lots_of_julias():
    inc = 20
    calc_pbar = ProgressBar(maxval=inc)
    calc_pbar.start()
    for r in range(inc):
        for i in range(inc):
            left_x = -1
            right_x = 1
            top_y = 1
            bottom_y = -1
            cr = left_x+(r*((right_x-left_x)/inc))
            ci = top_y-(i*((top_y-bottom_y)/inc))
            create_test_julia(100, 100, left_x, right_x, top_y, bottom_y, cr, ci, "test_julia_{}_{}".format(cr, ci))
        calc_pbar.update(r+1)
    calc_pbar.finish()

def generate_julia_gif1():
    inc = 200
    calc_pbar = ProgressBar(maxval=inc)
    calc_pbar.start()
    images = [None for inc_value in range(inc)]
    for r in range(inc):
        i = r
        left_x = -1
        right_x = 1
        top_y = 1
        bottom_y = -1
        cr = left_x+(r*((right_x-left_x)/inc))
        ci = top_y-(i*((top_y-bottom_y)/inc))
        images[r] = create_test_julia(400, 400, left_x, right_x, top_y, bottom_y, cr, ci)
        calc_pbar.update(r+1)
    calc_pbar.finish()

    writeGif("test_julia.gif", images)
"""

def create_test_julia_helper(args):
    width, height, left_x, right_x, top_y, bottom_y, cr, ci, directory = args
    return create_test_julia(width, height, left_x, right_x, top_y, bottom_y, cr, ci, "{}/test_julia_{}_{}".format(directory, cr, ci))



def generate_julia_spiral_gif(width, height, increments, view_port_range, constant_range):
    THREAD_POOL_SIZE = 6

    p = multiprocessing.Pool(THREAD_POOL_SIZE)
    directory = "spiral_julia"
    X = Y = increments
    data_mappings = []
    images = []

    FractalLib.empty_dir_and_remove(directory)
    os.mkdir(directory)

    r = i = 0
    dr = 0
    di = -1
    for k in range(max(X, Y)**2):
        if (-X/2 < r <= X/2) and (-Y/2 < i <= Y/2):
            cr = constant_range['left_x']+(r*((constant_range['right_x']-constant_range['left_x'])/X))
            ci = constant_range['top_y']-(i*((constant_range['top_y']-constant_range['bottom_y'])/Y))
            data_mappings.append([width, height, view_port_range['left_x'], view_port_range['right_x'], view_port_range['top_y'], view_port_range['bottom_y'], cr, ci, directory])
        if r == i or (r < 0 and r == -i) or (r > 0 and r == 1-i):
            dr, di = -di, dr
        r, i = r+dr, i+di

    calc_pbar = ProgressBar(maxval=len(data_mappings))
    calc_pbar.start()
    results = []
    for i, _ in enumerate(p.imap(create_test_julia_helper, data_mappings), 1):
        calc_pbar.update(i)
        results.append(_)
    calc_pbar.finish()

    for filename in results:
        images.append(Image.open(filename).convert('RGBA'))

    writeGif("test_julia_spiral.gif", images)



"""
generate_lots_of_julia_buddhas()
generate_lots_of_julias()
generate_julia_spiral_gif(100, 100, 50, -1, 1, 1, -1)left_x, right_x, top_y, bottom_y
view_port_range = {'left_x': -1, 'right_x': 1, 'top_y': 1, 'bottom_y': -1}
constant_range = {'left_x': -1.35, 'right_x': -1.2, 'top_y': 0.1, 'bottom_y': -0.1}
generate_julia_spiral_gif(200, 200, 10, view_port_range, constant_range)

view_port_range = {'left_x': -1, 'right_x': 1, 'top_y': 1, 'bottom_y': -1}
constant_range = {'left_x': -1.35, 'right_x': -1.2, 'top_y': 0.1, 'bottom_y': -0.1}
generate_julia_spiral_gif(200, 200, 10, view_port_range, constant_range)
"""

def main(args):
    view_port_range = {'left_x': args.viewport_left, 'right_x': args.viewport_right,
                       'top_y': args.viewport_top, 'bottom_y': args.viewport_bottom}
    constant_range = {'left_x': args.constant_left, 'right_x': args.constant_right,
                      'top_y': args.constant_top, 'bottom_y': args.constant_bottom}
    generate_julia_spiral_gif(args.width, args.height, args.increments, view_port_range, constant_range)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=True)
    process = parser.add_mutually_exclusive_group(required=True)

    parser.add_argument('-f', '--fractal', default="mandelbrot", type=str,
                        choices=['mandelbrot', 'julia','burningship', 'star', 'newton', 'phoenix_mandelbrot',
                                 'phoenix_julia', 'cubic_mandelbrot', 'quartic_mandelbrot', 'cubic_julia',
                                 'experimental_cubic_julia', 'quartic_julia', 'buddhabrot', 'buddhabrot_julia'])
    parser.add_argument('-w', '--width', default=200, type=int)
    parser.add_argument('-h', '--height', default=200, type=int)
    parser.add_argument('-i', '--increments', default=10, type=int)
    parser.add_argument('-vl', '--viewport_left', default=-1.0, type=float)
    parser.add_argument('-vr', '--viewport_right', default=1.0, type=float)
    parser.add_argument('-vt', '--viewport_top', default=1.0, type=float)
    parser.add_argument('-vb', '--viewport_bottom', default=-1.0, type=float)
    parser.add_argument('-cl', '--constant_left', default=-1.0, type=float)
    parser.add_argument('-cr', '--constant_right', default=1.0, type=float)
    parser.add_argument('-ct', '--constant_top', default=1.0, type=float)
    parser.add_argument('-cb', '--constant_bottom', default=-1.0, type=float)
    parser.add_argument('-t', '--traversal', default=None, type=str,
                        choices=['diagonal', 'spiral'])
    args = parser.parse_args()
    main(args)