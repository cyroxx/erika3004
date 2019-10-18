from erika.image_converter import WrappedImage


def main():
    root_path = 'tests/test_resources/'
    _print_image_at_path_for_debugging(WrappedImage(root_path + 'test_image_monochrome_1.bmp'))
    print()
    _print_image_at_path_for_debugging(WrappedImage(root_path + 'test_image_monochrome_2.bmp'))
    print()
    _print_image_at_path_for_debugging(WrappedImage(root_path + 'test_image_grayscale_1.bmp'))
    print()
    _print_image_at_path_for_debugging(WrappedImage(root_path + 'test_image_grayscale_2.bmp'))
    print()
    _print_image_at_path_for_debugging(WrappedImage(root_path + 'test_image_color.bmp'))


def _print_image_at_path_for_debugging(wrapped_image):
    if wrapped_image.is_grayscale():
        _print_grayscale_image_for_debugging(wrapped_image)
    elif wrapped_image.is_rgb():
        _print_rgb_image_for_debugging(wrapped_image)
    else:
        raise Exception("Image type not supported")


def _print_grayscale_image_for_debugging(wrapped_image):
    num_pixels_x_axis = wrapped_image.image.width
    num_pixels_y_axis = wrapped_image.image.height
    for y in range(0, num_pixels_y_axis):
        for x in range(0, num_pixels_x_axis):
            pixel = wrapped_image.pixels[x, y]
            print(str(pixel).zfill(3), end=", ")
        print()


def _print_rgb_image_for_debugging(wrapped_image):
    num_pixels_x_axis = wrapped_image.image.width
    num_pixels_y_axis = wrapped_image.image.height
    for y in range(0, num_pixels_y_axis):
        for x in range(0, num_pixels_x_axis):
            pixel = wrapped_image.pixels[x, y]
            # calculate a grayscale value + print to system out
            grayscale_value = (pixel[0] + pixel[1] + pixel[2]) // 3
            print(str(grayscale_value).zfill(3), end=", ")
        print()


if __name__ == "__main__":
    main()
