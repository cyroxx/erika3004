import unittest

from erika.TicTacToe import TicTacToe
from erika.erika_mock import CharacterBasedErikaMock
from tests.erika_mock_unittest import assert_print_output


class TicTacToeUnitTest(unittest.TestCase):
    def test_initial_playing_field(self):
        """Simple test that the initial playing field looks like a tic tac toe grid"""
        with CharacterBasedErikaMock(11, 11, False, inside_unit_test=True) as my_erika:
            game = TicTacToe(my_erika)
            game._print_initial_field()
            assert_print_output(self, my_erika, ["   |   |   ",
                                                 "-----------",
                                                 "   |   |   ",
                                                 "-----------",
                                                 "   |   |   "])

    def test_erika_will_make_a_move(self):
        """test that Erika moves (puts an "o")"""
        with CharacterBasedErikaMock(11, 11, False, inside_unit_test=True) as my_erika:
            game = TicTacToe(my_erika)
            game._print_initial_field()
            game._cursor_to_start_position()

            any_x_on_field = any(['x' in line for line in my_erika.canvas])
            any_o_on_field = any(['o' in line for line in my_erika.canvas])
            self.assertFalse(any_x_on_field, "player should not have moved yet")
            self.assertFalse(any_o_on_field, "erika should not have moved yet")

            game.ai_select()

            any_x_on_field = any(['x' in line for line in my_erika.canvas])
            any_o_on_field = any(['o' in line for line in my_erika.canvas])
            self.assertFalse(any_x_on_field, "player should not have moved yet")
            self.assertTrue(any_o_on_field, "erika should have moved")


def main():
    unittest.main()


if __name__ == '__main__':
    main()
