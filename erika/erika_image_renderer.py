import math
import random
from enum import Enum

from erika.image_converter import WrappedImage, NotAnImageException


class Direction(Enum):
    NORTHEAST = 1
    NORTHWEST = 2
    SOUTHEAST = 3
    SOUTHWEST = 4


class ErikaImageRenderer:
    def __init__(self, some_erika, rendering_strategy):
        self._output_device = some_erika
        self.rendering_strategy = rendering_strategy
        self.rendering_strategy._set_output_device(some_erika)

    def render_ascii_art_file(self, file_path):
        self.rendering_strategy.render_ascii_art_file(file_path)

    def render_ascii_art_lines(self, lines):
        self.rendering_strategy.render_ascii_art_lines(lines)

    def set_strategy(self, new_strategy):
        self.rendering_strategy = new_strategy
        self.rendering_strategy._set_output_device(self._output_device)


class ErikaImageRenderingStrategy:

    def __init__(self):
        pass

    # noinspection PyAttributeOutsideInit
    def _set_output_device(self, some_erika):
        self._output_device = some_erika

    def render_ascii_art_file(self, file_path):
        lines = self._read_lines_without_trailing_newlines(file_path)
        self.render_ascii_art_lines(lines)

    def render_ascii_art_lines(self, lines):
        self.render_ascii_art_lines_internal(self._remove_trailing_newlines(lines))

    def render_ascii_art_lines_internal(self, lines):
        raise Exception('Not implemented')

    def _read_lines_without_trailing_newlines(self, file_path):
        lines = []
        with open(file_path, "r") as open_file:
            lines = open_file.readlines()
        return self._remove_trailing_newlines(lines)

    def _remove_trailing_newlines(self, lines):
        lines_without_newlines = []
        for line in lines:
            lines_without_newlines.append(self._remove_trailing_newline(line))
        return lines_without_newlines


    def _remove_trailing_newline(self, line):
        return line.replace('\n', "").replace('\r', "")

    def _calculate_max_line_length(self, lines):
        max_length = 0
        for line in lines:
            if len(line) > max_length:
                max_length = len(line)
        return max_length

    def _generate_coordinates(self, range_x_upper, range_y_upper, range_x_lower=0, range_y_lower=0):
        for x in range(range_x_lower, range_x_upper):
            for y in range(range_y_lower, range_y_upper):
                yield (x, y)

    def _initialize_printed_characters_map(self, lines, max_line_length, line_count):
        self._printed = []
        for y in range(line_count):
            new_row = []
            for x in range(max_line_length):
                new_row.append(False)
            self._printed.append(new_row)


class LineByLineErikaImageRenderingStrategy(ErikaImageRenderingStrategy):

    def __init__(self):
        ErikaImageRenderingStrategy.__init__(self)

    def render_ascii_art_lines_internal(self, lines):
        for line in lines:
            self._output_device.print_ascii(line)
            self._output_device.crlf()


class InterlacedErikaImageRenderingStrategy(ErikaImageRenderingStrategy):

    def __init__(self):
        ErikaImageRenderingStrategy.__init__(self)

    def render_ascii_art_lines_internal(self, lines):
        line_count = len(lines)
        moved = 0
        for even in range(0, line_count, 2):
            line = lines[even]
            self._output_device.print_ascii(line)
            self._output_device.crlf()
            self._output_device.crlf()
            moved += 2

        # reset cursor to start of line
        self._output_device.crlf()

        # do not compensate the line that this adds - the extra line will position the cursor right where we want it
        # self._output_device.move_up()

        for lines_to_move_up in range(0, moved):
            self._output_device.move_up()

        for odd in range(1, line_count, 2):
            line = lines[odd]
            self._output_device.print_ascii(line)
            self._output_device.crlf()
            self._output_device.crlf()


