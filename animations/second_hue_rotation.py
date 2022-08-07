from __future__ import division
from progressbar import ProgressBar
import math

__author__ = 'guydmann'

from animations.hue_rotation import HueRotation


class SecondHueRotation(HueRotation):
    animation_name = "second_hue_rotation"

    def generate_images(self):
        calc_pbar = ProgressBar(maxval=self.increments)
        print("Creating Fractal Images")
        calc_pbar.start()
        results = []
        h_start = self.fractal.color_algorithm.start_degree
        h_end = self.fractal.color_algorithm.end_degree
        multiplier = (h_end-h_start) / self.increments
        for k in range(self.increments):
            self.fractal.color_algorithm.set_start_degree((int)(abs(math.sin(math.radians((h_start+(multiplier*k)))/(2*math.pi)))*360))
            self.fractal.color_algorithm.set_end_degree((int)(abs(math.sin(math.radians((h_end+(multiplier*k)))/(2*math.pi)))*360))

            self.fractal.set_filename("{}{}_{}_{}_{}".format(self.fractal.directory,
                                                             self.animation_name,
                                                             k,
                                                             self.fractal.color_algorithm.start_degree,
                                                             self.fractal.color_algorithm.end_degree))
            results.append(self.render_fractal())

            calc_pbar.update(k)
        calc_pbar.finish()

        output = []
        for image_file in results:
            output.append(image_file)
        for image_file in reversed(results):
            output.append(image_file)
        return output

