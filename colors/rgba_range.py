from __future__ import division
from colors.color import Color


class RGBARange(Color):
    color_count = 5
    start_color = {'red': 0, 'green': 0, 'blue': 0, 'alpha': 255}
    end_color = {'red': 255, 'green': 255, 'blue': 255, 'alpha': 255}

    def set_start_color(self, new_start_color):
        self.start_color = new_start_color

    def set_end_color(self, new_end_color):
        self.end_color = new_end_color

    def set_color_count(self, new_color_count):
        self.color_count = new_color_count

    def verify_data(self):
        if self.precision is None:
            raise Exception("precision not set")
        if self.start_color is None:
            raise Exception("start color not set")
        if self.end_color is None:
            raise Exception("end color not set")
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
            R = (((modcolor * (self.end_color['red'] - self.start_color['red'])) + self.start_color['red']) % 256)
            G = (((modcolor * (self.end_color['green'] - self.start_color['green'])) + self.start_color['green']) % 256)
            B = (((modcolor * (self.end_color['blue'] - self.start_color['blue'])) + self.start_color['blue']) % 256)
            A = (((modcolor * (self.end_color['alpha'] - self.start_color['alpha'])) + self.start_color['alpha']) % 256)
            color = (int(R), int(G), int(B), int(A))
        return color