class PerpendicularSpiralInwardErikaImageRenderingStrategy(ErikaImageRenderingStrategy):

    def __init__(self):
        ErikaImageRenderingStrategy.__init__(self)

    def render_ascii_art_lines_internal(self, lines):
        line_count = len(lines)
        max_line_length = self._calculate_max_line_length(lines)
        self._print_spiral_recursively(lines, 0, 0, max_line_length - 1, line_count - 1)

    def _print_spiral_recursively(self, lines, upper_left_x, upper_left_y, lower_right_x, lower_right_y):
        """ASSUMPTION: current position is at (upper_left_x, upper_left_y)"""
        if upper_left_x > lower_right_x or upper_left_y > lower_right_y:
            return

        # render one round of the spiral, clockwise

        #
        # =====>
        #
        for x in range(upper_left_x, lower_right_x + 1):
            self._output_device.print_ascii(lines[upper_left_y][x])

        # edge case: this was the only last row
        if upper_left_y == lower_right_y:
            return

        # reset to last cursor position
        self._output_device.move_left()

        # go down - do not print a character twice
        self._output_device.move_down()

        # ||
        # ||
        # \/
        for y in range(upper_left_y + 1, lower_right_y):
            self._output_device.print_ascii(lines[y][lower_right_x])
            self._output_device.move_down()
            self._output_device.move_left()

        # special handling of last character - smoothen transition
        self._output_device.print_ascii(lines[lower_right_y][lower_right_x])

        # edge case: this was the only last column
        if upper_left_x == lower_right_x:
            return

        # back to last printed character
        self._output_device.move_left()
        self._output_device.move_left()

        #
        # <=====
        #
        for x in range(lower_right_x - 1, upper_left_x - 1, -1):
            self._output_device.print_ascii(lines[lower_right_y][x])
            self._output_device.move_left()
            self._output_device.move_left()

        self._output_device.move_right()
        self._output_device.move_up()

        # /\
        # ||
        # ||
        for y in range(lower_right_y - 1, upper_left_y + 1, -1):
            self._output_device.print_ascii(lines[y][upper_left_x])
            self._output_device.move_up()
            self._output_device.move_left()

        # special handling of last character - smoothen transition
        if lower_right_y - 1 >= upper_left_y + 1:
            self._output_device.print_ascii(lines[upper_left_y + 1][upper_left_x])

        # continue with smaller spiral - restart recursion
        self._print_spiral_recursively(lines, upper_left_x + 1, upper_left_y + 1, lower_right_x - 1, lower_right_y - 1)


class RandomDotFillErikaImageRenderingStrategy(ErikaImageRenderingStrategy):

    def __init__(self):
        ErikaImageRenderingStrategy.__init__(self)

    def render_ascii_art_lines_internal(self, lines):
        self.current_x = 0
        self.current_y = 0

        line_count = len(lines)
        max_line_length = self._calculate_max_line_length(lines)
        self._initialize_printed_characters_map(lines, max_line_length, line_count)
        self.render_random_dots_naive(line_count, max_line_length, lines)

    # naive approach: generate random position, render if not yet printed there
    # * this results in about 100 additional re-generation attempts for random numbers for the small test images
    # * improvement idea:
    # ** define a cut-off point (e.g. "if 100 letters left")
    # ** add remaining dots to a list + use random.choice(list) on those instead of continuing to guess blindly
    def render_random_dots_naive(self, line_count, max_line_length, lines):
        # once more, assuming a squere image
        number_of_characters = line_count * max_line_length

        for i in range(0, number_of_characters):
            # generate random position
            # look up if already printed - re-generate until empty space was found
            position_x, position_y = self._generate_random_position(max_line_length, line_count)
            while self._printed[position_y][position_x]:
                position_x, position_y = self._generate_random_position(max_line_length, line_count)

            # move there + print
            self._move_to(position_x, position_y)

            self._output_device.print_ascii(lines[position_y][position_x])
            self.current_x += 1
            self._printed[position_y][position_x] = True
            # repeat

    def _generate_random_position(self, exclusive_max_x, exclusive_max_y):
        random1 = random.randint(0, exclusive_max_x - 1)
        random2 = random.randint(0, exclusive_max_y - 1)
        return (random1, random2)

    def _move_to(self, position_x, position_y):
        # naive: adjust X position first, then Y position
        while self.current_x < position_x:
            self._output_device.move_right()
            self.current_x += 1

        while (position_x < self.current_x):
            self._output_device.move_left()
            self.current_x -= 1

        while self.current_y < position_y:
            self._output_device.move_down()
            self.current_y += 1

        while (position_y < self.current_y):
            self._output_device.move_up()
            self.current_y -= 1


