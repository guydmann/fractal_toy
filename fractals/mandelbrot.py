from iterative_fractal import IterativeFractal

__author__ = 'guydmann'


class Mandelbrot(IterativeFractal):
    fractal_name = "mandelbrot"
    breakout = 4
    viewport = {'left_x': -1.5,
                'right_x': 0.5,
                'top_y': 1.0,
                'bottom_y': -1.0}

    def dwell(self, cx, cy):
        # equation
        # z <= z(n-1)^2 +c
        x = cx
        y = cy
        x2 = x * x
        y2 = y * y

        count = 0
        for count in range(self.max_iter):
            if (x2 + y2) > self.breakout:
                break
            y = (2 * (x * y)) + cy
            x = x2 - y2 + cx
            x2 = x * x
            y2 = y * y
        return {'count': count, 'x': x, 'y': y}