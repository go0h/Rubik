from copy import deepcopy

from rubik.Colors import colors, B, L, U, R, D, F, NONE
from rubik.Side import Side
from rubik.Corner import CORNERS_SIDES
from rubik.Edge import EDGE_SIDES
import rubik.CubieCube as cc


class FaceletCube:
    """http://kociemba.org/math/faceletlevel.htm"""
    def __init__(self, size=3):
        self.size = size
        self.back = Side(self.size, B)
        self.left = Side(self.size, L)
        self.up = Side(self.size, U)
        self.right = Side(self.size, R)
        self.down = Side(self.size, D)
        self.front = Side(self.size, F)

        self.sides = [self.back, self.left, self.up, self.right, self.down, self.front]
        self.__moves__ = {
            "F": self.f, "F'": self.f_r, "F2": self.f2,
            "B": self.b, "B'": self.b_r, "B2": self.b2,
            "U": self.u, "U'": self.u_r, "U2": self.u2,
            "D": self.d, "D'": self.d_r, "D2": self.d2,
            "R": self.r, "R'": self.r_r, "R2": self.r2,
            "L": self.lf, "L'": self.l_r, "L2": self.l2
        }

    def move(self, move: str) -> None:
        """Разрешенные действия F R U B L D - F' R' U' B' L' D'"""
        self.__moves__[move]()

    def scramble(self, scramble: str) -> None:
        allowed_moves = self.__moves__.keys()
        for move in scramble.strip().split(" "):
            if move in allowed_moves:
                self.move(move)
            else:
                raise ValueError(f"Can't recognize move {move}")

    def f(self) -> None:
        """ Notation - F
            Вращение передней (синей) стороны по часовой стрелке"""
        self.front.rotate_90()

        line = self.up.set_row(self.size - 1, self.left.get_col(self.size - 1, True))
        line = self.right.set_col(0, line, True)
        line = self.down.set_row(0, line)
        self.left.set_col(self.size - 1, line)

    def f_r(self) -> None:
        """ Notation - F'
            Вращение передней (синей) стороны против часовой стрелки"""
        self.front.rotate_270()

        line = self.up.set_row(self.size - 1, self.right.get_col(0), True)
        line = self.left.set_col(self.size - 1, line)
        line = self.down.set_row(0, line, True)
        self.right.set_col(0, line)

    def f2(self) -> None:
        """ Notation - F2
            Вращение передней (синей) стороны на 180 градусов"""
        self.front.rotate_180()

        line = self.up.set_row(self.size - 1, self.down.get_row(0, True), True)
        self.down.set_row(0, line)
        line = self.left.set_col(self.size - 1, self.right.get_col(0, True), True)
        self.right.set_col(0, line)

    def b(self) -> None:
        """ Notation - B
            Вращение задней (оранжевой) стороны по часовой стрелке"""
        self.back.rotate_90()

        line = self.up.set_row(0, self.right.get_col(self.size - 1), True)
        line = self.left.set_col(0, line)
        line = self.down.set_row(self.size - 1, line, True)
        self.right.set_col(self.size - 1, line)

    def b_r(self) -> None:
        """ Notation - B'
            Вращение задней (оранжевой) стороны против часовой стрелки"""
        self.back.rotate_270()

        line = self.up.set_row(0, self.left.get_col(0, True))
        line = self.right.set_col(self.size - 1, line, True)
        line = self.down.set_row(self.size - 1, line)
        self.left.set_col(0, line)

    def b2(self) -> None:
        """ Notation - B2
            Вращение задней (оранжевой) стороны на 180 градусов"""
        self.back.rotate_180()

        line = self.up.set_row(0, self.down.get_row(self.size - 1, True), True)
        self.down.set_row(self.size - 1, line)
        line = self.right.set_col(self.size - 1, self.left.get_col(0, True), True)
        self.left.set_col(0, line)

    def u(self) -> None:
        """ Notation - U
            Вращение верхней (желтой) стороны по часовой стрелке"""
        self.up.rotate_90()

        line = self.back.set_row(0, self.left.get_row(0))
        line = self.right.set_row(0, line)
        line = self.front.set_row(0, line)
        self.left.set_row(0, line)

    def u_r(self) -> None:
        """ Notation - U'
            Вращение верхней (желтой) стороны против часовой стрелки"""
        self.up.rotate_270()

        line = self.back.set_row(0, self.right.get_row(0))
        line = self.left.set_row(0, line)
        line = self.front.set_row(0, line)
        self.right.set_row(0, line)

    def u2(self) -> None:
        """ Notation - U2
            Вращение верхней (желтой) стороны стороны на 180 градусов"""
        self.up.rotate_180()

        line = self.back.set_row(0, self.front.get_row(0))
        self.front.set_row(0, line)
        line = self.left.set_row(0, self.right.get_row(0))
        self.right.set_row(0, line)

    def d(self) -> None:
        """ Notation - D
            Вращение нижней (белой) стороны по часовой стрелке"""
        self.down.rotate_90()

        line = self.back.set_row(self.size - 1, self.right.get_row(self.size - 1))
        line = self.left.set_row(self.size - 1, line)
        line = self.front.set_row(self.size - 1, line)
        self.right.set_row(self.size - 1, line)

    def d_r(self) -> None:
        """ Notation - D'
            Вращение нижней (белой) стороны против часовой стрелки"""
        self.down.rotate_270()

        line = self.back.set_row(self.size - 1, self.left.get_row(self.size - 1))
        line = self.right.set_row(self.size - 1, line)
        line = self.front.set_row(self.size - 1, line)
        self.left.set_row(self.size - 1, line)

    def d2(self) -> None:
        """ Notation - D2
            Вращение нижней (белой) стороны стороны на 180 градусов"""
        self.down.rotate_180()

        line = self.back.set_row(self.size - 1, self.front.get_row(self.size - 1))
        self.front.set_row(self.size - 1, line)
        line = self.left.set_row(self.size - 1, self.right.get_row(self.size - 1))
        self.right.set_row(self.size - 1, line)

    def r(self) -> None:
        """ Notation - R
        Вращение правой (красной) стороны по часовой стрелке"""
        self.right.rotate_90()

        line = self.up.set_col(self.size - 1, self.front.get_col(self.size - 1), True)
        line = self.back.set_col(0, line, True)
        line = self.down.set_col(self.size - 1, line)
        self.front.set_col(self.size - 1, line)

    def r_r(self) -> None:
        """ Notation - R'
        Вращение правой (красной) стороны против часовой стрелки"""
        self.right.rotate_270()

        line = self.up.set_col(self.size - 1, self.back.get_col(0, True))
        line = self.front.set_col(self.size - 1, line)
        line = self.down.set_col(self.size - 1, line, True)
        self.back.set_col(0, line)

    def r2(self) -> None:
        """ Notation - R2
            Вращение правой (красной) стороны на 180 градусов"""
        self.right.rotate_180()

        line = self.up.set_col(self.size - 1, self.down.get_col(self.size - 1))
        self.down.set_col(self.size - 1, line)
        line = self.back.set_col(0, self.front.get_col(self.size - 1, True), True)
        self.front.set_col(self.size - 1, line)

    def lf(self) -> None:
        """ Notation - L
        Вращение левой (оранжевой) стороны по часовой стрелке"""
        self.left.rotate_90()

        line = self.up.set_col(0, self.back.get_col(self.size - 1, True))
        line = self.front.set_col(0, line)
        line = self.down.set_col(0, line, True)
        self.back.set_col(self.size - 1, line)

    def l_r(self) -> None:
        """ Notation - L'
        Вращение левой (оранжевой) стороны против часовой стрелки"""
        self.left.rotate_270()

        line = self.up.set_col(0, self.front.get_col(0), True)
        line = self.back.set_col(self.size - 1, line, True)
        line = self.down.set_col(0, line)
        self.front.set_col(0, line)

    def l2(self) -> None:
        """ Notation - L2
            Вращение левой (оранжевой) стороны на 180 градусов"""
        self.left.rotate_180()

        line = self.up.set_col(0, self.down.get_col(0))
        self.down.set_col(0, line)

        line = self.front.set_col(0, self.back.get_col(self.size - 1, True), True)
        self.back.set_col(self.size - 1, line)

    def solved(self) -> bool:
        """Checks if cube is solved"""
        for side in self.sides:
            if not side.solved():
                return False
        return True

    def to_string(self) -> str:
        res = ""
        for side in self.sides:
            res += side.to_string()
        return res

    def __str__(self) -> str:
        """
        Print color Facelet Cube to STDOUT
             |  UP |
        |LEFT|FRONT|RIGHT|BACK|
             |DOWN |
        """
        res = ""
        for line in self.up.side:
            res += "  " * self.size + ''.join(colors[i] for i in line) + colors[NONE] + "\n"

        straight_sides = [self.left, self.front, self.right, self.back]

        for i in range(self.size):
            temp = ""
            for side in straight_sides:
                temp += ''.join(colors[j] for j in side.side[i]) + colors[NONE]
            res += temp + "\n" + colors[NONE]

        for line in self.down.side:
            res += "  " * self.size + ''.join(colors[i] for i in line) + colors[NONE] + "\n"

        return res

    def __copy__(self):
        return deepcopy(self)

    def __eq__(self, other) -> bool:
        if self.size != other.size:
            return False
        for i in range(6):
            if self.sides[i] != other.sides[i]:
                return False
        return True

    def set_corner(self, cur_pos, corner) -> None:
        c1, c2, c3 = corner.get_coordinates(cur_pos)
        s1, s2, s3 = CORNERS_SIDES[cur_pos]
        self.sides[s1].set_face(c1)
        self.sides[s2].set_face(c2)
        self.sides[s3].set_face(c3)

    def set_edge(self, cur_pos, edge) -> None:
        c1, p2 = edge.get_coordinates(cur_pos)
        s1, s2 = EDGE_SIDES[cur_pos]
        self.sides[s1].set_face(c1)
        self.sides[s2].set_face(p2)

    def to_cubie_cube(self):
        cubie = cc.CubieCube()
        for i in range(8):
            cubie.set_corner(i, self.sides)
        for i in range(12):
            cubie.set_edge(i, self.sides)
        return cubie
