from enum import Enum
from math import ceil

import numpy as np

from erika.erika import Erika
from erika.erika_mock import CharacterBasedErikaMock


class Players(Enum):
    Erika = 1
    Player1 = 2
    N0NE = 0


player_chars = [" ", "o", "x"]


def create_field(field_size=3, cell_width=3, cell_height=1, vertical_sep="#", horizontal_sep="#"):
    cell = " " * cell_width
    row = vertical_sep.join([cell] * field_size)
    horizontal_line = "\n" + (horizontal_sep * len(row)) + "\n"
    result = horizontal_line.join(["\n".join([row] * cell_height)] * field_size)
    return result


class TicTacToe:

    def __init__(self, erika):
        # configure game field
        self.field_size = 3
        self.cell_width = 3
        self.cell_height = 1
        self.vertical_sep = "|"
        self.horizontal_sep = "-"
        assert self.field_size % 2 == 1
        self.game_field = np.zeros((self.field_size, self.field_size), dtype=np.uint8)

        # setup initial cursor position
        self.pos_y = self.pos_x = self.field_size - 1
        self.last_move_x = self.pos_x
        self.last_move_y = self.pos_y

        self.game_over = False
        self.turn = -1

        # setup erika
        self.erika = erika

        self.start_game()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.erika.__exit__()

    def start_game(self):
        # disable keyboard echo
        self.erika.set_keyboard_echo(False)

        # print field
        ascii_field = create_field(self.field_size, cell_height=self.cell_height
                                   , cell_width=self.cell_width, vertical_sep=self.vertical_sep
                                   , horizontal_sep=self.horizontal_sep)
        self.erika.print_ascii(ascii_field)

        # move to center / init position
        self.erika._cursor_back(ceil(self.cell_width / 2))
        self.move_left(self.pos_x // 2)

        self.erika._cursor_up(self.cell_height // 2)
        self.move_up(self.pos_y // 2)

        self.turn = np.random.randint(1, 3)
        self.game_over = False
        self.game_loop()

    def game_loop(self):
        while not self.game_over:
            if self.turn == Players.Erika.value:
                self.ai_select()
            else:
                inp = self.erika.read()
                input_mapping = {
                    "w": self.move_up
                    , "a": self.move_left
                    , "s": self.move_down
                    , "d": self.move_right
                    , " ": self.player_select
                    , "\n": self.player_select
                }
                input_mapping.get(inp, lambda _: "")(1)

            self.check_winner()

    @staticmethod
    def check_row(game_field, last):
        return (last == game_field).all()

    def check_winner(self):
        if self.game_over:
            return

        last = self.game_field[self.last_move_y, self.last_move_x]

        if last == Players.N0NE.value:
            return

        if self.check_row(self.game_field[self.last_move_y], last):
            self.won(last)
        elif self.check_row(self.game_field.T[self.last_move_x], last):
            self.won(last)
        elif self.check_row(np.diag(self.game_field), last):
            self.won(last)
        elif self.check_row(np.diag(np.fliplr(self.game_field)), last):
            self.won(last)
        else:
            candidates = np.argwhere(self.game_field == Players.N0NE.value)
            if not len(candidates):
                self.tie()
                return

    def tie(self):
        self.game_over = True
        self.move_abs(0, self.field_size - 1)
        self.erika._cursor_back(1)
        self.erika._cursor_down(1)
        self.erika.print_ascii("Tie!\n")
        self.erika.print_ascii("Press any key to exit.")
        self.erika.read()

    def won(self, winner):
        self.game_over = True
        self.move_abs(0, self.field_size - 1)
        self.erika._cursor_back(1)
        self.erika._cursor_down(1)
        self.erika.print_ascii(f"{Players(winner).name} won.\n")
        self.erika.print_ascii("Press any key to exit.")
        self.erika.read()

    def move_abs(self, x, y):
        if self.pos_y < y:
            self.move_down(y - self.pos_y)
        elif self.pos_y > y:
            self.move_up(self.pos_y - y)

        if self.pos_x < x:
            self.move_right(x - self.pos_x)
        elif self.pos_x > x:
            self.move_left(self.pos_x - x)

    def move_up(self, n):
        if self.pos_y - n >= 0:
            self.pos_y -= n
            self.erika._cursor_up((self.cell_height + len(self.horizontal_sep)) * n)

    def move_down(self, n):
        if self.pos_y + n < self.field_size:
            self.pos_y += n
            self.erika._cursor_down((self.cell_height + len(self.horizontal_sep)) * n)

    def move_left(self, n):
        if self.pos_x - n >= 0:
            self.pos_x -= n
            self.erika._cursor_back((self.cell_width + len(self.vertical_sep)) * n)

    def move_right(self, n):
        if self.pos_x + n < self.field_size:
            self.pos_x += n
            self.erika._cursor_forward((self.cell_width + len(self.vertical_sep)) * n)

    def update_last_move(self):
        self.last_move_x = self.pos_x
        self.last_move_y = self.pos_y

    def player_select(self, _):
        if self.game_field[self.pos_y][self.pos_x] == Players.N0NE.value:
            self.make_move(Players.Player1)
            self.turn = Players.Erika.value

    def make_move(self, player):
        self.game_field[self.pos_y, self.pos_x] = player.value
        self.erika.print_ascii(player_chars[player.value])
        self.erika._cursor_back(1)
        self.update_last_move()

    def ai_select(self):
        # TODO: implement different strategies
        candidates = np.argwhere(self.game_field == Players.N0NE.value)
        erikas_choice = candidates[np.random.choice(candidates.shape[0])]

        self.move_abs(erikas_choice[1], erikas_choice[0])
        self.make_move(Players.Erika)
        self.turn = Players.Player1.value


if __name__ == "__main__":
    # Erika("/dev/ttyAMA0")
    with CharacterBasedErikaMock() as erika:
        game = TicTacToe(erika)
