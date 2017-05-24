import numpy as np
from iterative_fractal import IterativeFractal


class Mandelbrot(IterativeFractal):
    fractal_name = "mandelbrot"
    breakout = 4
    viewport = {'left_x': -1.5,
                'right_x': 0.5,
                'top_y': 1.0,
                'bottom_y': -1.0}

    def dwell_cell(self, cx, cy):
        # equation
        # z <= z(n-1)^2 +c
        x = cx
        y = cy
        x2 = x * x
        y2 = y * y

        count = 0
        for count in range(self.max_iter):
            if (x2 + y2) > self.breakout:
                break
            y = (2 * (x * y)) + cy
            x = x2 - y2 + cx
            x2 = x * x
            y2 = y * y
        return count

    def dwell(self):
        ix, iy = np.mgrid[0:self.width, 0:self.height]
        x = np.linspace(self.viewport['left_x'], self.viewport['right_x'], self.width)[ix]
        y = np.linspace(self.viewport['bottom_y'], self.viewport['top_y'], self.height)[iy]
        c = x+complex(0,1)*y
        del x, y
        img = np.zeros(c.shape, dtype=int)
        ix.shape = self.width*self.height
        iy.shape = self.width*self.height
        c.shape = self.width*self.height
        z = np.copy(c)
        for i in xrange(self.precision):
            if not len(z): break

            # z = z^2 + c
            np.multiply(z, z, z)
            np.add(z, c, z)

            rem = abs(z)>self.breakout
            img[ix[rem], iy[rem]] = i+1
            rem = -rem
            z = z[rem]
            ix, iy = ix[rem], iy[rem]
            c = c[rem]

        img[img==0] = self.max_iter
        return img