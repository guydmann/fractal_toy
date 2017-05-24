from iterative_fractal import IterativeFractal

__author__ = 'guydmann'


class BurningShip(IterativeFractal):
    fractal_name = "burning_ship"
    breakout = 8
    width = 400
    height = 300
    viewport = {'left_x': -2.5,
                'right_x': 1.5,
                'top_y': -2.0,
                'bottom_y': 1.0}

    def dwell_cell(self, cx, cy):
        x = cx
        y = cy
        x2 = x * x
        y2 = y * y
        count = 0
        for count in range(self.max_iter):
            if (x2 + y2) > self.breakout:
                break
            y = (2.0 * abs(x * y)) + cy
            x = x2 - y2 + cx
            x2 = x * x
            y2 = y * y
        return count