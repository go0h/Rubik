from copy import deepcopy

from rubik.Colors import *
from rubik.Side import Side


class Rubik:

    def __init__(self, size=3):
        """
        Разрешенные действия
        F R U B L D - F' R' U' B' L' D'
        """
        self.size = size
        self.orange = Side(self.size, ORANGE)
        self.green = Side(self.size, GREEN)
        self.white = Side(self.size, WHITE)
        self.blue = Side(self.size, BLUE)
        self.yellow = Side(self.size, YELLOW)
        self.red = Side(self.size, RED)

        self.sides = [self.orange, self.green, self.white, self.blue, self.yellow, self.red]
        self.__moves__ = {
            "F": self.f, "F'": self.f_r, "2F": self.f2,
            "B": self.b, "B'": self.b_r, "2B": self.b2,
            "U": self.u, "U'": self.u_r, "2U": self.u2,
            "D": self.d, "D'": self.d_r, "2D": self.d2,
            "R": self.r, "R'": self.r_r, "2R": self.r2,
            "L": self.lf, "L'": self.l_r, "2L": self.l2
        }

    def move(self, move: str):
        self.__moves__[move]()

    def f(self):
        """ Notation - F
            Вращение красной стороны по часовой стрелке"""
        self.red.rotate_90()

        line = self.white.set_row(self.size - 1, self.green.get_col(self.size - 1, True))
        line = self.blue.set_col(0, line, True)
        line = self.yellow.set_row(0, line)
        self.green.set_col(self.size - 1, line)

    def f_r(self):
        """ Notation - F'
            Вращение красной стороны против часовой стрелки"""
        self.red.rotate_270()

        line = self.white.set_row(self.size - 1, self.blue.get_col(0), True)
        line = self.green.set_col(self.size - 1, line)
        line = self.yellow.set_row(0, line, True)
        self.blue.set_col(0, line)

    def f2(self):
        """ Notation - 2F
            Вращение красной стороны на 180 градусов"""
        self.red.rotate_180()
        line = self.white.set_row(self.size - 1, self.yellow.get_row(0, True), True)
        self.yellow.set_row(0, line)

        line = self.green.set_col(self.size - 1, self.blue.get_col(0, True), True)
        self.blue.set_col(0, line)

    def b(self):
        """ Notation - B
            Вращение оранжевой стороны по часовой стрелке"""
        self.orange.rotate_90()

        line = self.white.set_row(0, self.blue.get_col(self.size - 1), True)
        line = self.green.set_col(0, line)
        line = self.yellow.set_row(self.size - 1, line, True)
        self.blue.set_col(self.size - 1, line)

    def b_r(self):
        """ Notation - B'
            Вращение оранжевой стороны против часовой стрелки"""
        self.orange.rotate_270()

        line = self.white.set_row(0, self.green.get_col(0, True))
        line = self.blue.set_col(self.size - 1, line, True)
        line = self.yellow.set_row(self.size - 1, line)
        self.green.set_col(0, line)

    def b2(self):
        """ Notation - 2B
            Вращение оранжевой стороны на 180 градусов"""
        self.orange.rotate_180()

        line = self.white.set_row(0, self.yellow.get_row(self.size - 1, True), True)
        self.yellow.set_row(self.size - 1, line)
        line = self.blue.set_col(self.size - 1, self.green.get_col(0, True), True)
        self.green.set_col(0, line)

    def u(self):
        """ Notation - U
            Вращение белой стороны по часовой стрелке"""
        self.white.rotate_90()

        line = self.orange.set_row(0, self.green.get_row(0))
        line = self.blue.set_row(0, line)
        line = self.red.set_row(0, line)
        self.green.set_row(0, line)

    def u_r(self):
        """ Notation - U'
            Вращение белой стороны против часовой стрелки"""
        self.white.rotate_270()

        line = self.orange.set_row(0, self.blue.get_row(0))
        line = self.green.set_row(0, line)
        line = self.red.set_row(0, line)
        self.blue.set_row(0, line)

    def u2(self):
        """ Notation - 2U
            Вращение белой стороны стороны на 180 градусов"""
        self.white.rotate_180()

        line = self.orange.set_row(0, self.red.get_row(0))
        self.red.set_row(0, line)
        line = self.green.set_row(0, self.blue.get_row(0))
        self.blue.set_row(0, line)

    def d(self):
        """ Notation - D
            Вращение белой стороны по часовой стрелке"""
        self.white.rotate_270()

        line = self.orange.set_row(self.size - 1, self.blue.get_row(self.size - 1))
        line = self.green.set_row(self.size - 1, line)
        line = self.red.set_row(self.size - 1, line)
        self.blue.set_row(self.size - 1, line)

    def d_r(self):
        """ Notation - D'
            Вращение желтой стороны против часовой стрелки"""
        self.yellow.rotate_270()

        line = self.orange.set_row(self.size - 1, self.green.get_row(self.size - 1))
        line = self.blue.set_row(self.size - 1, line)
        line = self.red.set_row(self.size - 1, line)
        self.green.set_row(self.size - 1, line)

    def d2(self):
        """ Notation - 2D
            Вращение желтой стороны стороны на 180 градусов"""
        self.yellow.rotate_180()

        line = self.orange.set_row(self.size - 1, self.red.get_row(self.size - 1))
        self.red.set_row(self.size - 1, line)
        line = self.green.set_row(self.size - 1, self.blue.get_row(self.size - 1))
        self.blue.set_row(self.size - 1, line)

    def r(self):
        """ Notation - R
        Вращение синей стороны по часовой стрелке"""
        self.blue.rotate_90()

        line = self.white.set_col(self.size - 1, self.red.get_col(self.size - 1), True)
        line = self.orange.set_col(0, line, True)
        line = self.yellow.set_col(self.size - 1, line)
        self.red.set_col(self.size - 1, line)

    def r_r(self):
        """ Notation - R'
        Вращение синей стороны против часовой стрелки"""
        self.blue.rotate_270()

        line = self.white.set_col(self.size - 1, self.orange.get_col(0, True))
        line = self.red.set_col(self.size - 1, line)
        line = self.yellow.set_col(self.size - 1, line, True)
        self.orange.set_col(0, line)

    def r2(self):
        """ Notation - 2R
            Вращение синей стороны на 180 градусов"""
        self.blue.rotate_180()

        line = self.white.set_col(self.size - 1, self.yellow.get_col(self.size - 1))
        self.yellow.set_col(self.size - 1, line)
        line = self.orange.set_col(0, self.red.get_col(self.size - 1, True), True)
        self.red.set_col(self.size - 1, line)

    def lf(self):
        """ Notation - L
        Вращение зеленой стороны по часовой стрелке"""
        self.green.rotate_90()

        line = self.white.set_col(0, self.orange.get_col(self.size - 1, True))
        line = self.red.set_col(0, line)
        line = self.yellow.set_col(0, line, True)
        self.orange.set_col(self.size - 1, line)

    def l_r(self):
        """ Notation - L'
        Вращение зеленой стороны против часовой стрелки"""
        self.green.rotate_270()

        line = self.white.set_col(0, self.red.get_col(0), True)
        line = self.orange.set_col(self.size - 1, line, True)
        line = self.yellow.set_col(0, line)
        self.red.set_col(0, line)

    def l2(self):
        """ Notation - 2L
            Вращение зеленой стороны на 180 градусов"""
        self.green.rotate_180()

        line = self.white.set_col(0, self.yellow.get_col(0))
        self.yellow.set_col(0, line)

        line = self.red.set_col(0, self.orange.get_col(self.size - 1, True), True)
        self.orange.set_col(self.size - 1, line)

    def __str__(self):
        """
        Печатает кубик в цвете в развернутом виде
             |  UP |
        |LEFT|FRONT|RIGHT|BACK|
             |DOWN |
        """
        res = ""
        for line in self.white.side:
            res += "  " * self.size + ''.join(colors[i] for i in line) + colors[DROP] + "\n"

        straight_sides = [self.green, self.red, self.blue, self.orange]

        for i in range(self.size):
            temp = ""
            for side in straight_sides:
                temp += ''.join(colors[j] for j in side.side[i]) + colors[DROP]
            res += temp + "\n" + colors[DROP]

        for line in self.yellow.side:
            res += "  " * self.size + ''.join(colors[i] for i in line) + colors[DROP] + "\n"

        return res

    def __copy__(self):
        return deepcopy(self)

    def __eq__(self, other):
        if self.size != other.size:
            return False
        for i in range(6):
            if self.sides[i] != other.sides[i]:
                return False
        return True
