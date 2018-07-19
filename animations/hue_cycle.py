from __future__ import division
from imageio import mimsave, imread
from progressbar import ProgressBar
from animations.animation import Animation

__author__ = 'guydmann'


class HueCycle(Animation):
    animation_name = "hue_cycle"

    def animate(self):
        self.preprocess()

        calc_pbar = ProgressBar(maxval=360)
        print("Creating Fractal Images")
        calc_pbar.start()
        results = []
        for k in range(self.increments):
            self.fractal.set_filename("{}{}_{}_{}_{}".format(self.fractal.directory,
                                                             self.animation_name,
                                                             k,
                                                             self.fractal.color_algorithm.start_degree,
                                                             self.fractal.color_algorithm.color_step_shift))
            results.append(self.render_fractal())
            #iterate hue cycle
            self.fractal.color_algorithm.\
                set_start_degree(self.fractal.color_algorithm.start_degree + \
                                 self.fractal.color_algorithm.color_step_shift)
            calc_pbar.update(k)
        calc_pbar.finish()
        for image_file in results:
            self.images.append(imread(image_file))

        mimsave("{}.gif".format(self.filename), self.images)