from enum import Enum
from math import ceil

import numpy as np

sys
from erika.erika import Erika


class Players(Enum):
    Erika = 1
    Player1 = 2
    N0NE = 0


player_chars = [" ", "o", "x"]


# from erika import erika

def create_field(field_size=3, cell_width=3, cell_height=1, vertical_sep="#", horizontal_sep="#"):
    cell = " " * cell_width
    row = vertical_sep.join(list([cell] * field_size))
    horizontal_line = "\n" + (horizontal_sep * len(row)) + "\n"
    result = horizontal_line.join(list(["\n".join([row] * cell_height)] * field_size))
    return result


class TicTacToe:

    def __init__(self):

        self.field_size = 3
        self.cell_width = 3
        self.cell_height = 1
        self.vertical_sep = "|"
        self.horizontal_sep = "-"
        assert self.field_size % 2 == 1
        self.pos_y = self.pos_x = self.field_size // 2

        self.game_field = np.zeros((self.field_size, self.field_size), dtype=np.uint8)

        self.game_over = False
        self.turn = -1

        self.erika = Erika()
        # disable keyboard echo
        self.erika.set_keyboard_echo(False)

        # print field
        ascii_field = create_field(self.field_size, cell_height=self.cell_height
                                   , cell_width=self.cell_width, vertical_sep=self.vertical_sep
                                   , horizontal_sep=self.horizontal_sep)
        print(ascii_field)
        self.erika.print_ascii(ascii_field)

        # move to center / init position
        self.erika._cursor_back(ceil(self.cell_width / 2))
        self.move_left(self.pos_x)

        self.erika._cursor_up(self.cell_height // 2)
        self.move_up(self.pos_y)

        self.start_game()

    def start_game(self):
        self.turn = np.random.randint(1, 3)
        self.game_over = False

        while not self.game_over:
            if self.turn == 1:
                self.ai_select()
            else:
                inp = erika.read()
                input_mapping = {
                    "w": self.move_up
                    , "a": self.move_left
                    , "s": self.move_down
                    , "d": self.move_right
                    , " ": self.player_select
                    , "\n": self.player_select
                }
                input_mapping[inp](1)
            self.check_winner()

    def check_winner(self):
        empty_fields = np.argwhere(self.game_field == Players.N0NE.value)

        for row in self.game_field:
            for col in row:

        if len(empty_fields):

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

    def player_select(self):
        if self.game_field[self.pos_y][self.pos_x] == Players.N0NE.value:
            self.game_field[self.pos_y][self.pos_x] = Players.Player1
            self.erika.print_ascii(player_chars[Players.Player1.value])
            self.erika._cursor_back(1)

    def ai_select(self):
        candidates = np.argwhere(self.game_field == Players.N0NE.value)
        erikas_choice = np.random.choice(candidates)

    if __name__ == "__main__":
        pass
