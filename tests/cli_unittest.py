import io
import unittest
import unittest.mock

from erika.cli import *


class CliTest(unittest.TestCase):
    def test_argument_parser_parses_arguments(self):
        """simple test that ArgumentParser will parse the given command line"""
        # arrange
        parser = create_argument_parser()
        self.assertIsNotNone(parser)

        #  act / assert - short form of parameters
        args = parser.parse_args(["render_ascii_art", "-d", "-p", "/dev/ttyACM0", "-f", "test_file.txt", "-s",
                                  "PerpendicularSpiralInward"])
        self.assertEqual(args.func, print_ascii_art)
        self.assertTrue(args.dry_run)
        self.assertEqual(args.file, "test_file.txt")
        self.assertEqual(args.serial_port, "/dev/ttyACM0")
        self.assertEqual(args.strategy, "PerpendicularSpiralInward")

        #  act / assert - long form of parameters
        args = parser.parse_args(
            ["render_ascii_art", "--dry-run", "--serial-port", "/dev/ttyACM0", "--file", "test_file.txt",
             "--strategy", "ArchimedeanSpiralOutward"])
        self.assertEqual(args.func, print_ascii_art)
        self.assertTrue(args.dry_run)
        self.assertEqual(args.file, "test_file.txt")
        self.assertEqual(args.serial_port, "/dev/ttyACM0")
        self.assertEqual(args.strategy, "ArchimedeanSpiralOutward")

        #  act / assert - defaults
        args = parser.parse_args(["render_ascii_art", "-p", "COM3"])
        self.assertEqual(args.func, print_ascii_art)
        self.assertFalse(args.dry_run)
        self.assertEqual(args.file, "-")
        self.assertEqual(args.serial_port, "COM3")
        self.assertEqual(args.strategy, "LineByLine")

        #  act / assert - demo mode
        args = parser.parse_args(["demo", "-p", "COM3", "-d"])
        self.assertEqual(args.func, print_demo)
        self.assertTrue(args.dry_run)
        self.assertEqual(args.serial_port, "COM3")

    def test_argument_parser_prints_help(self):
        """simple test that ArgumentParser will print help text and exit"""
        # arrange
        parser = create_argument_parser()
        self.assertIsNotNone(parser)

        # act / assert
        # https://stackoverflow.com/a/46307456/1143126
        actual_stdout = self.call_parse_args_and_capture_stdout(parser, ["--help"])
        self.assertTrue("-h" in actual_stdout)
        self.assertTrue("--help" in actual_stdout)
        self.assertTrue("erika_sh" in actual_stdout)
        self.assertTrue("render_ascii_art" in actual_stdout)
        self.assertTrue("demo" in actual_stdout)

        # act / assert
        actual_stdout = self.call_parse_args_and_capture_stdout(parser, ["-h"])
        self.assertTrue("-h" in actual_stdout)
        self.assertTrue("--help" in actual_stdout)
        self.assertTrue("erika_sh" in actual_stdout)
        self.assertTrue("render_ascii_art" in actual_stdout)
        self.assertTrue("demo" in actual_stdout)

        # act / assert
        actual_stdout = self.call_parse_args_and_capture_stdout(parser, ["render_ascii_art", "--help"])
        self.assertTrue("-h" in actual_stdout)
        self.assertTrue("--help" in actual_stdout)
        self.assertTrue("erika_sh render_ascii_art" in actual_stdout)
        self.assertTrue("--file FILEPATH, -f FILEPATH" in actual_stdout)
        self.assertTrue("--dry-run, -d" in actual_stdout)
        self.assertTrue("--serial-port SERIAL_PORT, -p SERIAL_PORT" in actual_stdout)
        self.assertTrue("--strategy" in actual_stdout)
        self.assertTrue("LineByLine" in actual_stdout)
        self.assertTrue("Interlaced" in actual_stdout)
        self.assertTrue("PerpendicularSpiralInward" in actual_stdout)
        self.assertTrue("RandomDotFill" in actual_stdout)
        self.assertTrue("ArchimedeanSpiralOutward" in actual_stdout)

        # act / assert
        actual_stdout = self.call_parse_args_and_capture_stdout(parser, ["render_ascii_art", "-h"])
        self.assertTrue("-h" in actual_stdout)
        self.assertTrue("--help" in actual_stdout)
        self.assertTrue("erika_sh render_ascii_art" in actual_stdout)
        self.assertTrue("--file FILEPATH, -f FILEPATH" in actual_stdout)
        self.assertTrue("--dry-run, -d" in actual_stdout)
        self.assertTrue("--serial-port SERIAL_PORT, -p SERIAL_PORT" in actual_stdout)
        self.assertTrue("--strategy" in actual_stdout)
        self.assertTrue("LineByLine" in actual_stdout)
        self.assertTrue("Interlaced" in actual_stdout)
        self.assertTrue("PerpendicularSpiralInward" in actual_stdout)
        self.assertTrue("RandomDotFill" in actual_stdout)
        self.assertTrue("ArchimedeanSpiralOutward" in actual_stdout)

        # act / assert
        actual_stdout = self.call_parse_args_and_capture_stdout(parser, ["demo", "--help"])
        self.assertTrue("-h" in actual_stdout)
        self.assertTrue("--help" in actual_stdout)
        self.assertTrue("erika_sh demo" in actual_stdout)
        self.assertTrue("--dry-run, -d" in actual_stdout)
        self.assertTrue("--serial-port SERIAL_PORT, -p SERIAL_PORT" in actual_stdout)

        # act / assert
        actual_stdout = self.call_parse_args_and_capture_stdout(parser, ["demo", "-h"])
        self.assertTrue("-h" in actual_stdout)
        self.assertTrue("--help" in actual_stdout)
        self.assertTrue("erika_sh demo" in actual_stdout)
        self.assertTrue("--dry-run, -d" in actual_stdout)
        self.assertTrue("--serial-port SERIAL_PORT, -p SERIAL_PORT" in actual_stdout)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def call_parse_args_and_capture_stdout(self, parser, args, mock_stdout):
        self.assertRaises(SystemExit, parser.parse_args, args)
        return mock_stdout.getvalue()


def main():
    unittest.main()


if __name__ == '__main__':
    main()
