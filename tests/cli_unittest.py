import unittest

from erika.cli import *


class CliTest(unittest.TestCase):
    def test_argument_parser_prints_help(self):
        """simple test that ArgumentParser will parse the given command line"""
        # arrange
        parser = create_argument_parser()
        self.assertIsNotNone(parser)

        #  act / assert - short form of parameters
        args = parser.parse_args(["render_ascii_art_file", "-d", "-p", "/dev/ttyACM0", "-f", "test_file.txt", "-s",
                                  "PerpendicularSpiralInward"])
        self.assertTrue(args.dry_run)
        self.assertEqual(args.file, "test_file.txt")
        self.assertEqual(args.serial_port, "/dev/ttyACM0")
        self.assertEqual(args.strategy, "PerpendicularSpiralInward")

        #  act / assert - long form of parameters
        args = parser.parse_args(
            ["render_ascii_art_file", "--dry-run", "--serial-port", "/dev/ttyACM0", "--file", "test_file.txt",
             "--strategy", "ArchimedeanSpiralOutward"])
        self.assertTrue(args.dry_run)
        self.assertEqual(args.file, "test_file.txt")
        self.assertEqual(args.serial_port, "/dev/ttyACM0")
        self.assertEqual(args.strategy, "ArchimedeanSpiralOutward")

        #  act / assert - defaults
        args = parser.parse_args(["render_ascii_art_file", "-p", "COM3", "-f", "test_file2.txt"])
        self.assertFalse(args.dry_run)
        self.assertEqual(args.file, "test_file2.txt")
        self.assertEqual(args.serial_port, "COM3")
        self.assertEqual(args.strategy, "LineByLine")


def main():
    unittest.main()


if __name__ == '__main__':
    main()
