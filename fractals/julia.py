from fractals.iterative_fractal import IterativeFractal
import numpy as np


class Julia(IterativeFractal):
    fractal_name = "julia"
    constants_required = True
    breakout = 8
    cr = 0
    ci = 0
    viewport = {'left_x': -2,
                'right_x': 2,
                'top_y': 2,
                'bottom_y': -2}

    def dwell_cell(self, cx, cy):
        x = cx
        y = cy

        x2 = x*x
        y2 = y*y
        count = 0
        for count in range(self.max_iter):
            if x2+y2 > self.breakout:
                break
            y = (2*x*y) + self.ci
            x = x2-y2+self.cr
            x2 = x*x
            y2 = y*y
        return count

    def dwell(self):
        x = np.full((self.width, self.height), self.cr)
        y = np.full((self.width, self.height), self.ci)
        c = x+complex(0, 1)*y
        del x, y
        ix, iy = np.mgrid[0:self.width, 0:self.height]
        x = np.linspace(self.viewport['left_x'], self.viewport['right_x'], self.width)[ix]
        y = np.linspace(self.viewport['bottom_y'], self.viewport['top_y'], self.height)[iy]
        z = x+complex(0, 1)*y
        del x, y

        img = np.zeros(c.shape, dtype=int)
        ix.shape = self.width * self.height
        iy.shape = self.width * self.height
        c.shape = self.width * self.height
        z.shape = self.width * self.height
        for i in range(self.precision):
            if not len(z):
                break

            np.multiply(z, z, z)
            np.add(z, c, z)

            rem = abs(z) > self.breakout
            img[ix[rem], iy[rem]] = i + 1
            rem = ~rem
            z = z[rem]
            ix, iy = ix[rem], iy[rem]
            c = c[rem]

        img[img == 0] = self.max_iter
        return img
