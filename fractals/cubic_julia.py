from julia import Julia

__author__ = 'guydmann'


class CubicJulia(Julia):
    fractal_name = "cubic_julia"
    breakout = 8

    def __init__(self):
        super(Julia, self).__init__()

    def dwell(self, cx, cy):
        x = cx
        y = cy

        a3 = -3 * (cx * cx - cy * cy)
        b3 = -3 * (2 * cx * cy)

        x2 = x * x
        y2 = y * y
        #z <= z(n-1)^3 +c
        count = 0
        for count in range(self.max_iter):
            if (x2 + y2) > self.breakout:
                break
            xsqr = x2 - y2 + a3
            ysqr = 2.0 * (y * x) + b3

            tmp = (xsqr * x) - (ysqr * y)
            y = (xsqr * y) + (ysqr * x)
            x = tmp

            x += self.cr
            y += self.ci

            x2 = x * x
            y2 = y * y
        return {'count': count, 'x': x, 'y': y}