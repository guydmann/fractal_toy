from fractals.julia import Julia


class ExperimentalCubicJulia(Julia):
    fractal_name = "experimental_cubic_julia"
    breakout = 8

    def __init__(self):
        super(Julia, self).__init__()

    def dwell_cell(self, cx, cy):
        x = cx
        y = cy

        a3 = -3 * (cx * cx - cy * cy)
        b3 = -3 * (2 * cx * cy)

        x2 = x * x
        y2 = y * y
        # z <= z(n-1)^3 +c
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
        count1 = count

        x = -1*cx
        y = -1*cy

        a3 = -3 * (cx * cx - cy * cy)
        b3 = -3 * (2 * cx * cy)

        x2 = x * x
        y2 = y * y
        # z <= z(n-1)^3 +c
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

        count2 = count
        if count1 == count2:
            count = self.max_iter
        elif count1 < count2:
            count = count1
        else:
            count = count2

        return count
