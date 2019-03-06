class ErikaImageRenderer:
    def __init__(self, some_erika, rendering_strategy):
        self.output_device = some_erika
        self.rendering_strategy = rendering_strategy
        self.rendering_strategy.set_output_device(some_erika)

    def render_ascii_art_file(self, filePath):
        self.rendering_strategy.render_ascii_art_file(filePath)


class ErikaImageRenderingStrategy:

    def __init__(self):
        pass

    # noinspection PyAttributeOutsideInit
    def set_output_device(self, some_erika):
        self.output_device = some_erika

    def render_ascii_art_file(self, file_path):
        raise Exception('Not implemented')

    def remove_trailing_newline(self, line):
        return line.replace('\n', "")

    def read_lines_without_trailing_newlines(self, open_file):
        lines = open_file.readlines()
        lines_without_newlines = []
        for line in lines:
            lines_without_newlines.append(self.remove_trailing_newline(line))
        return lines_without_newlines


class LineByLineErikaImageRenderingStrategy(ErikaImageRenderingStrategy):

    def __init__(self):
        ErikaImageRenderingStrategy.__init__(self)

    def render_ascii_art_file(self, file_path):
        with open(file_path, "r") as open_file:
            for line in open_file.readlines():
                line_without_newline = line.replace('\n', "")
                self.output_device.print_ascii(line_without_newline)
                self.output_device.crlf()


class InterlacedErikaImageRenderingStrategy(ErikaImageRenderingStrategy):

    def __init__(self):
        ErikaImageRenderingStrategy.__init__(self)

    def render_ascii_art_file(self, file_path):
        with open(file_path, "r") as open_file:
            lines = open_file.readlines()
            line_count = len(lines)
            moved = 0
            for even in range(0, line_count, 2):
                line_without_newline = lines[even].replace('\n', "")
                self.output_device.print_ascii(line_without_newline)
                self.output_device.crlf()
                self.output_device.crlf()
                moved += 2

            # reset cursor to start of line
            self.output_device.crlf()

            # do not compensate the line that this adds - the extra line will position the cursor right where we want it
            # self.output_device.move_up()

            for lines_to_move_up in range(0, moved):
                self.output_device.move_up()

            for odd in range(1, line_count, 2):
                line_without_newline = lines[odd].replace('\n', "")
                self.output_device.print_ascii(line_without_newline)
                self.output_device.crlf()
                self.output_device.crlf()


class PerpendicularSpiralInwardErikaImageRenderingStrategy(ErikaImageRenderingStrategy):

    def __init__(self):
        ErikaImageRenderingStrategy.__init__(self)

    def render_ascii_art_file(self, file_path):
        with open(file_path, "r") as open_file:
            lines = self.read_lines_without_trailing_newlines(open_file)
            line_count = len(lines)
            max_line_length = self.calculate_max_line_length(lines)
            self.print_spiral_recursively(lines, 0, 0, max_line_length - 1, line_count - 1)

    def calculate_max_line_length(self, lines):
        max_length = 0
        for line in lines:
            if len(line) > max_length:
                max_length = len(line)
        return max_length

    def print_spiral_recursively(self, lines, upper_left_x, upper_left_y, lower_right_x, lower_right_y):
        """ASSUMPTION: current position is at (upper_left_x, upper_left_y)"""
        if upper_left_x > lower_right_x or upper_left_y > lower_right_y:
            return

        # render one round of the spiral, clockwise

        #
        # =====>
        #
        for x in range(upper_left_x, lower_right_x + 1):
            self.output_device.print_ascii(lines[upper_left_y][x])

        # edge case: this was the only last row
        if upper_left_y == lower_right_y:
            return

        # reset to last cursor position
        self.output_device.move_left()

        # go down - do not print a character twice
        self.output_device.move_down()

        # ||
        # ||
        # \/
        for y in range(upper_left_y + 1, lower_right_y):
            self.output_device.print_ascii(lines[y][lower_right_x])
            self.output_device.move_down()
            self.output_device.move_left()

        # special handling of last character - smoothen transition
        self.output_device.print_ascii(lines[lower_right_y][lower_right_x])

        # edge case: this was the only last column
        if upper_left_x == lower_right_x:
            return

        # back to last printed character
        self.output_device.move_left()
        self.output_device.move_left()

        #
        # <=====
        #
        for x in range(lower_right_x - 1, upper_left_x - 1, -1):
            self.output_device.print_ascii(lines[lower_right_y][x])
            self.output_device.move_left()
            self.output_device.move_left()

        self.output_device.move_right()
        self.output_device.move_up()

        # /\
        # ||
        # ||
        for y in range(lower_right_y - 1, upper_left_y + 1, -1):
            self.output_device.print_ascii(lines[y][upper_left_x])
            self.output_device.move_up()
            self.output_device.move_left()


        # special handling of last character - smoothen transition
        if lower_right_y - 1 >= upper_left_y + 1:
            self.output_device.print_ascii(lines[upper_left_y + 1][upper_left_x])

        # continue with smaller spiral - restart recursion
        self.print_spiral_recursively(lines, upper_left_x + 1, upper_left_y + 1, lower_right_x - 1, lower_right_y - 1)
