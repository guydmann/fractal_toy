from iterative_fractal import IterativeFractal

__author__ = 'guydmann'


class Star(IterativeFractal):
    fractal_name = "star"
    breakout = 0.00001
    px = .289
    py = .928

    def dwell_cell(self, cx, cy):

        absv = 1.0
        x = cx
        y = cy
        count = 0
        for count in range(self.max_iter):
            if absv <= self.breakout:
                break
            oldx = x
            oldy = y
            notx = 0.0
            noty = 0.0

            if -1 < oldx < 1:
                notx = 1.0
            if -1 < oldy < 1:
                noty = 1.0

            x = (self.px*notx*oldx) - (self.px*noty*oldy) - (self.py*noty*oldx) - (self.py*notx*oldy)
            y = (self.px*noty*oldx) + (self.px*notx*oldy) + (self.py*notx*oldx) - (self.py*noty*oldy)
            absv = (oldx-x)*(oldx-x)+(oldy-y)*(oldy-y)

        if absv > self.breakout:
            count = self.precision
        return count