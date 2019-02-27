# coding=utf-8

import unittest

from erika.erika_image_renderer import *
from tests.erika_mock import *
from tests.erika_mock_unittest import assert_print_output


# noinspection SpellCheckingInspection
class RendererTest(unittest.TestCase):

    def helper_test_ErikaImageRenderingStrategy(self, strategy):
        """test helper to verify rendering with the given strategy works"""
        with ErikaMock(6, 6) as my_erika:
            renderer = ErikaImageRenderer(my_erika, strategy)
            renderer.render_ascii_art_file('tests/test_resources/test_ascii_art_small.txt')
            assert_print_output(self, my_erika, ["abcdef", "ghijkl", "mnopqr", "stuvwx", "yzäöüß", "!?#'\"/"])

    def testLineByLineErikaImageRenderingStrategy(self):
        """simple test that printing line by line works"""
        strategy = LineByLineErikaImageRenderingStrategy()
        self.helper_test_ErikaImageRenderingStrategy(strategy)


    def testInterlacedErikaImageRenderingStrategy(self):
        """simple test that printing odd-then-even lines works"""
        strategy = InterlacedErikaImageRenderingStrategy()
        self.helper_test_ErikaImageRenderingStrategy(strategy)



def main():
    unittest.main()


if __name__ == '__main__':
    main()
