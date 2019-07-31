from PIL import Image


def print_image_at_path_for_debugging(image_path):
    image = Image.open(image_path)

    if is_image_grayscale(image):
        print_grayscale_image_for_debugging(image)
    elif is_image_rgb(image):
        print_rgb_image_for_debugging(image)
    else:
        raise Exception("Image type not supported")


def is_image_grayscale(image):
    return image.mode == 'L'


def print_grayscale_image_for_debugging(image):
    num_pixels_x_axis = image.width
    num_pixels_y_axis = image.height
    pixels = image.load()
    for y in range(0, num_pixels_y_axis):
        for x in range(0, num_pixels_x_axis):
            pixel = pixels[x, y]
            print(str(pixel).zfill(3), end=", ")
        print()


def is_image_rgb(image):
    return image.mode == 'RGB'


def print_rgb_image_for_debugging(image):
    num_pixels_x_axis = image.width
    num_pixels_y_axis = image.height
    pixels = image.load()
    for y in range(0, num_pixels_y_axis):
        for x in range(0, num_pixels_x_axis):
            pixel = pixels[x, y]
            # calculate a grayscale value + print to system out
            grayscale_value = pixel[0] + pixel[1] + pixel[2]
            print(str(grayscale_value).zfill(3), end=", ")
        print()


def main():
    root_path = '../tests/test_resources/'
    print_image_at_path_for_debugging(root_path + 'test_image_monochrome_1.bmp')
    print()
    print_image_at_path_for_debugging(root_path + 'test_image_monochrome_2.bmp')
    print()
    print_image_at_path_for_debugging(root_path + 'test_image_grayscale_1.bmp')
    print()
    print_image_at_path_for_debugging(root_path + 'test_image_grayscale_2.bmp')
    print()
    print_image_at_path_for_debugging(root_path + 'test_image_color.bmp')

if __name__ == "__main__":
    main()
