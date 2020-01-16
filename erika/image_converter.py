class NotAnImageException(Exception):
    pass


class WrappedImage:
    def __init__(self, image_path, threshold=128):
        """
        :param image_path: path to image that should be opened
        :param threshold: threshold value - pixel is considered "set" if there is a grayscale-equivalent value
        at this coordinate that is greater or equal to the given threshold
        """
        import sys
        from PIL import Image

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
            return self.pixels[x, y] <= self.threshold
        elif self.is_rgb():
            pixel = self.pixels[x, y]
            grayscale_value = (pixel[0] + pixel[1] + pixel[2]) // 3
            return grayscale_value <= self.threshold
        else:
            raise Exception("Image type not supported")

    def width(self):
        return self.image.width

    def height(self):
        return self.image.height

    def __exit__(self, *args):
        self.image.close()
