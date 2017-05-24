from iterative_fractal import IterativeFractal

__author__ = 'guydmann'


class CubicMandelbrot(IterativeFractal):
    fractal_name = "cubic_mandelbrot"
    breakout = 8

    def __init__(self):
        super(IterativeFractal, self).__init__()

    def dwell_cell(self, cx, cy):
        x = cx
        y = cy
        x2 = x * x
        y2 = y * y
        #z <= z(n-1)^3 +c
        count = 0
        for count in range(self.max_iter):
            if (x2 + y2) > self.breakout:
                break
            xsqr = x2 - y2
            ysqr = 2.0 * (y * x)

            tmp = (xsqr * x) - (ysqr * y)
            y = (xsqr * y) + (ysqr * x)
            x = tmp

            x += cx
            y += cy

            x2 = x * x
            y2 = y * y
        return count