import time
from enum import Enum

import serial

from erika.erica_encoder_decoder import DDR_ASCII
from erika_fs.ansii_decoder import EscapeSequenceDecoder

ERIKA_BAUDRATE = 1200

DEFAULT_DELAY = 0.3
LINE_BREAK_DELAY = 2.0


class Direction(Enum):
    RIGHT = "73"
    LEFT = "74"
    UP = "76"
    DOWN = "75"


class Erika(EscapeSequenceDecoder):
    conversion_table_path = "erika/charTranslation.json"

    def __init__(self, com_port, *args, **kwargs):
        """Set comport to serial device that connects to Erika typewriter."""
        self.com_port = com_port
        self.connection = serial.Serial(com_port, ERIKA_BAUDRATE)  # , timeout=0, parity=serial.PARITY_EVEN, rtscts=1)
        self.ddr_ascii = DDR_ASCII()

    ## resource manager stuff

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.connection.close()

    ##########################

    def alarm(self, duration):
        """Sound alarm for given duration [s]"""
        assert duration <= 5.1, "duration must be less than or equal to 5.1 seconds"
        duration /= 0.02
        duration_hex = hex(round(duration))
        self._print_raw("AA")
        self._print_raw(chr(duration_hex[1:]))
        # self.connection.write(b"\xaa\xff")

    # TODO: use duration parameter instead of fixed value
    def read(self):
        """Read a character data from the Erika typewriter and try to decode it.
        Returns: ASCII encoded character
        """
        key_id = self.connection.read()
        return self.ddr_ascii.try_decode(key_id.hex().upper())

    def print_ascii(self, text, esc_sequences=False):
        """Print given string on the Erika typewriter."""
        # TODO: handle escape sequences
        if esc_sequences:
            self.decode(text)
        for c in text:
            key_id = self.ddr_ascii.encode(c)
            self._write_byte_delay(key_id)

    def move_up(self):
        self._print_raw("76")
        time.sleep(DEFAULT_DELAY)
        self._print_raw("76")
        time.sleep(DEFAULT_DELAY)

    def move_down(self):
        self._print_raw("75")
        time.sleep(DEFAULT_DELAY)
        self._print_raw("75")
        time.sleep(DEFAULT_DELAY)

    def move_left(self):
        self._print_raw("74")
        time.sleep(DEFAULT_DELAY)
        self._print_raw("74")
        time.sleep(DEFAULT_DELAY)

    def move_right(self):
        self._print_raw("73")
        time.sleep(DEFAULT_DELAY)
        self._print_raw("73")
        time.sleep(DEFAULT_DELAY)

    def crlf(self):
        self._print_raw("77")
        time.sleep(LINE_BREAK_DELAY)

    def set_keyboard_echo(self, value):
        if value:
            self._print_raw("92")
        else:
            self._print_raw("91")

    def demo(self):
        self._advance_paper()
        self._print_smiley()
        self._advance_paper()

    def _advance_paper(self):
        """ move paper up / cursor down by 10 halfsteps"""
        self._scroll_up(5)  # self._cursor_down(5)

    def _print_smiley(self):
        """print a smiley"""
        self._write_byte_delay('13')
        self._write_byte_delay('1F')

    def _write_byte_delay(self, data, delay=DEFAULT_DELAY):
        """print base16 encoded data with delay"""
        self._print_raw(data)
        time.sleep(delay)

    def _print_raw(self, data):
        """prints base16 formated data"""
        self.connection.write(bytes.fromhex(data))

    def _move_erika(self, direction: Direction, n=1):
        """
        Moves n full steps in the given direction.

        :param direction: direction to move: Direction
        :param n: number of full steps to move
        """
        self._print_raw(direction.value * (2 * n))

    def _cursor_up(self, n=1):
        self._move_erika(Direction.UP, n)

    def _cursor_down(self, n=1):
        self._move_erika(Direction.DOWN, n)

    def _cursor_forward(self, n=1):
        self._move_erika(Direction.RIGHT, n)

    def _cursor_back(self, n=1):
        self._move_erika(Direction.LEFT, n)

    def _cursor_next_line(self, n=1):
        self._cursor_down(n)
        self.print_ascii("\r")

    def _cursor_previous_line(self, n=1):
        self._cursor_up(n)
        self.print_ascii("\r")

    def _decode_character(self, char):
        key_id = self.ddr_ascii.encode(char)
        self._write_byte_delay(key_id)

    def _cursor_horizontal_absolute(self, n=1):
        pass

    def _cursor_position(self, n=1, m=1):
        pass

    def _erase_in_display(self, n=0):
        pass

    def _erase_in_line(self, n=0):
        pass

    def _scroll_up(self, n=1):
        self._cursor_down(n)

    def _scroll_down(self, n=1):
        self._cursor_up(n)

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
