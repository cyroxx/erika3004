import sys

from PIL import Image


class NotAnImageException(Exception):
    pass


class WrappedImage:

    def __init__(self, image_path, threshold=128):
        """
        :param image_path: path to image that should be opened
        :param threshold: threshold value - pixel is considered "set" if there is a grayscale-equivalent value
        at this coordinate that is greater or equal to the given threshold
        """
        try:
            self.image = Image.open(image_path)
        except FileNotFoundError:
            raise FileNotFoundError("Exception when opening the file {} - file not found".format(image_path)) \
                .with_traceback(sys.exc_info()[2])
        except OSError:
            # OSError - OS-specific! Results may vary among different operating systems
            raise NotAnImageException("Exception when opening the file {} - maybe not an image?".format(image_path)) \
                .with_traceback(sys.exc_info()[2])

        self.pixels = self.image.load()
        self.threshold = threshold

    def is_grayscale(self):
        return self.image.mode == 'L'

    def is_rgb(self):
        return self.image.mode == 'RGB' or self.image.mode == 'RGBA'

    def is_pixel_set(self, x, y):
        if self.is_grayscale():
            return self.pixels[x, y] >= self.threshold
        elif self.is_rgb():
            pixel = self.pixels[x, y]
            grayscale_value = (pixel[0] + pixel[1] + pixel[2]) // 3
            return grayscale_value >= self.threshold
        else:
            raise Exception("Image type not supported")

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
        for y in range(0, num_pixels_y_axis):
            for x in range(0, num_pixels_x_axis):
                pixel = self.pixels[x, y]
                print(str(pixel).zfill(3), end=", ")
            print()

    def _print_rgb_image_for_debugging(self):
        num_pixels_x_axis = self.image.width
        num_pixels_y_axis = self.image.height
        for y in range(0, num_pixels_y_axis):
            for x in range(0, num_pixels_x_axis):
                pixel = self.pixels[x, y]
                # calculate a grayscale value + print to system out
                grayscale_value = (pixel[0] + pixel[1] + pixel[2]) // 3
                print(str(grayscale_value).zfill(3), end=", ")
            print()
