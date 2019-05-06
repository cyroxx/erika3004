from argparse import ArgumentParser
from argparse import RawTextHelpFormatter

from erika.erika import Erika
from erika.erika_image_renderer import *
from erika.erika_mock import *


def create_argument_parser():
    # TODO support using piped input https://docs.python.org/3/library/fileinput.html

    parser = ArgumentParser(prog='erika.sh')
    command_parser = parser.add_subparsers(help='Available commands')
    render_ascii_art_file_parser = command_parser.add_parser('render_ascii_art_file',
                                                             formatter_class=RawTextHelpFormatter,
                                                             help='Rendering ASCII art in a specified pattern (rendering strategy)')
    render_ascii_art_file_parser.add_argument('--file', '-f', required=True, metavar='FILEPATH',
                                              help='File path to the file to print out, containing a pre-rendered ASCII art image.')
    render_ascii_art_file_parser.add_argument('--dry-run', '-d',
                                              action='store_true',
                                              help='If set, will print to standard out instead of connecting to Erika')
    render_ascii_art_file_parser.add_argument('--serial-port', '-p', required=True, metavar='SERIAL_PORT',
                                              help='Serial communications port for communicating with the Erika machine.')
    render_ascii_art_file_parser.add_argument('--strategy', '-s',
                                              choices=['LineByLine', 'Interlaced', 'PerpendicularSpiralInward',
                                                       'RandomDotFill', 'ArchimedeanSpiralOutward'],
                                              default='LineByLine',
                                              help="""Rendering strategy to apply. The value must be one of the following: 
    LineByLine 
        * render the given image line by line
        * default option
    Interlaced
        * render the given image, every even line first (starting count at 0), every odd line later
    PerpendicularSpiralInward ##
        * render the given image, spiralling inward to the middle while going parallel to X or Y axis all the time
    RandomDotFill
        * render the given image, printing one random letter at a time
    ArchimedeanSpiralOutward
        * render the given image, starting from the middle, following an Archimedean spiral as closely as possible""")
    return parser


def main():
    args = create_argument_parser().parse_args()

    if args.strategy == 'LineByLine':
        strategy = strategy = LineByLineErikaImageRenderingStrategy()
    elif args.strategy == 'Interlaced':
        strategy = InterlacedErikaImageRenderingStrategy()
    elif args.strategy == 'PerpendicularSpiralInward':
        strategy = PerpendicularSpiralInwardErikaImageRenderingStrategy()
    elif args.strategy == 'RandomDotFill':
        strategy = RandomDotFillErikaImageRenderingStrategy()
    elif args.strategy == 'ArchimedeanSpiralOutward':
        strategy = ArchimedeanSpiralOutwardErikaImageRenderingStrategy()

    if args.dry_run:
        erika = ErikaMock()
        renderer = ErikaImageRenderer(erika, strategy)
        renderer.render_ascii_art_file(args.file)
        erika.test_debug_helper_print_canvas()
    else:
        erika = Erika(args.com_port)
        renderer = ErikaImageRenderer(erika, strategy)
        renderer.render_ascii_art_file(args.file)


if __name__ == "__main__":
    main()
