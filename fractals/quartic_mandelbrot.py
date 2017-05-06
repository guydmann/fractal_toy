from iterative_fractal import IterativeFractal

__author__ = 'guydmann'


class QuarticMandelbrot(IterativeFractal):
    fractal_name = "quartic_mandelbrot"
    breakout = 128

    def __init__(self):
        super(IterativeFractal, self).__init__()

    def dwell(self, cx, cy):
        x = cx
        y = cy
        x2 = x * x
        y2 = y * y
        #z <= z(n-1)^3 +c
        count = 0
        for count in range(self.max_iter):
            if (x2 + y2) > self.breakout:
                break
            xsqr = (x * x) - (y * y)
            ysqr = (x * y) + (y * x)

            x = (xsqr * xsqr) - (ysqr * ysqr)
            y = (xsqr * ysqr) + (ysqr * xsqr)

            x = x + cx
            y = y + cy

            x2 = x * x
            y2 = y * y
        return {'count': count, 'x': x, 'y': y}