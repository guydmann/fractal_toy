from fractals.julia import Julia
import numpy as np


class PhoenixJulia(Julia):
    fractal_name = "phoenix_julia"
    breakout = 128

    def __init__(self):
        super(Julia, self).__init__()

    def dwell_cell(self, cx, cy):
        x = cx
        y = cy
        xprev = 0
        yprev = 0

        x2 = x*x
        y2 = y*y
        # z[n+1] <= z[n]^2 +Re(c) + Im(c)*z[n-1]
        count = 0
        for count in range(self.max_iter):
            if x2+y2 > self.breakout:
                break

            xint = -1 * yprev * self.ci
            yint = xprev * self.ci

            xint += self.cr

            xprev = x
            yprev = y

            x = (x2-y2) + xint
            y = (2*x*y) + yint

            x2 = x*x
            y2 = y*y

        return count

    def dwell(self):
        ix, iy = np.mgrid[0:self.width, 0:self.height]
        x = np.linspace(self.viewport['left_x'], self.viewport['right_x'], self.width)[ix]
        y = np.linspace(self.viewport['bottom_y'], self.viewport['top_y'], self.height)[iy]
        z = x+complex(0, 1)*y
        del x, y

        cx = np.full((self.width, self.height), self.cr)
        cy = np.full((self.width, self.height), self.ci)
        cx = cx+complex(0, 1)*0
        cy = 0+complex(0, 1)*cy

        img = np.zeros(cx.shape, dtype=int)
        shape = self.width*self.height
        ix.shape = shape
        iy.shape = shape
        cx.shape = shape
        cy.shape = shape
        z.shape = shape
        for i in range(self.precision):
            if not len(z):
                break

            zn_minus_1 = z
            np.multiply(z, z, z)
            np.add(z, cx, z)
            temp_c = np.copy(cy)
            np.multiply(temp_c, zn_minus_1, temp_c)
            np.add(z, temp_c, z)

            rem = abs(z) > self.breakout
            img[ix[rem], iy[rem]] = i + 1
            rem = ~rem
            z = z[rem]
            ix, iy = ix[rem], iy[rem]
            cx, cy = cx[rem], cy[rem]

        img[img == 0] = self.max_iter
        return img
