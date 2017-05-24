from __future__ import division
from math import floor
from traversal_fractal import TraversalFractal

__author__ = 'guydmann'


class Buddhabrot(TraversalFractal):
    fractal_name = "buddhabrot"
    breakout = 4

    def __init__(self):
        super(TraversalFractal, self).__init__()
        self.set_viewport_left(-1.5)
        self.set_viewport_right(0.5)

    def dwell_cell(self, cx, cy):
        x = cx
        y = cy
        x2 = x * x
        y2 = y * y
        #z <= z(n-1)^2 +c
        for count in range(self.max_iter):
            if (x2 + y2) > self.breakout:
                break
            y = (2.0 * (x * y)) + cy
            x = x2 - y2 + cx
            x2 = x * x
            y2 = y * y

            j_t = int(floor((x-self.viewport['left_x'])/self.x_inc))
            k_t = int(floor((self.viewport['top_y']-y)/self.y_inc))
            if 0 <= j_t < self.width and 0 <= k_t < self.height:
                if self.fractal_array[j_t][k_t] == self.precision:
                    self.fractal_array[j_t][k_t] = 1
                else:
                    self.fractal_array[j_t][k_t] += 1
        return self.fractal_array
