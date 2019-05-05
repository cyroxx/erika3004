from enum import Enum
from erika.erika import Erika
from erika.erika_image_renderer import *
from argparse import ArgumentParser
# from argparse import RawTextHelpFormatter
# from argparse import RawDescriptionHelpFormatter

class ErikaCommands(Enum):
    render_ascii_art_file = 1

class ErikaRenderingStrategies(Enum):
    LineByLine = 1
    Interlaced = 2
    PerpendicularSpiralInward = 3
    RandomDotFill = 4
    ArchimedeanSpiralOutward = 5

# TODO support using piped input https://docs.python.org/3/library/fileinput.html

parser = ArgumentParser(prog='erika.sh')
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

# TODO wire up with the actual code
print ('### DEBUG: Args[{}]'.format(args))
