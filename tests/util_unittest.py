import unittest

from erika.util import twos_complement
from erika.util import twos_complement_hex_string


class UtilTest(unittest.TestCase):

    def test_twos_complement_invalid(self):
        with self.assertRaises(Exception) as context_high:
            twos_complement(128)
        e_high = context_high.exception
        self.assertTrue("high" in str(e_high))

        with self.assertRaises(Exception) as context_low:
            twos_complement(-129)
        e_low = context_low.exception
        self.assertTrue("low" in str(e_low))

    def test_twos_complement_positive(self):
        self.assertEqual(0, twos_complement(0))
        self.assertEqual(1, twos_complement(1))
        self.assertEqual(23, twos_complement(23))
        self.assertEqual(42, twos_complement(42))
        self.assertEqual(127, twos_complement(127))

        self.assertEqual(b'\x00', twos_complement(0).to_bytes(1, 'little'))
        self.assertEqual(b'\x01', twos_complement(1).to_bytes(1, 'little'))
        self.assertEqual(b'\x17', twos_complement(23).to_bytes(1, 'little'))
        self.assertEqual(b'\x2A', twos_complement(42).to_bytes(1, 'little'))
        self.assertEqual(b'\x7F', twos_complement(127).to_bytes(1, 'little'))

    def test_twos_complement_negative(self):
        self.assertEqual(b'\xFF', twos_complement(-1).to_bytes(1, 'little'))
        self.assertEqual(b'\xE9', twos_complement(-23).to_bytes(1, 'little'))
        self.assertEqual(b'\xD6', twos_complement(-42).to_bytes(1, 'little'))
        self.assertEqual(b'\x81', twos_complement(-127).to_bytes(1, 'little'))
        self.assertEqual(b'\x80', twos_complement(-128).to_bytes(1, 'little'))

        self.assertEqual(255, twos_complement(-1))
        self.assertEqual(233, twos_complement(-23))
        self.assertEqual(214, twos_complement(-42))
        self.assertEqual(129, twos_complement(-127))
        self.assertEqual(128, twos_complement(-128))

    def test_twos_complement_hex_string_positive(self):
        self.assertEqual("00", twos_complement_hex_string(0))
        self.assertEqual("01", twos_complement_hex_string(1))
        self.assertEqual("17", twos_complement_hex_string(23))
        self.assertEqual("2A", twos_complement_hex_string(42))
        self.assertEqual("7F", twos_complement_hex_string(127))

    def test_twos_complement_hex_string_negative(self):
        self.assertEqual("FF", twos_complement_hex_string(-1))
        self.assertEqual("E9", twos_complement_hex_string(-23))
        self.assertEqual("D6", twos_complement_hex_string(-42))
        self.assertEqual("81", twos_complement_hex_string(-127))
        self.assertEqual("80", twos_complement_hex_string(-128))


def main():
    unittest.main()


if __name__ == '__main__':
    main()
