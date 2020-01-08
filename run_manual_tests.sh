#!/usr/bin/env bash

###########################################################################################################
####################################### Codified manual tests #############################################
###########################################################################################################
#
# It showed over time that the mock-based tests are not perfect, and some characteristics of python make it
# difficult to test every line of code and be 100% sure about not breaking existing code.
#
# Thus, here's the attempt to provide a set of simple tests, to be run as a bash script, to help a reviewer
# perform at least some checks on the software.

# fail on error
set -e


echo """
###########################################
### Erika 3004 tool suite: manual tests ###
###########################################

Please do run the unit tests first!

Then, just play along: press any key once the
program seems to stop, finish any games that
come up.

Afterward, you can be fairly sure everything
is still working!
"

./erika.sh -h

./erika.sh demo -h
./erika.sh demo -d

./erika.sh render_ascii_art -h
./erika.sh render_ascii_art -d -f ./tests/test_resources/test_ascii_art.txt
./erika.sh render_ascii_art -d -f ./tests/test_resources/test_ascii_art.txt -s LineByLine
./erika.sh render_ascii_art -d -f ./tests/test_resources/test_ascii_art.txt -s Interlaced
./erika.sh render_ascii_art -d -f ./tests/test_resources/test_ascii_art.txt -s RandomDotFill
./erika.sh render_ascii_art -d -f ./tests/test_resources/test_ascii_art.txt -s PerpendicularSpiralInward
./erika.sh render_ascii_art -d -f ./tests/test_resources/test_ascii_art.txt -s ArchimedeanSpiralOutward

./erika.sh tictactoe -d

echo """
##############################
### Successful manual test ###
##############################"