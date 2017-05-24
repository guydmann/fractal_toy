from __future__ import division
from color import Color


class HueCyclic(Color):
    color_count = 5
    start_degree = 0
    color_step_shift = 30

    def set_color_count(self, new_color_count):
        self.color_count = new_color_count

    def set_start_degree(self, new_start_degree):
        self.start_degree = new_start_degree

    def set_color_step_shift(self, new_color_step_shift):
        self.color_step_shift = new_color_step_shift

    def verify_data(self):
        if self.precision is None:
            raise Exception("precision not set")
        if self.set_start_degree is None:
            raise Exception("start degree not set")
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
            h = round(modcolor*(self.color_step_shift))+self.start_degree
            color = self.hsv_to_rgb(h%360, 100, 100)
        return color
