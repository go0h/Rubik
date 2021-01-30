from rubik.Colors import *
from rubik.Utils import rotate_side


class Rubik:

    def __init__(self, side=3):
        """
        Разрешенные действия
        F R U B L D - F' R' U' B' L' D'
        """
        self.side = side

        self.sides = {
            ORANGE: [[ORANGE for _ in range(self.side)] for _ in range(self.side)],
            GREEN: [[GREEN for _ in range(self.side)] for _ in range(self.side)],
            WHITE: [[WHITE for _ in range(self.side)] for _ in range(self.side)],
            BLUE: [[BLUE for _ in range(self.side)] for _ in range(self.side)],
            YELLOW: [[YELLOW for _ in range(self.side)] for _ in range(self.side)],
            RED: [[RED for _ in range(self.side)] for _ in range(self.side)]
        }

    def rotate(self, side=RED, reverse=False):

        self.sides[side] = rotate_side(self.sides[side])

        row = self.get_shift_row(side, left[side])
        row = self.shift_row(side, up[side], row)
        row = self.shift_row(side, opposite[left[side]], row)
        row = self.shift_row(side, opposite[up[side]], row)
        self.shift_row(side, left[side], row)

    def shift_row(self, side, shift_side, row):

        new_row = self.get_shift_row(side, shift_side)

        if shift_side == left[side]:
            for i in range(self.side):
                self.sides[shift_side][i][self.side - 1] = row[i]
        elif shift_side == opposite[left[side]]:
            for i in range(self.side):
                self.sides[shift_side][i][0] = row[i]
        elif shift_side == up[side]:
            self.sides[shift_side][self.side - 1] = row
        elif shift_side == opposite[up[side]]:
            self.sides[shift_side][0] = row
        return new_row

    def get_shift_row(self, side, shift_side):

        if shift_side == left[side]:
            return [self.sides[shift_side][self.side - 1][i] for i in range(self.side)]
        elif shift_side == opposite[left[side]]:
            return [self.sides[shift_side][i][0] for i in range(self.side)]
        elif shift_side == up[side]:
            return self.sides[shift_side][self.side - 1]
        elif shift_side == opposite[up[side]]:
            return self.sides[shift_side][0]
        return []

    def __str__(self):
        """
        Печатает кубик в цвете в развернутом виде
             |  UP |
        |LEFT|FRONT|RIGHT|BACK|
             |DOWN |
        """
        res = ""
        for line in self.sides[WHITE]:
            res += "  " * self.side + ''.join(colors[i] for i in line) + colors[DROP] + "\n"

        straight_sides = [self.sides[GREEN], self.sides[RED],
                          self.sides[BLUE], self.sides[ORANGE]]

        for i in range(self.side):
            temp = ""
            for side in straight_sides:
                temp += ''.join(colors[j] for j in side[i]) + colors[DROP]
            res += temp + "\n" + colors[DROP]

        for line in self.sides[YELLOW]:
            res += "  " * self.side + ''.join(colors[i] for i in line) + colors[DROP] + "\n"

        return res