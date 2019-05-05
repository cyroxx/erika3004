#!/usr/bin/env bash

# Forward all to Python Command Line Interface
# e.g. call
# ./erika.sh -h
# ./erika.sh render_ascii_art_file -h
# ./erika.sh render_ascii_art_file -d -f ./tests/test_resources/test_ascii_art_small.txt -s PerpendicularSpiralInward
# ./erika.sh render_ascii_art_file -f ./tests/test_resources/test_ascii_art_small.txt -s PerpendicularSpiralInward
python3 -m erika.cli $@