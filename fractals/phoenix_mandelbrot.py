from fractals.iterative_fractal import IterativeFractal
import numpy as np


class PhoenixMandelbrot(IterativeFractal):
    fractal_name = "phoenic_mandelbrot"
    breakout = 8

    def __init__(self):
        super(IterativeFractal, self).__init__()

    def dwell_cell(self, cx, cy):
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

        return count

    def dwell(self):
        # equation z[n+1] <= z[n]^2 +Re(c) + Im(c)*z[n-1]
        ix, iy = np.mgrid[0:self.width, 0:self.height]
        x = np.linspace(self.viewport['left_x'], self.viewport['right_x'], self.width)[ix]
        y = np.linspace(self.viewport['bottom_y'], self.viewport['top_y'], self.height)[iy]
        c = x+complex(0, 1)*y
        x = x+complex(0, 1)*0
        y = 0+complex(0, 1)*y

        img = np.zeros(c.shape, dtype=int)
        shape = self.width*self.height
        ix.shape = shape
        iy.shape = shape
        x.shape = shape
        y.shape = shape
        c.shape = shape
        z = np.copy(c)
        for i in range(self.precision):
            if not len(z):
                break

            zn_minus_1 = z
            np.multiply(z, z, z)
            np.add(z, x, z)
            temp_c = np.copy(y)
            np.multiply(temp_c, zn_minus_1, temp_c)
            np.add(z, temp_c, z)

            rem = abs(z) > self.breakout
            img[ix[rem], iy[rem]] = i + 1
            rem = ~rem
            z = z[rem]
            ix, iy = ix[rem], iy[rem]
            x, y = x[rem], y[rem]
            c = c[rem]
        img[img == 0] = self.max_iter
        return img
