from __future__ import division
import multiprocessing
import argparse
from progressbar import ProgressBar
from images2gif import writeGif
from PIL import Image
import os

from fractals.mandelbrot import Mandelbrot
from fractals.julia import Julia
from fractals.burning_ship import BurningShip
from fractals.star import Star
from fractals.newton import Newton
from fractals.phoenix_mandelbrot import PhoenixMandelbrot
from fractals.phoenix_julia import PhoenixJulia
from fractals.cubic_mandelbrot import CubicMandelbrot
from fractals.cubic_julia import CubicJulia
from fractals.experimental_cubic_julia import ExperimentalCubicJulia
from fractals.quartic_mandelbrot import QuarticMandelbrot
from fractals.quartic_julia import QuarticJulia
from fractals.buddhabrot import Buddhabrot
from fractals.buddhabrot_julia import BuddhabrotJulia

from colors.simple import Simple
from colors.black_and_white import BlackAndWhite
from colors.hue_range import HueRange

from fractal_lib import FractalLib

def setup_fractal(fractal_algorithm):
    """
        fractal_algorithm: 'mandelbrot', 'julia','burningship', 'star', 'newton', 'phoenix_mandelbrot',
                           'phoenix_julia', 'cubic_mandelbrot', 'quartic_mandelbrot', 'cubic_julia',
                           'experimental_cubic_julia', 'quartic_julia', 'buddhabrot', 'buddhabrot_julia'
    """
    fractal = None
    if fractal_algorithm == "mandelbrot":
        fractal = Mandelbrot()
    elif fractal_algorithm == "julia":
        fractal = Julia()
    elif fractal_algorithm == "burning_ship":
        fractal = BurningShip()
    elif fractal_algorithm == "star":
        fractal = Star()
    elif fractal_algorithm == "newton":
        fractal = Newton()
    elif fractal_algorithm == "phoenix_mandelbrot":
        fractal = PhoenixMandelbrot()
    elif fractal_algorithm == "phoenix_julia":
        fractal = PhoenixJulia()
    elif fractal_algorithm == "cubic_mandelbrot":
        fractal = CubicMandelbrot()
    elif fractal_algorithm == "cubic_julia":
        fractal = CubicJulia()
    elif fractal_algorithm == "quartic_mandelbrot":
        fractal = QuarticMandelbrot()
    elif fractal_algorithm == "quartic_julia":
        fractal = QuarticJulia()
    elif fractal_algorithm == "experimental_cubic_julia":
        fractal = ExperimentalCubicJulia()
    elif fractal_algorithm == "buddhabrot":
        fractal = Buddhabrot()
    elif fractal_algorithm == "buddhabrot_julia":
        fractal = BuddhabrotJulia()
    return fractal


def setup_fractal_color_scheme(fractal, color_algorithm=None, hue_start_degree=None, hue_end_degree=None):
    """
        must pass:
            color_algorithm: simple, black_and_white, hue_range
        can pass:
            hue_start_degree:   0-360
            hue_end_degree:     0-360
    """
    color = None
    if color_algorithm == "simple":
        color = Simple()
        fractal.set_color_algorithm_name(color_algorithm)
    elif color_algorithm == "black_and_white":
        color = BlackAndWhite()
        fractal.set_color_algorithm_name(color_algorithm)
    elif color_algorithm == "hue_range":
        color = HueRange()
        if hue_start_degree is not None:
            color.set_start_degree(hue_start_degree)
        if hue_end_degree is not None:
            color.set_end_degree(hue_end_degree)
        fractal.set_color_algorithm_name("{}-{}-{}".format(color_algorithm, color.start_degree, color.end_degree))
    fractal.set_color_algorithm(color)
    return fractal


def setup_fractal_viewport(fractal, viewport_left=None, viewport_right=None, viewport_top=None, viewport_bottom=None):
    """
        args can contain:
            viewport_left, viewport_right, viewport_top, viewport_bottom
    """
    if viewport_left is not None and viewport_right is not None \
            and viewport_bottom is not None and viewport_top is not None:
        viewport = {'left_x': viewport_left,
                    'right_x': viewport_right,
                    'top_y': viewport_top,
                    'bottom_y': viewport_bottom}
        fractal.set_viewport(viewport)
    else:
        if viewport_left is not None:
            fractal.set_viewport_left(viewport_left)
        if viewport_right is not None:
            fractal.set_viewport_right(viewport_right)
        if viewport_top is not None:
            fractal.set_viewport_top(viewport_top)
        if viewport_bottom is not None:
            fractal.set_viewport_bottom(viewport_bottom)
    return fractal

