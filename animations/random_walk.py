from __future__ import division
from progressbar import ProgressBar
from imageio import mimsave
from PIL import Image
from animations.animation import Animation
from fractals.julia import Julia
import math
import copy
import random

__author__ = 'guydmann'


class RandomWalk(Animation):
    animation_name = "random_walk"

    def animate(self):
        self.preprocess()

        fractal_backup = copy.deepcopy(self.fractal)

        calc_pbar = ProgressBar(maxval=360)
        print("Generating Mandelbrot Set")
        self.fractal.set_bypass_image_generation(True)
        self.render_fractal()

        random_x = random.randint(0, self.fractal.width-1)
        random_y = random.randint(0, self.fractal.height-1)
        print("Searching for Starting Point")
        while (self.fractal.fractal_array[random_x][random_y]['count'] < self.fractal.precision*.8):
            random_x = random.randint(0, self.fractal.width-1)
            random_y = random.randint(0, self.fractal.height-1)

        print("Creating Fractal Images")
        calc_pbar.start()
        results = []


        for k in range(self.increments):
            self.fractal = Julia()
            # self.fractal
            self.fractal.set_filename("{}{}_{}_{}_{}".format(self.fractal.directory,
                                                             self.animation_name,
                                                             k,
                                                             self.fractal.color_algorithm.start_degree,
                                                             self.fractal.color_algorithm.end_degree))
            results.append(self.render_fractal())
            self.fractal.color_algorithm.set_start_degree((int)(math.sin(math.radians(h_start+(multiplier*k)))*360))
            self.fractal.color_algorithm.set_end_degree((int)(math.sin(math.radians(h_end+(multiplier*k)))*360))
            calc_pbar.update(k)
        calc_pbar.finish()

        for image_file in results:
            self.images.append(Image.open(image_file).convert('RGBA'))

        mimsave("{}.gif".format(self.filename), self.images)