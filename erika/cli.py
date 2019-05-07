from argparse import ArgumentParser
from argparse import RawTextHelpFormatter

from erika.erika import Erika
from erika.erika_image_renderer import *
from erika.erika_mock import *


def create_argument_parser():
    parser = ArgumentParser(prog='erika.sh')
    command_parser = parser.add_subparsers(help='Available commands')
    add_render_ascii_art_parser(command_parser)
    return parser


# TODO support using piped input https://docs.python.org/3/library/fileinput.html
def add_render_ascii_art_parser(command_parser):
    render_ascii_art_file_parser = command_parser.add_parser('render_ascii_art_file',
                                                             formatter_class=RawTextHelpFormatter,
                                                             help='Rendering ASCII art in a specified pattern (rendering strategy)')
    render_ascii_art_file_parser.set_defaults(func=print_ascii_art)
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


def print_ascii_art(args):
    startegy_string = args.strategy
    is_dry_run = args.dry_run
    file_path = args.file
    com_port = args.serial_port

    if startegy_string == 'LineByLine':
        strategy = strategy = LineByLineErikaImageRenderingStrategy()
    elif startegy_string == 'Interlaced':
        strategy = InterlacedErikaImageRenderingStrategy()
    elif startegy_string == 'PerpendicularSpiralInward':
        strategy = PerpendicularSpiralInwardErikaImageRenderingStrategy()
    elif startegy_string == 'RandomDotFill':
        strategy = RandomDotFillErikaImageRenderingStrategy()
    elif startegy_string == 'ArchimedeanSpiralOutward':
        strategy = ArchimedeanSpiralOutwardErikaImageRenderingStrategy()

    if is_dry_run:
        # using 40x40 just so it fits on the screen well - does not reflect the paper dimensions that Erika supports
        erika = ErikaMock(40, 40, output_after_each_step=True, delay_after_each_step=0.2)

        # when rendering test_ascii_art.txt, use these settings instead:
        # erika = ErikaMock(60, 40, output_after_each_step=True, delay_after_each_step=0.05)
        renderer = ErikaImageRenderer(erika, strategy)
        renderer.render_ascii_art_file(file_path)
    else:
        erika = Erika(com_port)
        renderer = ErikaImageRenderer(erika, strategy)
        renderer.render_ascii_art_file(file_path)


def main():
    args = create_argument_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