def animate_fractal(fractal, animation_algorithm):
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
    if animation_algorithm==0:
        run_animation_first(fractal)

def run_animation_first(fractal):

    fractal.set_filename()
    fractal.render()

















"""

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

    fractal = setup_fractal(args.fractal_algorithm)
    fractal = setup_fractal_color_scheme(fractal, args)
    fractal = setup_fractal_viewport(fractal, args)

    fractal.set_show_progress_bar(False)
    if args.width is not None:
        fractal.set_width(args.width)
    if args.height is not None:
        fractal.set_height(args.height)
    if args.real_constant is not None:
        fractal.set_real_constant(args.real_constant)
    if args.imaginary_constant is not None:
        fractal.set_imaginary_constant(args.imaginary_constant)
    if args.filename is not None:
        fractal.set_filename(args.filename)
    if args.precision is not None:
        fractal.set_precision(args.precision)

    if args.fractal_animation is not None:
        animate_fractal(fractal, args.fractal_animation)

"""
    view_port_range = {'left_x': args.viewport_left, 'right_x': args.viewport_right,
                       'top_y': args.viewport_top, 'bottom_y': args.viewport_bottom}
    constant_range = {'left_x': args.constant_left, 'right_x': args.constant_right,
                      'top_y': args.constant_top, 'bottom_y': args.constant_bottom}
    generate_julia_spiral_gif(args.width, args.height, args.increments, view_port_range, constant_range)
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=True)

    parser.add_argument('-f', '--filename', type=str, help='do not include file extension')
    parser.add_argument('-a', '--fractal_algorithm', default="mandelbrot", type=str,
                        choices=['mandelbrot', 'julia','burning_ship', 'star', 'newton', 'phoenix_mandelbrot',
                                 'phoenix_julia', 'cubic_mandelbrot', 'quartic_mandelbrot', 'cubic_julia',
                                 'experimental_cubic_julia', 'quartic_julia', 'buddhabrot', 'buddhabrot_julia'])
    parser.add_argument('-c', '--color_algorithm', default="simple", type=str,
                        choices=['simple', 'black_and_white','hue_range'])
    parser.add_argument('-W', '--width', type=int)
    parser.add_argument('-H', '--height', type=int)
    parser.add_argument('-vl', '--viewport_left', type=float,
                        help='coordinate of left edge of view port')
    parser.add_argument('-vr', '--viewport_right', type=float,
                        help='coordinate of right edge of view port')
    parser.add_argument('-vt', '--viewport_top', type=float,
                        help='coordinate of top edge of view port')
    parser.add_argument('-vb', '--viewport_bottom', type=float,
                        help='coordinate of bottom edge of view port')
    parser.add_argument('-cr', '--real_constant', type=float,
                        help='only useful for julia set based fractals')
    parser.add_argument('-ci', '--imaginary_constant', type=float,
                        help='only useful for julia set based fractals')
    parser.add_argument('-p', '--precision', type=int)
    parser.add_argument('-hs', '--hue_start_degree', type=int,
                        help='use to define hue range for hue_range color algorithm')
    parser.add_argument('-he', '--hue_end_degree', type=int,
                        help='use to define hue range for hue_range color algorithm')

    parser.add_argument('-A', '--fractal_animation', type=str, help='int to select animation')
    parser.add_argument('-i', '--increments', default=80, type=int)\

    parser.add_argument('-cl', '--constant_left', default=-1.0, type=float)
    parser.add_argument('-cr', '--constant_right', default=1.0, type=float)
    parser.add_argument('-ct', '--constant_top', default=1.0, type=float)
    parser.add_argument('-cb', '--constant_bottom', default=-1.0, type=float)
    parser.add_argument('-t', '--traversal', default=None, type=str,
                        choices=['diagonal', 'spiral'])
    arguments = parser.parse_args()
    main(arguments)