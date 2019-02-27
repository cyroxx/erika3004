import json
import time

import serial

DEFAULT_DELAY = 0.5


class Erika:
    conversion_table_path = "erika/charTranslation.json"

    def __init__(self, com_port, *args, **kwargs):
        self.com_port = com_port
        self.connection = serial.Serial(com_port, 1200)  # , timeout=0, parity=serial.PARITY_EVEN, rtscts=1)
        self.ascii_2_ddr = {}
        self.ddr_2_ascii = {}
        self.read_conversion_table()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.connection.close()

    def read_conversion_table(self):
        """read conversion table from file and populate 2 dicts"""
        with open(self.conversion_table_path, encoding="UTF-8") as f:
            self.ascii_2_ddr = json.load(f)
        self.ddr_2_ascii = {value: key for key, value in self.ascii_2_ddr.items()}

    def write_delay(self, data, delay=DEFAULT_DELAY):
        self.write_byte_delay(data.encode("ASCII"), delay)

    def write_byte_delay(self, data, delay=DEFAULT_DELAY):
        self.connection.write(bytes.fromhex(data))
        time.sleep(delay)

    def print_smiley(self):
        self.write_delay('\x13')
        self.write_delay('\x1F')

    def advance_paper(self):
        # move paper up / cursor down
        for i in range(0, 10):
            self.connection.write(b'\x75')
            time.sleep(DEFAULT_DELAY)

    def demo(self):
        self.advance_paper()
        self.print_smiley()
        self.advance_paper()

    # TODO: use duration parameter instead of fixed value
    def alarm(self, duration):
        self.connection.write(b"\xaa\xff")

    def read(self):
        key_id = self.connection.read()
        return self.ddr_2_ascii.get(key_id.hex().upper(), key_id.hex())

    def print_ascii(self, text):
        for c in text:
            key_id = self.ascii_2_ddr[c]
            self.write_byte_delay(key_id)

    def print_raw(self, data):
        self.connection.write(bytes.fromhex(data))

    def move_up(self):
        self.print_raw("76")
        self.print_raw("76")

    def move_down(self):
        self.print_raw("75")
        self.print_raw("75")

    def move_left(self):
        self.print_raw("74")
        self.print_raw("74")

    def move_right(self):
        self.print_raw("73")
        self.print_raw("73")

    def crlf(self):
        self.print_raw("78")
        self.print_raw("9F")
