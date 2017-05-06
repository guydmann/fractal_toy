from julia import Julia

__author__ = 'guydmann'


class PhoenixJulia(Julia):
    fractal_name = "phoenix_julia"
    breakout = 128

    def __init__(self):
        super(Julia, self).__init__()

    def dwell(self, cx, cy):
        x = cx
        y = cy
        xprev = 0
        yprev = 0

        x2 = x*x
        y2 = y*y
        #z[n+1] <= z[n]^2 +Re(c) + Im(c)*z[n-1]
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

        return {'count': count, 'x': x, 'y': y}