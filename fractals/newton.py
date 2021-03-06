from __future__ import division
from fractals.iterative_fractal import IterativeFractal


class Newton(IterativeFractal):
    fractal_name = "newton"
    breakout = 0.00001

    def dwell_cell(self, cx, cy):
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
                return self.precision

            absv2 = (x-oldx) * (x-oldx) + (y-oldy) * (y-oldy)

        if absv2 > self.breakout:
            count = self.precision
        return count
