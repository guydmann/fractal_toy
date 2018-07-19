from fractals.fractal import Fractal
from PIL import Image
import numpy as np


class IterativeFractal(Fractal):
    iterative_algorithm = True

    def render(self):
        if not self.preprocessed:
            self.preprocess()

        if not self.fractal_data_generated:
            print("Calculating Fractal")
            self.fractal_array = self.dwell()
            self.set_fractal_data_generated(True)

        if not self.bypass_image_generation:
            img = Image.new('RGBA', (self.width, self.height))
            print("Coloring Fractal")
            uniques, indices = np.unique(self.fractal_array, return_inverse=True)
            precomputed_colors = dict([(unique, self.color(unique)) for unique in uniques])
            for cx in range(self.width):
                for cy in range(self.height):
                    img.putpixel((cx, cy), precomputed_colors[self.fractal_array[cx][cy]])
            img.save('{}.png'.format(self.filename), 'PNG')
            return '{}.png'.format(self.filename)
        else:
            return True
