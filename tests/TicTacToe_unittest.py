import unittest

from erika.TicTacToe import TicTacToe
from erika.erika_mock import CharacterBasedErikaMock
from tests.erika_mock_unittest import assert_print_output


class TicTacToeUnitTest(unittest.TestCase):
    def test_initial_playing_field(self):
        """Simple test that the initial playing field looks like a tic tac toe grid"""
        with CharacterBasedErikaMock(11, 11, False, inside_unit_test=True) as my_erika:
            game = TicTacToe(my_erika)
            game.print_initial_field()
            assert_print_output(self, my_erika, ["   |   |   ",
                                                 "-----------",
                                                 "   |   |   ",
                                                 "-----------",
                                                 "   |   |   "])


def main():
    unittest.main()


if __name__ == '__main__':
    main()
