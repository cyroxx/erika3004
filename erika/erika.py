import time

import serial

from erika.erica_encoder_decoder import DDR_ASCII
from erika.util import twos_complement_hex_string

DEFAULT_DELAY = 0.0
LINE_BREAK_DELAY = 0.0

# confirmed experimentally
MICROSTEPS_PER_CHARACTER_WIDTH = 10

# confirmed experimentally
MICROSTEPS_PER_CHARACTER_HEIGHT = 20


# special decorator: enforce that subclasses implement the method
# See https://stackoverflow.com/a/25651022
def enforcedmethod(func):
    func.__enforcedmethod__ = True
    return func


class MetaclassForEnforcingMethods:

    # verify that enforced methods are implemented
    def __new__(cls, *args, **kwargs):
        method_names = set()
        not_found_enforced_methods = set()
        # search through method resolution order
        method_resolution_order = cls.__mro__
        for base_class in method_resolution_order:
            for name, value in base_class.__dict__.items():
                # method_names are collected in this dictionary while going up the inheritance hierarchy.
                # If the method is not in there when the method is marked <to be enforced in the current base_class,
                # it has not been implemented in a base class as expected.
                if getattr(value, "__enforcedmethod__", False) and name not in method_names:
                    not_found_enforced_methods.add(name)
                method_names.add(name)

        if not_found_enforced_methods:
            raise TypeError("Can't instantiate abstract class {} - must implement enforced methods {}"
                            .format(cls.__name__, ', \n'.join(not_found_enforced_methods)))
        else:
            return super(MetaclassForEnforcingMethods, cls).__new__(cls)


class AbstractErika(MetaclassForEnforcingMethods):

    # verify that all "public" methods are part of this "interface" class
    def __new__(cls, *args, **kwargs):
        not_found_methods = set()

        # search through method resolution order
        method_resolution_order = cls.__mro__
        for base_class in method_resolution_order:
            for name, value in base_class.__dict__.items():
                if not name.startswith("_") and name not in AbstractErika.__dict__:
                    not_found_methods.add(name)
        if not_found_methods:
            raise TypeError("Can't instantiate abstract class {}. All public methods (not starting with underscore) "
                            "must be part of the AbstractErika base class: {}"
                            .format(cls.__name__, ', \n'.join(not_found_methods)))
        else:
            return super(AbstractErika, cls).__new__(cls)


    @enforcedmethod
    def alarm(self, duration):
        pass

    @enforcedmethod
    def read(self):
        pass

    @enforcedmethod
    def print_ascii(self, text):
        pass

    @enforcedmethod
    def move_up(self):
        pass

    @enforcedmethod
    def move_down(self):
        pass

    @enforcedmethod
    def move_left(self):
        pass

    @enforcedmethod
    def move_right(self):
        pass

    @enforcedmethod
    def move_down_microstep(self):
        pass

    @enforcedmethod
    def move_up_microstep(self):
        pass

    @enforcedmethod
    def move_right_microsteps(self, num_steps=1):
        pass

    @enforcedmethod
    def move_left_microsteps(self, num_steps=1):
        pass

    @enforcedmethod
    def crlf(self):
        pass

    @enforcedmethod
    def set_keyboard_echo(self, value):
        pass

    @enforcedmethod
    def demo(self):
        pass

    @enforcedmethod
    def print_pixel(self):
        pass


