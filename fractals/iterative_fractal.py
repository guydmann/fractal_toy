from fractal import Fractal
from progressbar import ProgressBar
from PIL import Image

__author__ = 'guydmann'


class IterativeFractal(Fractal):
    iterative_algorithm = True

    def render(self):
        if not self.preprocessed:
            self.preprocess()

        if self.show_progress_bar:
            pbar = ProgressBar(maxval=self.width)

        if not self.fractal_data_generated:
            if self.show_progress_bar:
                pbar.start()
            print "Calculating Fractal"
            for cx in range(self.width):
                for cy in range(self.height):
                    self.fractal_array[cx][cy]['count'] = \
                        self.dwell ((cx*self.x_inc)+self.viewport['left_x'], self.viewport['top_y']-(cy*self.y_inc))
                    self.fractal_array[cx][cy]['x'] = (cx*self.x_inc)+self.viewport['left_x']
                    self.fractal_array[cx][cy]['y'] = self.viewport['top_y']-(cy*self.y_inc)
                if self.show_progress_bar:
                    pbar.update(cx+1)
            if self.show_progress_bar:
                pbar.finish()
            self.set_fractal_data_generated(True)

        if not self.bypass_image_generation:
            img = Image.new('RGBA', (self.width, self.height))
            if self.show_progress_bar:
                pbar.start()
            print "Coloring Fractal"
            for cx in range(self.width):
                for cy in range(self.height):
                    img.putpixel((cx, cy), self.color(self.fractal_array[cx][cy]['count']))
                if self.show_progress_bar:
                    pbar.update(cx+1)
            if self.show_progress_bar:
                pbar.finish()
            img.save('{}.png'.format(self.filename), 'PNG')
            return '{}.png'.format(self.filename)
        else:
            return True
