from __future__ import division
from progressbar import ProgressBar
from imageio import mimsave
from PIL import Image
from animations.animation import Animation
import math

__author__ = 'guydmann'


class SecondHueRotation(Animation):
    animation_name = "second_hue_rotation"

    def animate(self):
        self.preprocess()

        calc_pbar = ProgressBar(maxval=360)
        print("Creating Fractal Images")
        calc_pbar.start()
        results = []
        h_start = self.fractal.color_algorithm.start_degree
        h_end = self.fractal.color_algorithm.end_degree
        multiplier = (int)((h_end-h_start)/self.increments)
        for k in range(self.increments):
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