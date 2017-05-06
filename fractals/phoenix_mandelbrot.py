from iterative_fractal import IterativeFractal

__author__ = 'guydmann'


class PhoenixMandelbrot(IterativeFractal):
    fractal_name = "phoenic_mandelbrot"
    breakout = 8

    def __init__(self):
        super(IterativeFractal, self).__init__()

    def dwell(self, cx, cy):
        x = cx
        y = cy
        cr = cx
        ci = cy
        xprev = 0
        yprev = 0

        x2 = x*x
        y2 = y*y
        # equation z[n+1] <= z[n]^2 +Re(c) + Im(c)*z[n-1]
        count = 0
        for count in range(self.max_iter):
            if x2+y2 > self.breakout:
                break

            xint = -1 * yprev * ci
            yint = xprev * ci

            xint += cr

            xprev = x
            yprev = y

            x = (x2-y2) + xint
            y = (2*x*y) + yint

            x2 = x*x
            y2 = y*y

        return {'count': count, 'x': x, 'y': y}