class ArchimedeanSpiralOutwardErikaImageRenderingStrategy(ErikaImageRenderingStrategy):

    # TODO mention "This is a reST style." in commit message + link to https://stackoverflow.com/a/24385103/1143126
    def __init__(self, spiral_param_a=1, spiral_param_b=0.35, spiral_step_size=0.01, render_remaining_characters=True):
        """
        "...with real numbers a and b.

        Changing the parameter a turns the spiral,

        while b controls the distance between successive turnings."

        https://en.wikipedia.org/wiki/Archimedean_spiral

        :param spiral_param_a: turns the spiral
        :param spiral_param_b: controls distance between spiral turns
        :param spiral_step_size: step size between successive datapoints
        :param render_remaining_characters: if False, will only render the spiral, not fill remaining gaps later
        """
        ErikaImageRenderingStrategy.__init__(self)

        self.spiral_param_a = spiral_param_a
        self.spiral_param_b = spiral_param_b

        # round spiral:
        # 1 / 20 * pi
        # 1 / 10
        #
        # jagged spiral:
        # 1
        self.spiral_step_size = spiral_step_size

        # tolerance around 45° angle (in all directions) to mark as area for cut-off
        self.CUTOFF_ANGLE_TOLERANCE = 15

        self.render_remaining_characters = render_remaining_characters

    def render_ascii_art_lines_internal(self, lines):
        self.current_x = 0
        self.current_y = 0

        line_count = len(lines)
        max_line_length = self._calculate_max_line_length(lines)
        self._initialize_printed_characters_map(lines, max_line_length, line_count)

        self.render_spiral(lines, max_line_length, line_count)

        if (self.render_remaining_characters):
            self.render_remaining(lines, max_line_length, line_count)

        self._reset_to_upper_left()

    # Formula for Archimedean spiral:
    # https://en.wikipedia.org/wiki/Archimedean_spiral
    # r = a + b * phi
    # (with phi replaced later by t = 0, 1, ...)
    #
    # from polar coordinates to cartesian coordinates:
    # x = r * cos(phi)
    # y = r * sin(phi)
    #
    # follows:
    # r = x / cos(phi)
    # x / cos(phi) = a + b * phi
    # x = (a + b * phi) * cos(phi)
    #
    # r = y / sin(phi)
    # y / sin(phi) = a + b * phi
    # y = (a + b * phi) * sin(phi)
    #
    def render_spiral(self, lines, max_line_length, line_count):

        max_x = max_line_length - 1
        max_y = line_count - 1

        # print('max_x: {}, max_y: {}'.format(max_x, max_y))

        i = 1
        directions_out_of_bounds = {}
        self.spiral_offset_x = math.floor(max_x / 2)
        self.spiral_offset_y = math.floor(max_y / 2)
        self._move_to(self.spiral_offset_x, self.spiral_offset_y)
        while True:
            t = i * self.spiral_step_size

            x = (self.spiral_param_a + self.spiral_param_b * t) * math.cos(t) + self.spiral_offset_x
            y = (self.spiral_param_a + self.spiral_param_b * t) * math.sin(t) + self.spiral_offset_y

            # cut off: cut off if turtle is in the corner (close to 45 degree angle in all directions) + out of bounds
            current_angle = (math.degrees(t) % 360)
            if ((45 - self.CUTOFF_ANGLE_TOLERANCE <= current_angle) \
                    and (current_angle <= 45 + self.CUTOFF_ANGLE_TOLERANCE)):
                self._note_if_out_of_bounds(directions_out_of_bounds, Direction.NORTHEAST, max_x, max_y, x, y)
            if ((135 - self.CUTOFF_ANGLE_TOLERANCE <= current_angle) \
                    and (current_angle <= 135 + self.CUTOFF_ANGLE_TOLERANCE)):
                self._note_if_out_of_bounds(directions_out_of_bounds, Direction.NORTHWEST, max_x, max_y, x, y)
            if ((225 - self.CUTOFF_ANGLE_TOLERANCE <= current_angle) \
                    and (current_angle <= 225 + self.CUTOFF_ANGLE_TOLERANCE)):
                self._note_if_out_of_bounds(directions_out_of_bounds, Direction.SOUTHEAST, max_x, max_y, x, y)
            if ((315 - self.CUTOFF_ANGLE_TOLERANCE <= current_angle) \
                    and (current_angle <= 315 + self.CUTOFF_ANGLE_TOLERANCE)):
                self._note_if_out_of_bounds(directions_out_of_bounds, Direction.SOUTHWEST, max_x, max_y, x, y)

            # all 4 directions are out of bounds now
            if len(directions_out_of_bounds) > 3:
                break

            rounded_x = math.floor(x)
            rounded_y = math.floor(y)
            # move to calculated next point + print
            self._goto_and_print_if_in_bounds(lines, max_x, max_y, rounded_x, rounded_y)

            i += 1

    def _note_if_out_of_bounds(self, directions_out_of_bounds, direction, max_x, max_y, x, y):
        if (x < 0) or (y < 0) or (max_x < x) or (max_y < y):
            directions_out_of_bounds[direction] = 1

    def _goto_and_print_if_in_bounds(self, lines, max_x, max_y, x, y):
        if (x < 0) or (y < 0) or (max_x < x) or (max_y < y):
            return
        self._goto_and_print(lines, x, y)

    def _goto_and_print(self, lines, x, y):
        # print('goto_and_print_if_in_bounds(1) -- x: {}, y: {}, current_x: {}, current_y: {}'.format(x, y, self._current_x, self._current_y))
        if (self._printed[y][x]):
            return

        self._printed[y][x] = True
        self._move_to(x, y)
        # print('goto_and_print_if_in_bounds(2) -- x: {}, y: {}, current_x: {}, current_y: {}'.format(x, y, self._current_x, self._current_y))
        self._output_device.print_ascii(lines[y][x])
        self.current_x += 1

    # TODO dry
    def _move_to(self, position_x, position_y):
        # naive: adjust X position first, then Y position
        while self.current_x < position_x:
            self._output_device.move_right()
            self.current_x += 1

        while (position_x < self.current_x):
            self._output_device.move_left()
            self.current_x -= 1

        while self.current_y < position_y:
            self._output_device.move_down()
            self.current_y += 1

        while (position_y < self.current_y):
            self._output_device.move_up()
            self.current_y -= 1

    def render_remaining(self, lines, max_line_length, line_count):
        # print('### Render remaining letters ###')
        # render remaining letters in ascending order of distance to middle point
        found = True
        while found:
            found = False
            min_distance = float("inf")
            min_position_x = 0
            min_position_y = 0

            for x, y in self._generate_coordinates(max_line_length, line_count):
                is_printed = self._printed[y][x]
                is_new_min_distance = self._distance_to_spiral_center(x, y) < min_distance
                if is_new_min_distance and not is_printed:
                    found = True
                    min_position_x = x
                    min_position_y = y
                    min_distance = self._distance_to_spiral_center(x, y)
            if found:
                self._goto_and_print(lines, min_position_x, min_position_y)

    def _distance_to_spiral_center(self, x, y):
        delta_x = math.fabs(self.spiral_offset_x - x)
        delta_y = math.fabs(self.spiral_offset_y - y)
        return math.sqrt(delta_x * delta_x + delta_y * delta_y)

    def _reset_to_upper_left(self):
        # print('### Reset to (0, 0) ###')
        self._move_to(0, 0)


