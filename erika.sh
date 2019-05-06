#!/usr/bin/env bash

# Forward all to Python Command Line Interface
# e.g. call
# ./erika.sh -h
# ./erika.sh render_ascii_art_file -h
# ./erika.sh render_ascii_art_file -d -p "fake_port" -f ./tests/test_resources/test_ascii_art_small.txt -s PerpendicularSpiralInward
# ./erika.sh render_ascii_art_file -p "COM3" -f ./tests/test_resources/test_ascii_art_small.txt
# ./erika.sh render_ascii_art_file -p "/dev/ttyACM0" -f ./tests/test_resources/test_ascii_art_small.txt -s PerpendicularSpiralInward
python3 -m erika.cli $@