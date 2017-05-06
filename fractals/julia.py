from iterative_fractal import IterativeFractal

__author__ = 'guydmann'


class Julia(IterativeFractal):
    fractal_name = "julia"
    constants_required = True
    breakout = 8
    cr = 0
    ci = 0

    def dwell(self, cx, cy):
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
        return {'count': count, 'x': x, 'y': y}