from __future__ import division
from progressbar import ProgressBar
from animations.animation import Animation
from fractals.julia import Julia
import numpy as np
import copy
import random

__author__ = 'guydmann'


class JuliaSearchingWalk(Animation):
    animation_name = "julia_searching_walk"

    def generate_images(self):
        fractal_backup = copy.deepcopy(self.fractal)

        calc_pbar = ProgressBar(maxval=self.increments)
        print("Generating Mandelbrot Set")
        # set the width and height really big so we can animate more smoothly
        self.fractal.set_width(self.fractal.width*4)
        self.fractal.set_height(self.fractal.height*4)
        self.fractal.set_bypass_image_generation(True)
        self.render_fractal()

        x_index = random.randint(0, self.fractal.width-1)
        y_index = random.randint(0, self.fractal.height-1)
        print("Searching for Starting Point")
        search_array = self.fractal.fractal_array
        x_coord_array = np.linspace(self.fractal.viewport['left_x'], self.fractal.viewport['right_x'], self.fractal.width)
        y_corrd_array = np.linspace(self.fractal.viewport['bottom_y'], self.fractal.viewport['top_y'], self.fractal.height)
        while not (self.fractal.precision > search_array[x_index][y_index] >= self.fractal.precision*.5):
            x_index = random.randint(0, self.fractal.width-1)
            y_index = random.randint(0, self.fractal.height-1)
        print("the Mandelbrot Value is {val}".format(val=search_array[x_index][y_index]))

        x = x_coord_array[x_index]
        y = y_corrd_array[y_index]

        previously_visited = []

        def search_adjacent_cells_for_most_interesting(current_x_index, current_y_index):
            max_val = None
            new_x_index = None
            new_y_index = None
            for m in range(-1, 2):
                for j in range(-1, 2):
                    # skip the current value
                    if (current_x_index + m, current_y_index + j) not in previously_visited:
                        if max_val is None or search_array[current_x_index + m][current_y_index + j] > max_val:
                            max_val = search_array[current_x_index + m][current_y_index + j]
                            new_x_index = current_x_index + m
                            new_y_index = current_y_index + j
                            print("{x}, {y}: {max}".format(x=m, y=j, max=max_val))

            return new_x_index, new_y_index

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
        for k in range(self.increments):
            self.fractal.set_filename("{}{}_{}_forward".format(self.fractal.directory, self.animation_name, k))
            results.append(self.render_fractal())
            calc_pbar.update(k)
            previously_visited.append((x_index, y_index))
            (x_index, y_index) = search_adjacent_cells_for_most_interesting(x_index, y_index)
            x = x_coord_array[x_index]
            y = y_corrd_array[y_index]

            self.fractal.set_real_constant(x)
            self.fractal.set_imaginary_constant(y)

        calc_pbar.finish()

        output = []
        for image_file in results:
            output.append(image_file)
        for image_file in reversed(results):
            output.append(image_file)
        return output
