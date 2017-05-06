from __future__ import division
from iterative_fractal import IterativeFractal

__author__ = 'guydmann'


class Newton(IterativeFractal):
    fractal_name = "newton"
    breakout = 0.00001

    def __init__(self):
        super(IterativeFractal, self).__init__()

    def dwell(self, cx, cy):
        absv2 = 1.0
        x = cx
        y = cy
        count = 0
        for count in range(self.max_iter):
            if absv2 <= self.breakout:
                break
            oldx = x
            oldy = y

            x2 = oldx * oldx
            y2 = oldy * oldy

            r4 = (x2+y2) * (x2+y2)
            if r4 > 0:
                x = (2 * oldx * r4 + x2 - y2) / (3.0*r4)
                y = 2 * oldy * (r4-oldx) / (3.0*r4)
            else:
                return {'count': self.precision, 'x': x, 'y': y}

            absv2 = (x-oldx) * (x-oldx) + (y-oldy) * (y-oldy)

        if absv2 > self.breakout:
            count = self.precision
        return {'count': count, 'x': x, 'y': y}