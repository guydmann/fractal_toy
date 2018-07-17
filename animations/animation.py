import datetime
from fractal_lib import FractalLib
from os import mkdir

__author__ = 'guydmann'


class Animation(object):
    fractal = None
    filename = None
    animation_name = None
    increments = None
    images = []

    def animate(self):
        pass

    def set_fractal(self, new_fractal):
        self.fractal = new_fractal

    def set_filename(self, new_filename):
        self.filename = new_filename

    def set_increments(self, new_increments):
        self.increments = new_increments

    def preprocess(self):
        self.fractal.directory = self.animation_name
        if not self.fractal.preprocessed:
            self.fractal.preprocess()

        if self.filename is None:
            i = datetime.datetime.now()
            if self.fractal.directory is not None:
                self.directory = "{}/".format(self.fractal.directory)
            else:
                self.directory = ""
            self.set_filename("{}{}_{}_{}_h{}_w{}_{}".format(self.fractal.directory,
                                                                 self.animation_name,
                                                                 self.fractal.fractal_name,
                                                                 self.fractal.color_algorithm_name,
                                                                 self.fractal.height,
                                                                 self.fractal.width,
                                                                 i.isoformat()))

        FractalLib.empty_dir_and_remove("{}".format(self.fractal.directory))
        mkdir("{}".format(self.fractal.directory))
        self.verify_data_postprocessing()

    def verify_data_postprocessing(self):
        if self.fractal is None:
            raise Exception("fractal not set")
        if self.filename is None:
            raise Exception("filename not set")

    def render_fractal(self):
        return self.fractal.render()
