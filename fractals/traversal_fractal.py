from progressbar import ProgressBar
from fractals.fractal import Fractal
from PIL import Image

__author__ = 'guydmann'


class TraversalFractal(Fractal):
    iterative_algorithm = False

    def render(self):
        if not self.preprocessed:
            self.preprocess()

        if self.show_progress_bar:
            calc_cols_pbar = ProgressBar(maxval=self.width)
            color_pbar = ProgressBar(maxval=self.width)

        if not self.fractal_data_generated:
            if self.show_progress_bar:
                calc_cols_pbar.start()
            if self.verbose:
                print("Calculating Fractal")
            for cx in range(self.width):
                for cy in range(self.height):
                    self.dwell_cell((cx*self.x_inc)+self.viewport['left_x'], self.viewport['top_y']-(cy*self.y_inc))
                if self.show_progress_bar:
                    calc_cols_pbar.update(cx+1)
            if self.show_progress_bar:
                calc_cols_pbar.finish()
            self.set_fractal_data_generated(True)

        if not self.bypass_image_generation:
            img = Image.new('RGBA', (self.width, self.height))
            if self.show_progress_bar:
                color_pbar.start()
            if self.verbose:
                print("Coloring Fractal")
            for cx in range(self.width):
                for cy in range(self.height):
                    img.putpixel((cx, cy), self.color(self.fractal_array[cx][cy]))
                if self.show_progress_bar:
                    color_pbar.update(cx+1)
            if self.show_progress_bar:
                color_pbar.finish()
            filename_with_extension = '{}.png'.format(self.filename)
            img.save(filename_with_extension, 'PNG')
            self.apply_post_rendering_image_filters()
            return filename_with_extension
        else:
            return True
