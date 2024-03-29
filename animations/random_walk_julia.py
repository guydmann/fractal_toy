from __future__ import division
from progressbar import ProgressBar
from animations.animation import Animation
from fractals.julia import Julia
import numpy as np
import copy
import random

__author__ = 'guydmann'


class RandomWalkJulia(Animation):
    animation_name = "random_walk_julia"

    def generate_images(self):
        fractal_backup = copy.deepcopy(self.fractal)

        calc_pbar = ProgressBar(maxval=self.increments)
        print("Generating Mandelbrot Set")
        self.fractal.set_bypass_image_generation(True)
        self.render_fractal()

        random_x = random.randint(0, self.fractal.width-1)
        random_y = random.randint(0, self.fractal.height-1)
        print("Searching for Starting Point")
        while not (self.fractal.precision > self.fractal.fractal_array[random_x][random_y] >= self.fractal.precision*.95):
            random_x = random.randint(0, self.fractal.width-1)
            random_y = random.randint(0, self.fractal.height-1)
        print("the Mandelbrot Value is {val}".format(val=self.fractal.fractal_array[random_x][random_y]))

        real_space = np.linspace(self.fractal.viewport['left_x'], self.fractal.viewport['right_x'], self.fractal.width)
        imaginary_space = np.linspace(self.fractal.viewport['bottom_y'], self.fractal.viewport['top_y'],
                                      self.fractal.height)
        x = real_space[random_x]
        y = imaginary_space[random_y]

        print("Creating Fractal Images")
        calc_pbar.start()
        results = []

        self.fractal = Julia()
        self.fractal.set_directory(fractal_backup.directory)
        self.fractal.set_color_algorithm_name(fractal_backup.color_algorithm_name)
        self.fractal.set_color_algorithm(fractal_backup.color_algorithm)

        self.fractal.set_viewport_left(fractal_backup.viewport['left_x'])
        self.fractal.set_viewport_right(fractal_backup.viewport['right_x'])
        self.fractal.set_viewport_top(fractal_backup.viewport['top_y'])
        self.fractal.set_viewport_bottom(fractal_backup.viewport['bottom_y'])

        self.fractal.set_width(fractal_backup.width)
        self.fractal.set_height(fractal_backup.height)
        self.fractal.set_precision(fractal_backup.precision)
        self.fractal.set_image_filtering(fractal_backup.image_filter)

        self.fractal.set_real_constant(x)
        self.fractal.set_imaginary_constant(y)
        previously_used = []


        for k in range(self.increments):
            self.fractal.set_filename("{}{}_{}_forward".format(self.fractal.directory, self.animation_name, k))
            results.append(self.render_fractal())
            calc_pbar.update(k)

            prev_x = random_x
            prev_y = random_y
            previously_used.append((prev_x, prev_y))
            while random_x == prev_x and random_y == prev_y and (random_x, random_y) in previously_used:
                random_x += random.randint(-1, 1)
                random_y += random.randint(-1, 1)
            x = real_space[random_x]
            y = imaginary_space[random_y]
            self.fractal.set_real_constant(x)
            self.fractal.set_imaginary_constant(y)

        calc_pbar.finish()

        output = []
        for image_file in results:
            output.append(image_file)
            output.append(image_file)
            output.append(image_file)
        for image_file in reversed(results):
            output.append(image_file)
            output.append(image_file)
            output.append(image_file)
        return output

