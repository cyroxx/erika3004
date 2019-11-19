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

from erika_fs.ansii_decoder import EscapeSequenceDecoder

"""page dimensions for Erika"""
# tested manually - the cursor will no longer move if a key is pressed
ERIKA_PAGE_WIDTH_HARD_LIMIT_AT_12_CHARS_PER_INCH = 74
# tested manually - thee will be a warning "beep" on the next pressed key
ERIKA_PAGE_WIDTH_SOFT_LIMIT_AT_12_CHARS_PER_INCH = 65

ERIKA_PAGE_HEIGHT = 150

import curses


class ErikaMock(EscapeSequenceDecoder):
    def _decode_character(self, char):
        pass

    def _cursor_up(self, n=1):
        y, x = self.stdscr.getyx()
        self.stdscr.move(y - n, x)

    def _cursor_down(self, n=1):
        y, x = self.stdscr.getyx()
        self.stdscr.move(y + n, x)

    def _cursor_forward(self, n=1):
        y, x = self.stdscr.getyx()
        self.stdscr.move(y, x + n)

    def _cursor_back(self, n=1):
        y, x = self.stdscr.getyx()
        self.stdscr.move(y, x - n)

    def _cursor_next_line(self, n=1):
        pass

    def _cursor_previous_line(self, n=1):
        pass

    def _cursor_horizontal_absolute(self, n=1):
        pass

    def _cursor_position(self, n=1, m=1):
        pass

    def _erase_in_display(self, n=0):
        pass

    def _erase_in_line(self, n=0):
        pass

    def _scroll_up(self, n=1):
        pass

    def _scroll_down(self, n=1):
        pass

    def _select_graphic_rendition(self, *n):
        pass

    def _aux_port_on(self):
        pass

    def _aux_port_off(self):
        pass

    def _device_status_report(self):
        pass

    def _save_cursor_position(self):
        pass

    def _restore_cursor_position(self):
        pass

    def __init__(self,
                 width=ERIKA_PAGE_WIDTH_SOFT_LIMIT_AT_12_CHARS_PER_INCH,
                 height=ERIKA_PAGE_HEIGHT,
                 exception_if_overprinted=True,
                 output_after_each_step=False,
                 delay_after_each_step=0):
        self.stdscr = curses.initscr()
        # disable input buffer
        curses.cbreak()
        curses.nl()
        # wrap special keys
        self.stdscr.keypad(True)

        self.width = width
        self.height = height
        self.exception_if_overprinted = exception_if_overprinted
        self.output_after_each_step = output_after_each_step
        self.delay_after_each_step = delay_after_each_step

    def __enter__(self):
        return self

    def __exit__(self, *args):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def set_keyboard_echo(self, value):
        if value:
            curses.echo()
        else:
            curses.noecho()

    def alarm(self, duration):
        pass

    def read(self):
        c = chr(self.stdscr.getch())
        return c

    def print_ascii(self, text):
        self.stdscr.addstr(text)

    def _print_raw(self, data):
        raise Exception('User is not supposed to call this function directly')

    def move_up(self):
        self._cursor_up()

    def move_down(self):
        self._cursor_down()

    def move_left(self):
        self._cursor_back()

    def move_right(self):
        self._cursor_forward()

    def crlf(self):
        self.stdscr.addstr("\n")

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

    def test_debug_helper_print_canvas(self):
        """for debugging: print the current canvas to stdout"""
        print(' ' + ''.zfill(self.width).replace('0', '#'))
        for line in self.canvas:
            print('#' + ''.join(line) + '#')
        print(' ' + ''.zfill(self.width).replace('0', '#'))
        print()
