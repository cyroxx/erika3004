from PIL import Image


class WrappedImage:

    def __init__(self, image_path):
        self.image = Image.open(image_path)

    def is_grayscale(self):
        return self.image.mode == 'L'

    def is_rgb(self):
        return self.image.mode == 'RGB'

    def __exit__(self, *args):
        self.image.close()

    def _print_image_at_path_for_debugging(self):
        if self.is_grayscale():
            self._print_grayscale_image_for_debugging()
        elif self.is_rgb():
            self._print_rgb_image_for_debugging()
        else:
            raise Exception("Image type not supported")

    def _print_grayscale_image_for_debugging(self):
        num_pixels_x_axis = self.image.width
        num_pixels_y_axis = self.image.height
        pixels = self.image.load()
        for y in range(0, num_pixels_y_axis):
            for x in range(0, num_pixels_x_axis):
                pixel = pixels[x, y]
                print(str(pixel).zfill(3), end=", ")
            print()

    def _print_rgb_image_for_debugging(self):
        num_pixels_x_axis = self.image.width
        num_pixels_y_axis = self.image.height
        pixels = self.image.load()
        for y in range(0, num_pixels_y_axis):
            for x in range(0, num_pixels_x_axis):
                pixel = pixels[x, y]
                # calculate a grayscale value + print to system out
                grayscale_value = pixel[0] + pixel[1] + pixel[2]
                print(str(grayscale_value).zfill(3), end=", ")
            print()
