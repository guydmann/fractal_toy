from __future__ import division
from colors.color import Color


class RGBACyclic(Color):
    color_count = 5
    start_color = {'red': 0, 'green': 0, 'blue': 0, 'alpha': 255}
    color_step_shift = {'red': 50, 'green': 50, 'blue': 50, 'alpha': 0}

    def set_color_count(self, new_color_count):
        self.color_count = new_color_count

    def set_start_color(self, new_start_color):
        self.start_color = new_start_color

    def set_color_step_shift(self, new_color_step_shift):
        self.color_step_shift = new_color_step_shift

    def verify_data(self):
        if self.precision is None:
            raise Exception("precision not set")
        if self.start_color is None:
            raise Exception("start color not set")
        if self.color_step_shift is None:
            raise Exception("color step shift not set")
        if self.color_count is None:
            raise Exception("color count not set")

    def color_pixel(self, pixel_data):
        """
            pixel_data: data about the pixel to color
        """
        self.verify_data()

        color = (0, 0, 0)
        if pixel_data < self.precision:
            modcolor = pixel_data % self.color_count
            R = self.start_color['red'] + ((modcolor*self.color_step_shift['red']) % 255)
            G = self.start_color['green'] + ((modcolor*self.color_step_shift['green']) % 255)
            B = self.start_color['blue'] + ((modcolor*self.color_step_shift['blue']) % 255)
            A = self.start_color['alpha'] + ((modcolor*self.color_step_shift['alpha']) % 255)
            color = (int(R), int(G), int(B), int(A))
        return color
