from __future__ import division
from progressbar import ProgressBar
from images2gif import writeGif
from PIL import Image
from animation import Animation

__author__ = 'guydmann'


class HueCycle(Animation):
    animation_name = "hue_cycle"

    def animate(self):
        self.preprocess()

        print "Creating Fractal Images"
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
        for image_file in results:
            self.images.append(Image.open(image_file).convert('RGBA'))

        writeGif("{}.gif".format(self.filename), self.images)