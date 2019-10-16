from erika.image_converter import WrappedImage


def main():
    root_path = 'tests/test_resources/'
    WrappedImage(root_path + 'test_image_monochrome_1.bmp')._print_image_at_path_for_debugging()
    print()
    WrappedImage(root_path + 'test_image_monochrome_2.bmp')._print_image_at_path_for_debugging()
    print()
    WrappedImage(root_path + 'test_image_grayscale_1.bmp')._print_image_at_path_for_debugging()
    print()
    WrappedImage(root_path + 'test_image_grayscale_2.bmp')._print_image_at_path_for_debugging()
    print()
    WrappedImage(root_path + 'test_image_color.bmp')._print_image_at_path_for_debugging()


if __name__ == "__main__":
    main()
