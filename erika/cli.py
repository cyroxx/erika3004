from argparse import ArgumentParser

from erika.erika import Erika
from erika.erika_image_renderer import *
from erika.erika_mock import *

# from argparse import RawTextHelpFormatter
# from argparse import RawDescriptionHelpFormatter

# TODO support using piped input https://docs.python.org/3/library/fileinput.html

parser = ArgumentParser(prog='erika.sh')
# TODO rendering of rendering strategy options is still broken, this tip does not help:
#       https://stackoverflow.com/questions/3853722/python-argparse-how-to-insert-newline-in-the-help-text
# parser = ArgumentParser(prog='erika.sh', formatter_class=RawTextHelpFormatter)
# parser = ArgumentParser(prog='erika.sh', formatter_class=RawDescriptionHelpFormatter)
command_parser = parser.add_subparsers(help='Available commands')
render_ascii_art_file_parser = command_parser.add_parser('render_ascii_art_file',
                                                         help='Rendering ASCII art in a specified pattern (rendering strategy)')
render_ascii_art_file_parser.add_argument('--file', '-f', required=True, metavar='FILEPATH',
                                          help='File path to the file to print out, containing a pre-rendered ASCII art image.')
render_ascii_art_file_parser.add_argument('--dry-run', '-d',
                                          action='store_true',
                                          help='If set, will print to standard out instead of connecting to Erika')

render_ascii_art_file_parser.add_argument('--strategy', '-s',
                                          choices=['LineByLine', 'Interlaced', 'PerpendicularSpiralInward',
                                                   'RandomDotFill', 'ArchimedeanSpiralOutward'],
                                          default='LineByLine',
                                          # metavar='STRAT',
                                          help="""Rendering strategy to apply. The value must be one of the following: 
                ## LineByLine ##
                    * render the given image line by line
                    * default option
                ## Interlaced ##
                    * render the given image, every even line first (starting count at 0), every odd line later
                ## PerpendicularSpiralInward ##
                    * render the given image, spiralling inward to the middle while going parallel to X or Y axis all the time
                ## RandomDotFill ##
                    * render the given image, printing one random letter at a time
                ## ArchimedeanSpiralOutward ##
                    * render the given image, starting from the middle, following an Archimedean spiral as closely as possible""")
args = parser.parse_args()

# print('### DEBUG: Args[{}]'.format(args))
# print('dry_run: {}'.format(args.dry_run))
# print('strategy: {}'.format(args.strategy))
# print('file: {}'.format(args.file))


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
    erika = Erika()
    renderer = ErikaImageRenderer(erika, strategy)
    renderer.render_ascii_art_file(args.file)
