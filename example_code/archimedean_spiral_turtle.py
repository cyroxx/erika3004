# Demonstrate painting of an Archimedean spiral using Tkinter.
#
# Copied and modified from:
# https://rosettacode.org/wiki/Archimedean_spiral#Python
#
# License of original:
# GNU Free Documentation License 1.2
# http://www.gnu.org/licenses/fdl-1.2.html

from turtle import delay, color, down, up, done, goto
from math import cos, sin, pi

######################################################
##################### PARAMETERS #####################
######################################################

# "...with real numbers a and b.
# Changing the parameter a turns the spiral,
# while b controls the distance between successive turnings."
# https://en.wikipedia.org/wiki/Archimedean_spiral
SPIRAL_PARAM_A = 1
SPIRAL_PARAM_B = 5

# round spiral:
# 1 / 20 * pi
# 1 / 10
#
# jagged spiral:
# 1
SPIRAL_STEP_SIZE = 1 / 20 * pi

######################################################

# in color blue...
color("blue")

# ... start painting ...
down()

# ... fast
delay(1)

# Formula for Archimedean spiral:
# https://en.wikipedia.org/wiki/Archimedean_spiral
# r = a + b * phi
# (with phi replaced later by t = 0, 1, ...)

# from polar coordinates to cartesian coordinates:
# x = r * cos(phi)
# y = r * sin(phi)

# follows:
# r = x / cos(phi)
# x / cos(phi) = a + b * phi
# x = (a + b * phi) * cos(phi)


# r = y / sin(phi)
# y / sin(phi) = a + b * phi
# y = (a + b * phi) * sin(phi)


for i in range(800):
    t = i * SPIRAL_STEP_SIZE

    x = (SPIRAL_PARAM_A + SPIRAL_PARAM_B * t) * cos(t)
    y = (SPIRAL_PARAM_A + SPIRAL_PARAM_B * t) * sin(t)

    # move to calculated next point
    goto(x, y)

# stop painting
up()

# end
done()
