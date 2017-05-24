from __future__ import division
from math import floor
from buddhabrot import Buddhabrot

__author__ = 'guydmann'


class BuddhabrotJulia(Buddhabrot):
    fractal_name = "buddhabrot_julia"
    breakout = 8
    constants_required = True
    cr = 0
    ci = 0

    def __init__(self):
        super(Buddhabrot, self).__init__()

    def dwell_cell(self, cx, cy):
        x = cx
        y = cy
        x2 = x*x
        y2 = y*y
        for count in range(self.max_iter):
            if (x2+y2) > self.breakout:
                break

            y = (2*x*y) + self.ci
            x = x2-y2+self.cr
            x2 = x*x
            y2 = y*y

            j_t = int(floor((x-self.viewport['left_x'])/self.x_inc))
            k_t = int(floor((self.viewport['top_y']-y)/self.y_inc))
            if 0 <= j_t < self.width and 0 <= k_t < self.height:
                if self.fractal_array[j_t][k_t] == self.precision:
                    self.fractal_array[j_t][k_t] = 1
                else:
                    self.fractal_array[j_t][k_t] += 1
        return self.fractal_array