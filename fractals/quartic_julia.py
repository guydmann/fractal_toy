from julia import Julia

__author__ = 'guydmann'


class QuarticJulia(Julia):
    fractal_name = "quartic_julia"
    breakout = 128

    def __init__(self):
        super(Julia, self).__init__()

    def dwell(self, cx, cy):
        x = cx
        y = cy
        x2 = x * x
        y2 = y * y
        # z <= z(n-1)^3 +c
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
        return {'count': count, 'x': x, 'y': y}