class ErikaAndInputFacadeFactory:

    @classmethod
    def create_for_path(cls, erika, file_path):
        try:
            image = WrappedImage(file_path)
            return ErikaAndImageInputFacade(erika, image)
        except NotAnImageException:
            lines = _read_lines_without_trailing_newlines(file_path)
            return ErikaAndAsciiArtInputFacade(erika, lines)

    @classmethod
    def create_for_lines(cls, erika, lines):
        return ErikaAndAsciiArtInputFacade(erika, lines)


class ErikaAndInputFacade:

    def move_left(self):
        pass

    def move_right(self):
        pass

    def move_up(self):
        pass

    def move_down(self):
        pass

    def crlf(self):
        pass

    def print_at(self, x, y):
        pass

    def print_line_at(self, y):
        pass

    def print_whole_line(self, line):
        pass


class ErikaAndAsciiArtInputFacade(ErikaAndInputFacade):

    def __init__(self, erika, lines):
        """
        Indirection for rendering ASCII art images - hiding the concrete type of image from the rendering strategy.
        :param erika an Erika instance (or test double)
        :param lines ASCII art image's text lines
        """
        self.erika = erika
        self.lines = lines

    def move_left(self):
        self.erika.move_left()

    def move_right(self):
        self.erika.move_right()

    def move_up(self):
        self.erika.move_up()

    def move_down(self):
        self.erika.move_down()

    def crlf(self):
        self.erika.crlf()

    def print_at(self, x, y):
        self.erika.print_ascii(self.lines[y][x])

    def print_line_at(self, y):
        self.erika.print_ascii(self.lines[y])

    def height(self):
        return len(self.lines)

    def width(self):
        return self._calculate_max_line_length(self.lines)

    @staticmethod
    def _calculate_max_line_length(lines):
        max_length = 0
        for line in lines:
            if len(line) > max_length:
                max_length = len(line)
        return max_length


