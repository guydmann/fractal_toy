from math import floor


class ColorLib:

    @staticmethod
    def black_and_white(fractal_pixel_data, precision):
        color = (0, 0, 0)
        if fractal_pixel_data['count'] < precision:
            color = (255, 255, 255, 255)
        return color

    @staticmethod
    def simple(fractal_pixel_data, precision):
        color = (0, 0, 0)
        if fractal_pixel_data['count'] < precision*.03:
            color = (255, 0, 0, 255)
        elif fractal_pixel_data['count'] < precision*.05:
            color = (255, 255, 0, 255)
        elif fractal_pixel_data['count'] < precision*.1:
            color = (0, 255, 0, 255)
        elif fractal_pixel_data['count'] < precision*.2:
            color = (0, 255, 255, 255)
        elif fractal_pixel_data['count'] < precision:
            color = (0, 0, 255, 255)
        return color

    @staticmethod
    def h_iter_range(self, start_degree, end_degree, fractal_pixel_data, precision):
        """
            start_degree: the degree at which to start the hue transition 0-360
            end_degree: the degree at which to end the hue transition 0-360
            fractal_pixel_data: data about the pixel to color
            precision: the precision at which the fractal was calculated
        """
        color = (0, 0, 0)
        if fractal_pixel_data['count'] < precision:
            h = round((fractal_pixel_data['count']/precision)*(end_degree-start_degree))+start_degree
            color = self.hsv_to_rgb(h, 100, 100)
        return color

    @staticmethod
    def rgba_cyclic(color_count, start_color, color_step_shift, fractal_pixel_data, precision):
        """
            color_count: number of colors to rotate through
            start_color: color to start with {'red': red_value, 'green': green_value, 'blue': blue_value, 'alpha': alpha_value}
            color_step_shift: amount of color to shirt on each step {'red': red_value, 'green': green_value, 'blue': blue_value, 'alpha': alpha_value}
            fractal_pixel_data: data about the pixel to color
            precision: the precision at which the fractal was calculated
        """
        color = (0, 0, 0)
        if fractal_pixel_data['count'] < precision:
            color_count = color_count
            modcolor = fractal_pixel_data['count'] % color_count
            r = start_color['red'] + ((modcolor*color_step_shift['red']) % 255)
            g = start_color['green'] + ((modcolor*color_step_shift['green']) % 255)
            b = start_color['blue'] + ((modcolor*color_step_shift['blue']) % 255)
            a = start_color['alpha'] + ((modcolor*color_step_shift['alpha']) % 255)
            color = (int(r), int(g), int(b), int(a))
        return color

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
        # that conversion here.
        s /= 100
        v /= 100

        if s == 0:
            # Achromatic (grey)
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

        return int(round(r * 255)), int(round(g * 255)), int(round(b * 255))
