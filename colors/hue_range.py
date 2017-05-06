from __future__ import division
from color import Color


class HueRange(Color):
    start_degree = 0    # start_degree: the degree at which to start the hue transition 0-360
    end_degree = 360    # end_degree: the degree at which to end the hue transition 0-360

    def set_start_degree(self, new_start_degree):
        self.start_degree = new_start_degree

    def set_end_degree(self, new_end_degree):
        self.end_degree = new_end_degree

    def verify_data(self):
        if self.precision is None:
            raise Exception("precision not set")
        if self.start_degree is None or self.end_degree is None:
            raise Exception("start and end degree not set")

    def color_pixel(self, pixel_data):
        """
            pixel_data: data about the pixel to color
        """
        self.verify_data()

        color = (0, 0, 0)
        if pixel_data['count'] < self.precision:
            h = round((pixel_data['count']/self.precision)*(self.end_degree-self.start_degree))+self.start_degree
            color = self.hsv_to_rgb(h, 100, 100)
        return color