class ErikaAndImageInputFacade(ErikaAndInputFacade):

    def __init__(self, erika, wrapped_image):
        """
        Indirection for rendering ASCII art images - hiding the concrete type of image from the rendering strategy.
        :param erika an Erika instance (or test double)
        :param wrapped_image a WrappedImage abstracting from the image data
        """
        self.erika = erika
        self.wrapped_image = wrapped_image

        # because we can't rely on the crlf command, we need to keep track of
        # the position along the X axis for supporting "newline" for image output
        self.position_x = 0

    def move_left(self):
        self.erika.move_left_microstep()
        self.position_x -= 1

    def move_right(self):
        self.erika.move_right_microstep()
        self.position_x += 1

    def move_up(self):
        self.erika.move_up_microstep()

    def move_down(self):
        self.erika.move_down_microstep()

    def crlf(self):
        self.erika.move_left_microsteps(self.position_x)
        self.position_x = 0
        self.erika.move_down_microstep()

    def print_at(self, x, y):
        if self.wrapped_image.is_pixel_set(x, y):
            self.erika.print_pixel()
        else:
            self.erika.move_right_microstep()
        self.position_x += 1

    def print_line_at(self, y):
        for x in range(0, self.wrapped_image.width):
            self.print_at(x, y)

    def height(self):
        return self.wrapped_image.height()

    def width(self):
        return self.wrapped_image.width()


def _read_lines_without_trailing_newlines(file_path):
    with open(file_path, "r") as open_file:
        lines = open_file.readlines()
    return _remove_trailing_newlines(lines)


def _remove_trailing_newlines(lines):
    lines_without_newlines = []
    for line in lines:
        lines_without_newlines.append(_remove_trailing_newline(line))
    return lines_without_newlines


def _remove_trailing_newline(line):
    return line.replace('\n', "").replace('\r', "")
