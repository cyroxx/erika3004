import time
import unittest
import pytest

from erika.erika import Erika

# TODO make parameter dynamic

# e.g. Linux
# (determine port by observing output of
#   dmesg
# on the command line after connecting USB)
#
# e.g. Linux
# COM_PORT = "/dev/ttyACM0"
COM_PORT = "/dev/ttyUSB0"

# e.g. Windows
# COM_PORT = "COM3"

@pytest.mark.hardware
class ConnectTest(unittest.TestCase):
    def test_connect(self):
        """simple test that there is no exception when connecting"""
        with Erika(COM_PORT) as ignored:
            pass

    def test_movement(self):
        """simple test to test cursor movement - validation is manual check of cursor movement"""
        delay = 0
        with Erika(COM_PORT) as my_erika:
            for i in range(10):
                my_erika.move_right()
                time.sleep(delay)
            for i in range(10):
                my_erika.move_up()
                time.sleep(delay)
            for i in range(10):
                my_erika.move_left()
                time.sleep(delay)
            for i in range(10):
                my_erika.move_down()
                time.sleep(delay)

    def test_write(self):
        """simple test that there is no exception when connecting"""
        with Erika(COM_PORT) as my_erika:
            my_erika.crlf()
            my_erika.print_ascii("Hello, World!")
            my_erika.crlf()


def main():
    unittest.main()


if __name__ == '__main__':
    main()
