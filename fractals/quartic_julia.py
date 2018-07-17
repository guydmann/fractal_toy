from julia import Julia
import numpy as np

__author__ = 'guydmann'


class QuarticJulia(Julia):
    fractal_name = "quartic_julia"
    breakout = 128

    def __init__(self):
        super(Julia, self).__init__()

    def dwell_cell(self, cx, cy):
        x = cx
        y = cy
        x2 = x * x
        y2 = y * y
        # z <= z(n-1)^4 +c
        count = 0
        for count in range(self.max_iter):
            if (x2 + y2) > self.breakout:
                break
            xsqr = (x * x) - (y * y)
            ysqr = (x * y) + (y * x)

            x = (xsqr * xsqr) - (ysqr * ysqr)
            y = (xsqr * ysqr) + (ysqr * xsqr)

            x = x + self.cr
            y = y + self.ci

            x2 = x * x
            y2 = y * y
        return count


    def dwell(self):
        x = np.full((self.width, self.height), self.cr)
        y = np.full((self.width, self.height), self.ci)
        c = x+complex(0,1)*y
        del x, y
        ix, iy = np.mgrid[0:self.width, 0:self.height]
        x = np.linspace(self.viewport['left_x'], self.viewport['right_x'], self.width)[ix]
        y = np.linspace(self.viewport['bottom_y'], self.viewport['top_y'], self.height)[iy]
        z = x+complex(0,1)*y
        del x, y

        img = np.zeros(c.shape, dtype=int)
        ix.shape = self.width*self.height
        iy.shape = self.width*self.height
        c.shape = self.width*self.height
        z.shape = self.width*self.height
        for i in xrange(self.precision):
            if not len(z): break

            #z <= z(n-1)^4 +c
            zn_minus1 = np.copy(z)
            np.multiply(z, z, z)
            np.multiply(z, zn_minus1, z)
            np.multiply(z, zn_minus1, z)
            del zn_minus1
            np.add(z, c, z)

            rem = abs(z)>self.breakout
            img[ix[rem], iy[rem]] = i+1
            rem = -rem
            z = z[rem]
            ix, iy = ix[rem], iy[rem]
            c = c[rem]

        img[img==0] = self.max_iter
        return img