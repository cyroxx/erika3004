# Demonstrate painting of an Archimedean spiral using Tkinter.
#
# Copied and modified from:
# https://rosettacode.org/wiki/Archimedean_spiral#Python
#
# License of original:
# GNU Free Documentation License 1.2
# http://www.gnu.org/licenses/fdl-1.2.html

import math
import turtle
from enum import Enum

class Direction(Enum):
    NORTHEAST = 1
    NORTHWEST= 2
    SOUTHEAST = 3
    SOUTHWEST = 4

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
SPIRAL_STEP_SIZE = 1 / 20 * math.pi

# outer boundaries; cut off rendering if these are reached
# default canvas size is about 600 x 500, but (0, 0) is in the middle of the window
MAX_VALUE_X = 400
MAX_VALUE_Y = 400

TOLERANCE = 5

######################################################

def note_if_out_of_bounds(directions_out_of_bounds, direction):
    if (x > MAX_VALUE_X) or (y > MAX_VALUE_Y) or (x < -1 * MAX_VALUE_X) or (y < -1 * MAX_VALUE_Y):
        directions_out_of_bounds[direction] = 1
        turtle.write("({:.2f}, {:.2f}) - {:.2f}°".format(x, y, current_angle))


# in color blue...
turtle.color("blue")

# ... start painting ...
turtle.down()

# ... fast
# turtle.delay(1)
turtle.delay(0)

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

# cos ^ -1 = acos

i = 1
directions_out_of_bounds = {}
while True:
    t = i * SPIRAL_STEP_SIZE

    x = (SPIRAL_PARAM_A + SPIRAL_PARAM_B * t) * math.cos(t)
    y = (SPIRAL_PARAM_A + SPIRAL_PARAM_B * t) * math.sin(t)

    # easy cut-off: cut off if x OR y reach the outer boundary
    # if (x > MAX_VALUE_X) or (y > MAX_VALUE_Y):
    #     break

    # better cut off: cut off if turtle is in the corner (close to 45 degree angle in all directions) + out of bounds
    current_angle = (math.degrees(t) % 360)
    if ((45 - TOLERANCE <= current_angle) and (current_angle <= 45 + TOLERANCE)):
        note_if_out_of_bounds(directions_out_of_bounds, Direction.NORTHEAST)
    if ((135 - TOLERANCE <= current_angle) and (current_angle <= 135 + TOLERANCE)):
        note_if_out_of_bounds(directions_out_of_bounds, Direction.NORTHWEST)
    if ((225 - TOLERANCE <= current_angle) and (current_angle <= 225 + TOLERANCE)):
        note_if_out_of_bounds(directions_out_of_bounds, Direction.SOUTHEAST)
    if ((315 - TOLERANCE <= current_angle) and (current_angle <= 315 + TOLERANCE)):
        note_if_out_of_bounds(directions_out_of_bounds, Direction.SOUTHWEST)

    if len(directions_out_of_bounds) > 3:
        turtle.write("({:.2f}, {:.2f})".format(x, y))
        break

    # move to calculated next point
    turtle.goto(x, y)
    i += 1

# stop painting
turtle.up()

# end
turtle.done()
