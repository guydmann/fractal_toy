from __future__ import division
from math import floor


class Color(object):
    precision = None    # precision: the precision at which the fractal was calculated

    def __init__(self):
        pass

    def color_pixel(self, pixel_data):
        pass

    def verify_data(self):
        if self.precision is None:
            raise Exception("precision not set")

    def set_precision(self, new_precision):
        self.precision = new_precision

    @staticmethod
    def hsv_to_rgb(h, s, v):
        """
        HSV to RGB color conversion

        H runs from 0 to 360 degrees
        S and V run from 0 to 100

        Ported from the excellent java algorithm by Eugene Vishnevsky at:
        http://www.cs.rit.edu/~ncs/color/t_convert.html
        """

        # Make sure our arguments stay in-range
        h = max(0, min(360, h))
        s = max(0, min(100, s))
        v = max(0, min(100, v))

        # We accept saturation and value arguments from 0 to 100 because that's
        # how Photoshop represents those values. Internally, however, the
        # saturation and value are calculated from a range of 0 to 1. We make
        #That conversion here. \
        s /= 100
        v /= 100

        if s == 0:
            #Achromatic (grey)
            r = g = b = v
            return [round(r * 255), round(g * 255), round(b * 255)]

        h /= 60         # sector 0 to 5
        i = floor(h)
        f = h - i       # factorial part of h
        p = v * (1 - s)
        q = v * (1 - s * f)
        t = v * (1 - s * (1 - f))

        if i == 0:
            r = v
            g = t
            b = p

        elif i == 1:
            r = q
            g = v
            b = p
        elif i == 2:
            r = p
            g = v
            b = t
        elif i == 3:
            r = p
            g = q
            b = v
        elif i == 4:
            r = t
            g = p
            b = v
        else:       # case 5
            r = v
            g = p
            b = q

        return (int(round(r * 255)), int(round(g * 255)), int(round(b * 255)))