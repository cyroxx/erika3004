"""
Record any printing and movement calls to Erika in a 2D array for testing purposes:

    x
    ===>
y ||
  ||
  \/

This way, rendering algorithms can be tested.
"""
import sys
from time import sleep
from erika.erika import AbstractErika

"""page dimensions for Erika"""
# tested manually - the cursor will no longer move if a key is pressed
ERIKA_PAGE_WIDTH_HARD_LIMIT_AT_12_CHARS_PER_INCH = 74
# tested manually - thee will be a warning "beep" on the next pressed key
ERIKA_PAGE_WIDTH_SOFT_LIMIT_AT_12_CHARS_PER_INCH = 65

ERIKA_PAGE_HEIGHT = 150


class ErikaMock(AbstractErika):

    def __init__(self,
                 width=ERIKA_PAGE_WIDTH_SOFT_LIMIT_AT_12_CHARS_PER_INCH,
                 height=ERIKA_PAGE_HEIGHT,
                 exception_if_overprinted=True,
                 output_after_each_step=False,
                 delay_after_each_step=0):
        self.width = width
        self.height = height
        self.canvas = []
        for y in range(height):
            new_list = []
            for x in range(width):
                new_list.append(" ")
            self.canvas.append(new_list)
        self.canvas_x = 0
        self.canvas_y = 0
        self.exception_if_overprinted = exception_if_overprinted
        self.output_after_each_step = output_after_each_step
        self.delay_after_each_step = delay_after_each_step

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def alarm(self, duration):
        pass

    def read(self):
        # reading not needed for current tests
        pass

    def print_ascii(self, text):
        for c in text:
            try:
                # print('Trying to print letter "{}" at ({}, {}).'.format(c, self.canvas_x, self.canvas_y))
                if not self.canvas[self.canvas_y][self.canvas_x] == " ":
                    if self.exception_if_overprinted:
                        raise Exception(
                            "Not supposed to print a letter twice: '{}' at ({}, {})."
                                .format(c, self.canvas_x, self.canvas_y))
                self.canvas[self.canvas_y][self.canvas_x] = c
            except IndexError as e:
                print("IndexError at ({}, {}) of ({}, {}) - increase values of "
                      "cli.DRY_RUN_WIDTH and cli.DRY_RUN_HEIGHT "
                      "if you need more space".format(self.canvas_x, self.canvas_y, self.width, self.height))
                sys.exit(1)

            self.canvas_x += 1
            if self.output_after_each_step:
                self._test_debug_helper_print_canvas()
                if self.delay_after_each_step > 0:
                    sleep(self.delay_after_each_step)

    def _print_raw(self, data):
        raise Exception('User is not supposed to call this function directly')

    def move_up(self):
        self.canvas_y -= 1

    def move_down(self):
        self.canvas_y += 1

    def move_left(self):
        self.canvas_x -= 1

    def move_right(self):
        self.canvas_x += 1

    def crlf(self):
        self.canvas_x = 0
        self.canvas_y += 1

    def demo(self):
        for i in range(0, 10):
            self.move_down()
        self.print_ascii(":)")
        for i in range(0, 10):
            self.move_down()

    def _advance_paper(self):
        raise Exception('User is not supposed to call this function directly')

    def _write_byte_delay(self, data, delay=0.5):
        raise Exception('User is not supposed to call this function directly')

    def _test_debug_helper_print_canvas(self):
        """for debugging: print the current canvas to stdout"""
        print(' ' + ''.zfill(self.width).replace('0', '#'))
        for line in self.canvas:
            print('#' + ''.join(line) + '#')
        print(' ' + ''.zfill(self.width).replace('0', '#'))
        print()

    def move_down_microstep(self):
        raise Exception('Microsteps are not supported in character-based tests')

    def move_up_microstep(self):
        raise Exception('Microsteps are not supported in character-based tests')

    def move_right_microsteps(self, num_steps=1):
        raise Exception('Microsteps are not supported in character-based tests')

    def move_left_microsteps(self, num_steps=1):
        raise Exception('Microsteps are not supported in character-based tests')

    def set_keyboard_echo(self, value):
        raise Exception('Not supported yet')

