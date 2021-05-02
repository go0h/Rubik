import copy

from rubik.Edge import *
from rubik.Corner import *
import rubik.FaceletCube

C = Corner
E = Edge

BASIC_CUBE_MOVES = {
    "U": [(UBR, 0), (URF, 0), (UFL, 0), (ULB, 0), (DFR, 0), (DLF, 0), (DBL, 0), (DRB, 0),
          (UB, 0), (UR, 0), (UF, 0), (UL, 0), (DR, 0), (DF, 0), (DL, 0), (DB, 0), (FR, 0), (FL, 0), (BL, 0), (BR, 0)],
    "R": [(DFR, 2), (UFL, 0), (ULB, 0), (URF, 1), (DRB, 1), (DLF, 0), (DBL, 0), (UBR, 2),
          (FR, 0), (UF, 0), (UL, 0), (UB, 0), (BR, 0), (DF, 0), (DL, 0), (DB, 0), (DR, 0), (FL, 0), (BL, 0), (UR, 0)],
    "F": [(UFL, 1), (DLF, 2), (ULB, 0), (UBR, 0), (URF, 2), (DFR, 1), (DBL, 0), (DRB, 0),
          (UR, 0), (FL, 1), (UL, 0), (UB, 0), (DR, 0), (FR, 1), (DL, 0), (DB, 0), (UF, 1), (DF, 1), (BL, 0), (BR, 0)],
    "D": [(URF, 0), (UFL, 0), (ULB, 0), (UBR, 0), (DLF, 0), (DBL, 0), (DRB, 0), (DFR, 0),
          (UR, 0), (UF, 0), (UL, 0), (UB, 0), (DF, 0), (DL, 0), (DB, 0), (DR, 0), (FR, 0), (FL, 0), (BL, 0), (BR, 0)],
    "L": [(URF, 0), (ULB, 1), (DBL, 2), (UBR, 0), (DFR, 0), (UFL, 2), (DLF, 1), (DRB, 0),
          (UR, 0), (UF, 0), (BL, 0), (UB, 0), (DR, 0), (DF, 0), (FL, 0), (DB, 0), (FR, 0), (UL, 0), (DL, 0), (BR, 0)],
    "B": [(URF, 0), (UFL, 0), (UBR, 1), (DRB, 2), (DFR, 0), (DLF, 0), (ULB, 2), (DBL, 1),
          (UR, 0), (UF, 0), (UL, 0), (BR, 1), (DR, 0), (DF, 0), (DL, 0), (BL, 1), (FR, 0), (FL, 0), (UB, 1), (DB, 1)]
}


class CubieCube:

    def __init__(self):
        self.corners = [Corner(i) for i in range(8)]
        self.edges = [Edge(i) for i in range(12)]
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
        self.rotate("F")

    def f_r(self) -> None:
        """ Notation - F'
            Вращение передней (синей) стороны против часовой стрелки"""
        self.rotate("F", 3)

    def f2(self) -> None:
        """ Notation - F2
            Вращение передней (синей) стороны на 180 градусов"""
        self.rotate("F", 2)

    def b(self) -> None:
        """ Notation - B
            Вращение задней (оранжевой) стороны по часовой стрелке"""
        self.rotate("B")

    def b_r(self) -> None:
        """ Notation - B'
            Вращение задней (оранжевой) стороны против часовой стрелки"""
        self.rotate("B", 3)

    def b2(self) -> None:
        """ Notation - B2
            Вращение задней (оранжевой) стороны на 180 градусов"""
        self.rotate("B", 2)

    def u(self) -> None:
        """ Notation - U
            Вращение верхней (желтой) стороны по часовой стрелке"""
        self.rotate("U")

    def u_r(self) -> None:
        """ Notation - U'
            Вращение верхней (желтой) стороны против часовой стрелки"""
        self.rotate("U", 3)

    def u2(self) -> None:
        """ Notation - U2
            Вращение верхней (желтой) стороны стороны на 180 градусов"""
        self.rotate("U", 2)

    def d(self) -> None:
        """ Notation - D
            Вращение нижней (белой) стороны по часовой стрелке"""
        self.rotate("D")

    def d_r(self) -> None:
        """ Notation - D'
            Вращение нижней (белой) стороны против часовой стрелки"""
        self.rotate("D", 3)

    def d2(self) -> None:
        """ Notation - D2
            Вращение нижней (белой) стороны стороны на 180 градусов"""
        self.rotate("D", 2)

    def r(self) -> None:
        """ Notation - R
        Вращение правой (красной) стороны по часовой стрелке"""
        self.rotate("R")

    def r_r(self) -> None:
        """ Notation - R'
        Вращение правой (красной) стороны против часовой стрелки"""
        self.rotate("R", 3)

    def r2(self) -> None:
        """ Notation - R2
            Вращение правой (красной) стороны на 180 градусов"""
        self.rotate("R", 2)

    def lf(self) -> None:
        """ Notation - L
        Вращение левой (оранжевой) стороны по часовой стрелке"""
        self.rotate("L")

    def l_r(self) -> None:
        """ Notation - L'
        Вращение левой (оранжевой) стороны против часовой стрелки"""
        self.rotate("L", 3)

    def l2(self) -> None:
        """ Notation - L2
            Вращение левой (оранжевой) стороны на 180 градусов"""
        self.rotate("L", 2)

    def rotate(self, move, count=1):
        m = BASIC_CUBE_MOVES[move]
        for i in range(count):
            c = copy.deepcopy(self.corners)
            e = copy.deepcopy(self.edges)
            for j in range(8):
                t = c[m[j][0]]
                self.corners[j].c = t.c
                self.corners[j].o = (t.o + m[j][1]) % 3

            for j in range(12):
                t = e[m[8 + j][0]]
                self.edges[j].c = t.c
                self.edges[j].o = (t.o + m[8 + j][1]) % 2

    def to_facelet_cube(self):
        facelet = rubik.FaceletCube.FaceletCube()
        for i in range(len(self.corners)):
            facelet.set_corner(i, self.corners[i])
        for i in range(len(self.edges)):
            facelet.set_edge(i, self.edges[i])
        return facelet

    def set_corner(self, position, sides) -> None:
        self.corners[position].set_coordinate(position, sides)

    def set_edge(self, position, sides) -> None:
        self.edges[position].set_coordinate(position, sides)

    def __str__(self) -> str:
        return ", ".join([f"({corner})" for corner in self.corners]) + '\n' + \
               ", ".join([f"({edge})" for edge in self.edges])

    def __eq__(self, other) -> bool:
        return self.edges == other.edges and self.corners == other.corners
