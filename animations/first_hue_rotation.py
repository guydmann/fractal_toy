from __future__ import division
from progressbar import ProgressBar

__author__ = 'guydmann'

from animations.hue_rotation import HueRotation


class FirstHueRotation(HueRotation):
    animation_name = "first_hue_rotation"

    def generate_images(self):
        calc_pbar = ProgressBar(maxval=self.increments)
        print("Creating Fractal Images")
        calc_pbar.start()
        results = []
        h_start = self.fractal.color_algorithm.start_degree
        h_end = self.fractal.color_algorithm.end_degree
        multiplier = self.color_multiplier
        for k in range(self.increments):
            self.fractal.color_algorithm.set_start_degree((h_start + (multiplier * k)))
            self.fractal.color_algorithm.set_end_degree((h_end + (multiplier * k)))

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
