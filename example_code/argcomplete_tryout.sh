#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
# ^ is about https://argcomplete.readthedocs.io/en/latest/#global-completion

import argcomplete, argparse

def print_stuff(parsed_args, arg):
    print("print_stuff called with argument '{}' for these args:\n{}".format(arg, parsed_args))


parser = argparse.ArgumentParser(prog='argcomplete_tryout.sh', description='Command line autocompletion test - ### MAKE SURE YOU CALL activate_argcomplete_tryout_sh_autocomplete.sh FIRST! ###')
command_parser = parser.add_subparsers(help='Available commands')

subparser_1 = command_parser.add_parser('option_1', help='Option 1')
subparser_1.set_defaults(func=print_stuff, arg="option 1 called")
subparser_1.add_argument('--flag', '-f',
                         action='store_true',
                         help='If set, will set a boolean flag')
subparser_1.add_argument('--string-argument', '-s', metavar='STRING_INPUT',
                         help='Some string parameter')

subparser_2 = command_parser.add_parser('option_2', help='Option 2')
subparser_2.set_defaults(func=print_stuff, arg="option 2 called")
subparser_2.add_argument('--flag2', '-f2',
                         action='store_true',
                         help='If set, will set a boolean flag')
subparser_2.add_argument('--string-argument2', '-s2', metavar='STRING_INPUT',
                         help='Some string parameter')

subparser_3 = command_parser.add_parser('third_option', help='Option 3')
subparser_3.set_defaults(func=print_stuff, arg="option 3 called")

subparser_3.add_argument('--flag3', '-f3',
                         action='store_true',
                         help='If set, will set a boolean flag')
subparser_3.add_argument('--string-argument3', '-s3', metavar='STRING_INPUT',
                         help='Some string parameter')
argcomplete.autocomplete(parser)

args = parser.parse_args()

if ('func' in args):
    args.func(args, args.arg)
else:
    argument_parser.parse_args('-h')
