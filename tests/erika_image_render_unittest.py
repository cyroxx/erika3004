# coding=utf-8

import unittest

from erika.erika_image_renderer import *
from tests.erika_mock import *
from tests.erika_mock_unittest import assert_print_output


# noinspection SpellCheckingInspection
class RendererTest(unittest.TestCase):

    def helper_test_ErikaImageRenderingStrategy_square(self, strategy):
        """test helper to verify rendering with the given strategy works"""
        with ErikaMock(6, 6) as my_erika:
            renderer = ErikaImageRenderer(my_erika, strategy)
            renderer.render_ascii_art_file('tests/test_resources/test_ascii_art_small.txt')
            assert_print_output(self, my_erika, ["abcdef", "ghijkl", "mnopqr", "stuvwx", "yzäöüß", "!?#'\"/"])

    def helper_test_ErikaImageRenderingStrategy_high(self, strategy):
        """test helper to verify rendering with the given strategy works"""
        with ErikaMock(3, 12) as my_erika:
            renderer = ErikaImageRenderer(my_erika, strategy)
            renderer.render_ascii_art_file('tests/test_resources/test_ascii_art_small_high.txt')
            assert_print_output(self, my_erika,
                                ["abc", "def", "ghi", "jkl", "mno", "pqr", "stu", "vwx", "yzä", "öüß", "!?#", "'\"/"])

    def helper_test_ErikaImageRenderingStrategy_wide(self, strategy):
        """test helper to verify rendering with the given strategy works"""
        with ErikaMock(9, 4) as my_erika:
            renderer = ErikaImageRenderer(my_erika, strategy)
            renderer.render_ascii_art_file('tests/test_resources/test_ascii_art_small_wide.txt')
            assert_print_output(self, my_erika, ["abcdefghi", "jklmnopqr", "stuvwxyzä", "öüß!?#'\"/"])

    def testLineByLineErikaImageRenderingStrategy(self):
        """simple test that printing line by line works"""
        strategy = LineByLineErikaImageRenderingStrategy()
        self.helper_test_ErikaImageRenderingStrategy_square(strategy)
        self.helper_test_ErikaImageRenderingStrategy_high(strategy)
        self.helper_test_ErikaImageRenderingStrategy_wide(strategy)

    def testInterlacedErikaImageRenderingStrategy(self):
        """simple test that printing odd-then-even lines works"""
        strategy = InterlacedErikaImageRenderingStrategy()
        self.helper_test_ErikaImageRenderingStrategy_square(strategy)
        self.helper_test_ErikaImageRenderingStrategy_high(strategy)
        self.helper_test_ErikaImageRenderingStrategy_wide(strategy)

    def testPerpendicularSpiralInwardErikaImageRenderingStrategy(self):
        """simple test that printing as a perpendicular spiral inward works"""
        strategy = PerpendicularSpiralInwardErikaImageRenderingStrategy()
        self.helper_test_ErikaImageRenderingStrategy_square(strategy)
        self.helper_test_ErikaImageRenderingStrategy_high(strategy)
        self.helper_test_ErikaImageRenderingStrategy_wide(strategy)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
