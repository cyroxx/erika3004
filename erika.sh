#!/usr/bin/env bash

# Forward all to Python Command Line Interface
# e.g.
#
# * help output:
# ./erika.sh -h
# ./erika.sh render_ascii_art_file -h
#
# * demo output
# ./erika.sh demo -p "COM3"
# ./erika.sh demo -p "/dev/ttyACM0"
#
# * simulation + "on-screen cinematics"
# ./erika.sh render_ascii_art_file -d -f ./tests/test_resources/test_ascii_art.txt -s PerpendicularSpiralInward -p 'fake_port'
# ./erika.sh render_ascii_art_file -d -f ./tests/test_resources/test_ascii_art.txt -s ArchimedeanSpiralOutward  -p 'fake_port'
# ./erika.sh render_ascii_art_file -d -f ./tests/test_resources/test_ascii_art.txt -s RandomDotFill  -p 'fake_port'
#
# * real output
# ./erika.sh render_ascii_art_file -p "COM3" -f ./tests/test_resources/test_ascii_art_small.txt
# ./erika.sh render_ascii_art_file -p "/dev/ttyACM0" -f ./tests/test_resources/test_ascii_art_small.txt -s PerpendicularSpiralInward
python3 -m erika.cli $@