class Erika(AbstractErika):

    def __init__(self, com_port, *args, **kwargs):
        """Set comport to serial device that connects to Erika typewriter."""
        self.com_port = com_port
        self.connection = serial.Serial(com_port, 1200, rtscts=True)  # , timeout=0, parity=serial.PARITY_EVEN, rtscts=1)
        self.ddr_ascii = DDR_ASCII()

    ## resource manager stuff

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.connection.close()

    ##########################

    def alarm(self, duration):
        """Sound alarm for as long as possible"""
        self._print_raw("AA")
        self._print_raw("FF")
        # self.connection.write(b"\xaa\xff")

    # TODO: use duration parameter instead of fixed value
    def read(self):
        """Read a character data from the Erika typewriter and try to decode it.
        Returns: ASCII encoded character
        """
        key_id = self.connection.read()
        return self.ddr_ascii.try_decode(key_id.hex().upper())

    def print_ascii(self, text):
        """Print given string on the Erika typewriter."""
        for c in text:
            key_id = self.ddr_ascii.encode(c)
            self._write_byte_delay(key_id)
    
    def _set_reverse_printing_mode(self, value):
        if value:
            self._print_raw("8E")
        else:
            self._print_raw("8D")

    def _set_correction_mode(self, value):
        if value:
            self._print_raw("8C")
        else:
            self._print_raw("8B")
    
    def _delete_ascii(self, text):
        """Delete given string on the Erika typewriter."""

        # enable correction_mode and reverse printing
        self._set_correction_mode(True)
        self._set_reverse_printing_mode(True)
        
        # send text to be deleted
        self.print_ascii(text)

        # reset to normal operating mode
        self._set_reverse_printing_mode(False)
        self._set_correction_mode(False)

    def move_up(self):
        self._write_byte_delay("76")
        self._write_byte_delay("76")

    def move_down(self):
        self._write_byte_delay("75")
        self._write_byte_delay("75")

    def move_left(self):
        self._write_byte_delay("74")
        self._write_byte_delay("74")

    def move_right(self):
        self._write_byte_delay("73")
        self._write_byte_delay("73")

    def move_down_microstep(self):
        self._write_byte_delay("81")

    def move_up_microstep(self):
        self._write_byte_delay("82")

    def move_right_microsteps(self, num_steps=1):
        while num_steps > 127:
            self._write_byte_delay("A5")
            self._write_byte_delay(twos_complement_hex_string(127))
            num_steps = num_steps - 127

        self._write_byte_delay("A5")
        self._write_byte_delay(twos_complement_hex_string(num_steps))

    def move_left_microsteps(self, num_steps=1):
        # two's complement numbers: negative value range is 1 bigger than positive (because 0 positive)
        while num_steps > 128:
            self._write_byte_delay("A5")
            self._write_byte_delay(twos_complement_hex_string(-128))
            num_steps = num_steps - 128

        self._write_byte_delay("A5")
        self._write_byte_delay(twos_complement_hex_string(-1 * num_steps))

    def print_pixel(self):
        """
        Print pixel and end up one microstep to the right of the initial position (in analogue to "normal" text printing)
        :return:
        """
        self.print_ascii(".")
        self.move_left_microsteps(MICROSTEPS_PER_CHARACTER_WIDTH - 1)

    def crlf(self):
        self._write_byte_delay("77")

    def set_keyboard_echo(self, value):
        if value:
            self._print_raw("92")
        else:
            self._print_raw("91")

    def demo(self):
        self.crlf()
        # self._print_smiley()
        self._print_demo_rectangle()
        self._advance_paper()

    def _print_demo_rectangle(self):

        for i in range(0, 10):
            self.print_ascii(".")
            self.move_left_microsteps(MICROSTEPS_PER_CHARACTER_WIDTH - 1)

        self.move_left_microsteps(1)

        for i in range(0, 5):
            self.move_down_microstep()
            self.print_ascii(".")
            self.move_left_microsteps(MICROSTEPS_PER_CHARACTER_WIDTH)

        self.move_left_microsteps(1)

        for i in range(0, 10):
            self.print_ascii(".")
            self.move_left_microsteps(MICROSTEPS_PER_CHARACTER_WIDTH + 1)

        self.move_right_microsteps(1)

        for i in range(0, 5):
            self.move_up_microstep()
            self.print_ascii(".")
            self.move_left_microsteps(MICROSTEPS_PER_CHARACTER_WIDTH)

    def _print_precision_test(self):
        self.crlf()
        self.crlf()

        self.print_ascii(".")
        self.move_left_microsteps(MICROSTEPS_PER_CHARACTER_WIDTH)
        self.move_right_microsteps(256)
        self.print_ascii(".")
        self.move_left_microsteps(MICROSTEPS_PER_CHARACTER_WIDTH)

        self.move_down_microstep()
        self.move_down_microstep()

        self.move_left_microsteps(256)
        self.print_ascii(".")
        self.move_left_microsteps(MICROSTEPS_PER_CHARACTER_WIDTH)
        self.move_right_microsteps(256)
        self.print_ascii(".")

    def _advance_paper(self):
        """ move paper up / cursor down by 10 halfsteps"""
        for i in range(0, 10):
            self.connection.write(b'\x75')  # TODO use self.move_down() instead?
            time.sleep(DEFAULT_DELAY)

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
