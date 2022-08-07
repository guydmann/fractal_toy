from __future__ import division
import datetime
import cv2
import numpy as np
from os import mkdir, path


class Fractal(object):
    verbose = False
    width = 200
    height = 200
    precision = 300
    max_iter = precision + 1
    breakout = 8                # this is just a default to make sure it's set, change it
    cr = None
    ci = None
    constants_required = False
    fractal_array = None
    fractal_data_generated = False
    bypass_image_generation = False
    x_inc = None
    y_inc = None
    show_progress_bar = True
    iterative_algorithm = None  # should be set to True or False
    filename = None
    directory = None
    fractal_name = "fractal"
    color_algorithm = None
    color_algorithm_name = None
    viewport = {'left_x': -1.0,
                'right_x': 1.0,
                'top_y': 1.0,
                'bottom_y': -1.0}
    preprocessed = False
    generate_image = True
    image_filter = None

    def dwell_cell(self, x, y):
        pass

    def dwell(self):
        for cx in range(self.width):
            for cy in range(self.height):
                self.fractal_array[cx][cy] = \
                    self.dwell_cell((cx*self.x_inc)+self.viewport['left_x'], self.viewport['top_y']-(cy*self.y_inc))
        return self.fractal_array

    def preprocess(self):
        self.verify_data_preprocessing()

        self.max_iter = self.precision + 1
        self.x_inc = (self.viewport['right_x'] - self.viewport['left_x']) / self.width
        self.y_inc = (self.viewport['top_y'] - self.viewport['bottom_y']) / self.height

        if self.filename is None:
            i = datetime.datetime.now()
            if self.directory is not None:
                if not self.directory.startswith("images/"):
                    self.directory = "images/{}/".format(self.directory)
            else:
                self.directory = "images/"
            if not path.isdir("images"):
                mkdir("images")
            self.set_filename("{}{}_{}_h{}_w{}_{}".format(self.directory,
                                                                 self.fractal_name,
                                                                 self.color_algorithm_name,
                                                                 self.height,
                                                                 self.width,
                                                                 i.isoformat().replace(":","")))
        self.preprocessed = True
        self.fractal_array = Fractal.create_empty_fractal_array(self.width, self.height)

        self.verify_data_postprocessing()

    def apply_post_rendering_image_filters(self):
        image_filters = []
        if self.image_filter == "basic":
            image_filters = ["bilateral_filter"]
        elif self.image_filter == "blur":
            image_filters = ["blur"]
        elif self.image_filter == "glow_takeover":
            image_filters = ["color_glow_takeover", "bilateral_filter"]
        elif self.image_filter == "additive_glow":
            image_filters = ["additive_glow", "bilateral_filter"]

        debugging_cv_output = False
        cv_image_data = original_image = cv2.imread('{}.png'.format(self.filename))
        for image_filter in image_filters:
            if image_filter == "bilateral_filter":
                cv_image_data = cv2.bilateralFilter(cv_image_data, 4, 35, 35)
            if image_filter == "blur":
                cv_image_data = cv2.blur(cv_image_data, (2, 2))
            if image_filter == "additive_color_glow":
                # cv_temp_data = cv2.bilateralFilter(cv_image_data, 4, 35, 35)
                cv_temp_data = cv2.blur(cv_image_data, (2, 2))
                diff = cv2.absdiff(original_image, cv_temp_data)
                mask = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

                th = 1
                imask = mask > th
                canvas = np.zeros_like(cv_image_data, np.uint8)
                canvas[imask] = cv_image_data[imask]

                alpha = 0.8
                beta = (1.0 - alpha)
                cv_image_data = cv2.addWeighted(cv_image_data, alpha, canvas, beta, 20.0)

                if debugging_cv_output:
                    cv2.imshow('Diff Image', canvas)
                    cv2.imshow('Additive Image', cv_image_data)

            if image_filter == "color_glow_takeover":
                cv_temp_data = cv2.blur(cv_image_data, (4, 4))
                # cv_temp_data = cv2.bilateralFilter(cv_image_data, 4, 35, 35)
                diff = cv2.absdiff(original_image, cv_temp_data)
                mask = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

                th = 1
                imask = mask > th
                canvas = np.zeros_like(cv_image_data, np.uint8)
                canvas[imask] = cv_image_data[imask]

                cv_image_data = canvas

                if debugging_cv_output:
                    cv2.imshow('override output', cv_image_data)

            if debugging_cv_output:
                cv2.imshow('Original Image', original_image)
                cv2.imshow('Final Image', cv_image_data)
                cv2.waitKey()
            cv2.imwrite('{}.png'.format(self.filename), cv_image_data)

    def verify_data_preprocessing(self):
        if self.viewport is None:
            raise Exception("viewport not set")
        if self.viewport['right_x'] is None:
            raise Exception("viewport right x not set")
        if self.viewport['left_x'] is None:
            raise Exception("viewport left x not set")
        if self.viewport['top_y'] is None:
            raise Exception("viewport top y not set")
        if self.viewport['bottom_y'] is None:
            raise Exception("viewport bottom y not set")
        if self.width is None:
            raise Exception("width not set")
        if self.height is None:
            raise Exception("height not set")
        if self.color_algorithm_name is None:
            raise Exception("color_algorithm_name not set")
        if self.iterative_algorithm is None:
            raise Exception("iterative_algorithm not set")
        if self.constants_required and self.cr is None:
            raise Exception("real constant not set")
        if self.constants_required and self.ci is None:
            raise Exception("imaginary constant not set")

    def verify_data_postprocessing(self):
        if self.x_inc is None:
            raise Exception("x_inc not set")
        if self.y_inc is None:
            raise Exception("y_inc not set")
        if self.fractal_array is None:
            raise Exception("fractal_array not set")
        if self.preprocessed is None:
            raise Exception("preprocessed not set")
        if not self.preprocessed:
            raise Exception("preprocessed is false")
        if self.filename is None:
            raise Exception("filename not set")

    def render(self):
        pass

    def color(self, pixel_data):
        return self.color_algorithm.color_pixel(pixel_data)

    def set_width(self, new_width):
        self.width = new_width
        if self.fractal_data_generated:
            self.set_fractal_data_generated(False)

    def set_height(self, new_height):
        self.height = new_height
        if self.fractal_data_generated:
            self.set_fractal_data_generated(False)

    def set_fractal_data_generated(self, new_fractal_data_generated):
        self.fractal_data_generated = new_fractal_data_generated

    def set_precision(self, new_precision):
        self.precision = new_precision
        self.max_iter = new_precision + 1
        if self.fractal_data_generated:
            self.set_fractal_data_generated(False)

    def set_filename(self, new_filename):
        self.filename = new_filename

    def set_generate_image(self, new_generate_image):
        self.generate_image = new_generate_image

    def set_color_algorithm_name(self, new_color_algorithm_name):
        self.color_algorithm_name = new_color_algorithm_name

    def set_directory(self, new_directory):
        self.directory = new_directory

    def set_bypass_image_generation(self, new_bypass_image_generation):
        self.bypass_image_generation = new_bypass_image_generation

    def set_viewport(self, new_viewport):
        self.viewport = new_viewport
        if self.fractal_data_generated:
            self.set_fractal_data_generated(False)

    def set_viewport_left(self, new_viewport_left):
        self.viewport['left_x'] = new_viewport_left
        if self.fractal_data_generated:
            self.set_fractal_data_generated(False)

    def set_viewport_right(self, new_viewport_right):
        self.viewport['right_x'] = new_viewport_right
        if self.fractal_data_generated:
            self.set_fractal_data_generated(False)

    def set_viewport_top(self, new_viewport_top):
        self.viewport['top_y'] = new_viewport_top
        if self.fractal_data_generated:
            self.set_fractal_data_generated(False)

    def set_viewport_bottom(self, new_viewport_bottom):
        self.viewport['bottom_y'] = new_viewport_bottom
        if self.fractal_data_generated:
            self.set_fractal_data_generated(False)

    def set_real_constant(self, new_real_constant):
        self.cr = new_real_constant
        if self.fractal_data_generated:
            self.set_fractal_data_generated(False)

    def set_imaginary_constant(self, new_imaginary_constant):
        self.ci = new_imaginary_constant
        if self.fractal_data_generated:
            self.set_fractal_data_generated(False)

    def set_color_algorithm(self, new_color_algorithm):
        new_color_algorithm.set_precision(self.precision)
        self.color_algorithm = new_color_algorithm

    def set_show_progress_bar(self, show):
        self.show_progress_bar = show

    def set_verbose(self, verbose):
        self.verbose = verbose

    def set_image_filtering(self, filter):
        self.image_filter = filter

    @staticmethod
    def create_empty_fractal_array(num_rows, num_cols):
        """
        create_empty_fractal_array generates a 3 dimensional data structure which has a [num_rows][num_cols][3] structure.
        it is used to store the data about the fractals
        @returns an allocated array
        """
        new_fractal_array = [[0 for i in range(num_cols)] for j in range(num_rows)]
        return new_fractal_array
