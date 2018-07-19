from __future__ import division
from progressbar import ProgressBar
from imageio import mimsave, imread
from animations.animation import Animation

__author__ = 'guydmann'


class FirstHueRotation(Animation):
    animation_name = "first_hue_rotation"

    def animate(self):
        self.preprocess()

        calc_pbar = ProgressBar(maxval=360)
        print("Creating Fractal Images")
        calc_pbar.start()
        results = []
        h_start = self.fractal.color_algorithm.start_degree
        h_end = self.fractal.color_algorithm.end_degree
        multiplier = int(360/self.increments)
        for k in range(self.increments):
            self.fractal.set_filename("{}{}_{}_{}_{}".format(self.fractal.directory,
                                                             self.animation_name,
                                                             k,
                                                             self.fractal.color_algorithm.start_degree,
                                                             self.fractal.color_algorithm.end_degree))
            results.append(self.render_fractal())
            self.fractal.color_algorithm.set_start_degree((h_start + (multiplier * k)) % 360)
            self.fractal.color_algorithm.set_end_degree((h_end + (multiplier * k)) % 360)
            calc_pbar.update(k)
        calc_pbar.finish()

        for image_file in results:
            self.images.append(imread(image_file))

        mimsave("{}.gif".format(self.filename), self.images)
