from color import Color

class Simple(Color):
    def color_pixel(self, pixel_data):
        self.verify_data()

        color = (0, 0, 0)
        if pixel_data < self.precision*.03:
            color = (255, 0, 0, 255)
        elif pixel_data < self.precision*.05:
            color = (255, 255, 0, 255)
        elif pixel_data < self.precision*.1:
            color = (0, 255, 0, 255)
        elif pixel_data < self.precision*.2:
            color = (0, 255, 255, 255)
        elif pixel_data < self.precision:
            color = (0, 0, 255, 255)
        return color