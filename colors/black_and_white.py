from color import Color

class BlackAndWhite(Color):
    def color_pixel(self, pixel_data):
        self.verify_data()

        color = (0, 0, 0)
        if pixel_data < self.precision:
            color = (255, 255, 255, 255)
        return color
