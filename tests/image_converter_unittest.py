import unittest

from erika.image_converter import *

root_path = 'tests/test_resources/'


# noinspection SpellCheckingInspection
class WrappedImageUnitTest(unittest.TestCase):

    def testBmpImageIsRecognizedAsGrayScale(self):
        """simple test that grayscale images are recognized as such"""
        image1 = WrappedImage(root_path + 'test_image_grayscale_1.bmp')
        self.assertTrue(image1.is_grayscale())
        self.assertFalse(image1.is_rgb())

        image2 = WrappedImage(root_path + 'test_image_grayscale_2.bmp')
        self.assertTrue(image2.is_grayscale())
        self.assertFalse(image2.is_rgb())

        image3 = WrappedImage(root_path + 'test_image_monochrome_1.bmp')
        self.assertTrue(image3.is_grayscale())
        self.assertFalse(image3.is_rgb())

        image4 = WrappedImage(root_path + 'test_image_monochrome_2.bmp')
        self.assertTrue(image4.is_grayscale())
        self.assertFalse(image4.is_rgb())

    def testBmpImageIsRecognizedAsRgb(self):
        """simple test that RGB color images are recognized as such"""
        image = WrappedImage(root_path + 'test_image_color.bmp')
        self.assertTrue(image.is_rgb())
        self.assertFalse(image.is_grayscale())

    def testPngImageIsRecognizedAsRgb(self):
        """simple test that RGB color images are recognized as such"""
        image = WrappedImage(root_path + 'ubuntu-logo32.png')
        self.assertTrue(image.is_rgb())
        self.assertFalse(image.is_grayscale())

    def testRenamedPngImageIsRecognizedAsRgb(self):
        """simple test that a renamed RGB image file is recognized as RGB image"""
        image = WrappedImage(root_path + 'ubuntu-logo32.png.renamedwithextension.txt')
        self.assertTrue(image.is_rgb())
        self.assertFalse(image.is_grayscale())

    def testIsPixelSetWorksForGrayScale(self):
        """simple test that the wrapper can correctly determine if a pixel is colored-in (grayscale image)"""
        image_white_first_pixel = WrappedImage(root_path + 'test_image_monochrome_1.bmp')
        self.assertTrue(image_white_first_pixel.is_pixel_set(0, 0))

        imageBlackFirstPixel = WrappedImage(root_path + 'test_image_grayscale_2.bmp')
        self.assertFalse(imageBlackFirstPixel.is_pixel_set(0, 0))

    def testAdjustableThresholdWorksForGrayScale(self):
        """simple test that the wrapper can correctly determine if a pixel is colored-in when the threshold is
        adjusted """
        image_gray_first_pixel = WrappedImage(root_path + 'test_image_grayscale_1.bmp')
        self.assertTrue(image_gray_first_pixel.is_pixel_set(0, 0))
        image_gray_first_pixel_higher_threshold = WrappedImage(root_path + 'test_image_grayscale_1.bmp', threshold=129)
        self.assertFalse(image_gray_first_pixel_higher_threshold.is_pixel_set(0, 0))

    def testIsPixelSetWorksForRgb(self):
        """simple test that the wrapper can correctly determine if a pixel is colored-in (RGB image)"""
        color_image = WrappedImage(root_path + 'test_image_color.bmp')
        self.assertTrue(color_image.is_pixel_set(0, 0))

        image_black_first_pixel = WrappedImage(root_path + 'ubuntu-logo32.png')
        self.assertFalse(image_black_first_pixel.is_pixel_set(0, 0))

    def testAdjustableThresholdWorksForRgb(self):
        """simple test that the wrapper can correctly determine if a pixel is colored-in when the threshold is
        adjusted """
        color_image = WrappedImage(root_path + 'test_image_color.bmp')
        self.assertTrue(color_image.is_pixel_set(0, 0))
        color_image_higher_threshold = WrappedImage(root_path + 'test_image_color.bmp', threshold=153)
        self.assertFalse(color_image_higher_threshold.is_pixel_set(0, 0))

    def testTextFileInput(self):
        """simple test how the wrapper behaves when given a text file (ASCII art)"""
        self.assertRaisesRegex(Exception, "Exception when opening the file - maybe not an image[?]",
                               load_text_file_as_wrapped_image)

    def testNonExistentFileInput(self):
        """simple test how the wrapper behaves when the file is not found"""
        self.assertRaisesRegex(Exception, "Exception when opening the file - file not found", load_non_existent_file)


def load_text_file_as_wrapped_image():
    WrappedImage(root_path + 'test_ascii_art.txt')


def load_non_existent_file():
    WrappedImage(root_path + 'nonexistent_file_for_test.xyz')


def main():
    unittest.main()


if __name__ == '__main__':
    main()
