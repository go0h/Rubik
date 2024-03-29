import copy
import rubik.FaceletCube as fc
import rubik.Utils as u
from rubik.Edge import *
from rubik.Corner import *
from math import comb  # биномиальный коэффициент

# приращение координаты и ориентации угла путем вращения
BASIC_CORNER_MOVES = {
    U: [(UBR, 0), (URF, 0), (UFL, 0), (ULB, 0), (DFR, 0), (DLF, 0), (DBL, 0), (DRB, 0)],
    R: [(DFR, 2), (UFL, 0), (ULB, 0), (URF, 1), (DRB, 1), (DLF, 0), (DBL, 0), (UBR, 2)],
    F: [(UFL, 1), (DLF, 2), (ULB, 0), (UBR, 0), (URF, 2), (DFR, 1), (DBL, 0), (DRB, 0)],
    D: [(URF, 0), (UFL, 0), (ULB, 0), (UBR, 0), (DLF, 0), (DBL, 0), (DRB, 0), (DFR, 0)],
    L: [(URF, 0), (ULB, 1), (DBL, 2), (UBR, 0), (DFR, 0), (UFL, 2), (DLF, 1), (DRB, 0)],
    B: [(URF, 0), (UFL, 0), (UBR, 1), (DRB, 2), (DFR, 0), (DLF, 0), (ULB, 2), (DBL, 1)]
}

# приращение координаты и ориентации ребра путем вращения
BASIC_EDGE_MOVES = {
    U: [(UB, 0), (UR, 0), (UF, 0), (UL, 0), (DR, 0), (DF, 0), (DL, 0), (DB, 0), (FR, 0), (FL, 0), (BL, 0), (BR, 0)],
    R: [(FR, 0), (UF, 0), (UL, 0), (UB, 0), (BR, 0), (DF, 0), (DL, 0), (DB, 0), (DR, 0), (FL, 0), (BL, 0), (UR, 0)],
    F: [(UR, 0), (FL, 1), (UL, 0), (UB, 0), (DR, 0), (FR, 1), (DL, 0), (DB, 0), (UF, 1), (DF, 1), (BL, 0), (BR, 0)],
    D: [(UR, 0), (UF, 0), (UL, 0), (UB, 0), (DF, 0), (DL, 0), (DB, 0), (DR, 0), (FR, 0), (FL, 0), (BL, 0), (BR, 0)],
    L: [(UR, 0), (UF, 0), (BL, 0), (UB, 0), (DR, 0), (DF, 0), (FL, 0), (DB, 0), (FR, 0), (UL, 0), (DL, 0), (BR, 0)],
    B: [(UR, 0), (UF, 0), (UL, 0), (BR, 1), (DR, 0), (DF, 0), (DL, 0), (BL, 1), (FR, 0), (FL, 0), (UB, 1), (DB, 1)]
}


class CubieCube:
    """http://kociemba.org/math/cubielevel.htm"""
    def __init__(self, corners=None, edges=None):
        if corners is None:
            self.corners = [Corner(i) for i in range(8)]
        else:
            self.corners = copy.deepcopy(corners)
        if edges is None:
            self.edges = [Edge(i) for i in range(12)]
        else:
            self.edges = copy.deepcopy(edges)
        self.__str_moves__ = {
            "U": self.u, "U2": self.u2, "U'": self.u_r,
            "R": self.r, "R2": self.r2, "R'": self.r_r,
            "F": self.f, "F2": self.f2, "F'": self.f_r,
            "D": self.d, "D2": self.d2, "D'": self.d_r,
            "L": self.lf, "L2": self.l2, "L'": self.l_r,
            "B": self.b, "B2": self.b2, "B'": self.b_r,
        }
        self.__moves__ = [
            self.u, self.u2, self.u_r,
            self.r, self.r2, self.r_r,
            self.f, self.f2, self.f_r,
            self.d, self.d2, self.d_r,
            self.lf, self.l2, self.l_r,
            self.b, self.b2, self.b_r
        ]

    def str_move(self, move: str) -> None:
        """Разрешенные действия F R U B L D - F' R' U' B' L' D'"""
        self.__str_moves__[move]()

    def move(self, move: int) -> None:
        """Разрешенные действия 0-17"""
        self.__moves__[move]()

    def apply_moves(self, moves) -> None:
        for move in moves:
            if move in u.MOVES:
                self.move(move)
            else:
                raise ValueError(f"Can't recognize move {move}. Allowed moves in range 0-17")

    def scramble(self, scramble: str) -> None:
        allowed_moves = self.__str_moves__.keys()
        if len(scramble.strip()) == 0:
            return
        moves = scramble.strip().split(" ")
        if len(moves) == 0:
            return
        for move in moves:
            if move in allowed_moves:
                self.str_move(move)
            else:
                raise ValueError(f"Can't recognize move {move}")

    def f(self) -> None:
        """ Notation - F
        Вращение передней (синей) стороны по часовой стрелке"""
        self.rotate(F)

    def f_r(self) -> None:
        """ Notation - F'
            Вращение передней (синей) стороны против часовой стрелки"""
        self.rotate(F, 3)

    def f2(self) -> None:
        """ Notation - F2
            Вращение передней (синей) стороны на 180 градусов"""
        self.rotate(F, 2)

    def b(self) -> None:
        """ Notation - B
            Вращение задней (оранжевой) стороны по часовой стрелке"""
        self.rotate(B)

    def b_r(self) -> None:
        """ Notation - B'
            Вращение задней (оранжевой) стороны против часовой стрелки"""
        self.rotate(B, 3)

    def b2(self) -> None:
        """ Notation - B2
            Вращение задней (оранжевой) стороны на 180 градусов"""
        self.rotate(B, 2)

    def u(self) -> None:
        """ Notation - U
            Вращение верхней (желтой) стороны по часовой стрелке"""
        self.rotate(U)

    def u_r(self) -> None:
        """ Notation - U'
            Вращение верхней (желтой) стороны против часовой стрелки"""
        self.rotate(U, 3)

    def u2(self) -> None:
        """ Notation - U2
            Вращение верхней (желтой) стороны стороны на 180 градусов"""
        self.rotate(U, 2)

    def d(self) -> None:
        """ Notation - D
            Вращение нижней (белой) стороны по часовой стрелке"""
        self.rotate(D)

    def d_r(self) -> None:
        """ Notation - D'
            Вращение нижней (белой) стороны против часовой стрелки"""
        self.rotate(D, 3)

    def d2(self) -> None:
        """ Notation - D2
            Вращение нижней (белой) стороны стороны на 180 градусов"""
        self.rotate(D, 2)

    def r(self) -> None:
        """ Notation - R
        Вращение правой (красной) стороны по часовой стрелке"""
        self.rotate(R)

    def r_r(self) -> None:
        """ Notation - R'
        Вращение правой (красной) стороны против часовой стрелки"""
        self.rotate(R, 3)

    def r2(self) -> None:
        """ Notation - R2
            Вращение правой (красной) стороны на 180 градусов"""
        self.rotate(R, 2)

    def lf(self) -> None:
        """ Notation - L
        Вращение левой (оранжевой) стороны по часовой стрелке"""
        self.rotate(L)

    def l_r(self) -> None:
        """ Notation - L'
        Вращение левой (оранжевой) стороны против часовой стрелки"""
        self.rotate(L, 3)

    def l2(self) -> None:
        """ Notation - L2
            Вращение левой (оранжевой) стороны на 180 градусов"""
        self.rotate(L, 2)

    def rotate(self, move, count=1):
        c_m = BASIC_CORNER_MOVES[move]
        e_m = BASIC_EDGE_MOVES[move]
        for i in range(count):
            c = copy.deepcopy(self.corners)
            e = copy.deepcopy(self.edges)
            for j in range(8):
                t = c[c_m[j][0]]
                self.corners[j].c = t.c
                self.corners[j].o = (t.o + c_m[j][1]) % 3

            for j in range(12):
                t = e[e_m[j][0]]
                self.edges[j].c = t.c
                self.edges[j].o = (t.o + e_m[j][1]) % 2

    def solved(self) -> bool:
        """Комментарии излишни"""
        i = 0
        for corner in self.corners:
            if corner.c != i or corner.o != 0:
                return False
            i += 1
        i = 0
        for edge in self.edges:
            if edge.c != i or edge.o != 0:
                return False
            i += 1
        return True

    def to_facelet_cube(self):
        facelet = fc.FaceletCube()
        for i in range(len(self.corners)):
            facelet.set_corner(i, self.corners[i])
        for i in range(len(self.edges)):
            facelet.set_edge(i, self.edges[i])
        return facelet

    def set_corner(self, position, sides) -> None:
        self.corners[position].set_coordinate(position, sides)

    def set_edge(self, position, sides) -> None:
        self.edges[position].set_coordinate(position, sides)

    def corner_multiply(self, other):
        corners = [Corner(0) for _ in range(8)]
        ori = 0
        for i in range(8):
            # (A*B)(x).c = A(B(x).c).c
            corners[i].c = self.corners[other.corners[i].c].c
            # (A*B)(x).o = A(B(x).c).o + B(x).o
            ori_a = self.corners[other.corners[i].c].o
            ori_b = other.corners[i].o
            if ori_a < 3 and ori_b < 3:
                ori = (ori_a + ori_b) % 3

            # if we use reflections at the LR-plane in symmetry operations
            elif ori_a < 3 <= ori_b:  # cube b is in a mirrored state
                ori = ori_a + ori_b
                if ori >= 6:
                    ori -= 3  # the composition also is in a mirrored state
            elif ori_a >= 3 > ori_b:  # cube a is in a mirrored state
                ori = ori_a - ori_b
                if ori < 3:
                    ori += 3  # the composition is a mirrored cube
            elif ori_a >= 3 and ori_b >= 3:  # if both cubes are in mirrored states
                ori = ori_a - ori_b
                if ori < 0:
                    ori += 3  # the composition is a regular cube
            corners[i].o = ori
        self.corners = corners

    def edge_multiply(self, other):
        # (A*B)(x).c = A(B(x).c).c
        edges = [Edge(0) for _ in range(12)]
        for i in range(12):
            # (A*B)(x).c = A(B(x).c).c
            edges[i].c = self.edges[other.edges[i].c].c
            # (A*B)(x).o = A(B(x).c).o + B(x).o
            edges[i].o = (self.edges[other.edges[i].c].o + other.edges[i].o) % 2
        self.edges = edges

    def multiply(self, other):
        self.corner_multiply(other)
        self.edge_multiply(other)

    def get_ud_slice_coord(self):
        """http://kociemba.org/math/UDSliceCoord.htm
            Ориентация чертырех средних ребер UD-разреза (FR, FL, BL, BR) без использования их перестановок.
            Фаза 1: от 0 до 495
            Фаза 2: 0"""
        res, n = 0, 0
        for i in range(BR, UR - 1, -1):
            if FR <= self.edges[i].c <= BR:
                res += comb(11 - i, n + 1)
                n += 1
        return res

    def __edges_coord__(self, start, end):
        from collections import deque
        res, n = 0, 0
        edges = deque(self.edges[:])
        if start == UR or start == DR:
            edges.rotate(4)
        for i in range(BR, UR - 1, -1):
            if start <= edges[i].c <= end:
                res += comb(11 - i, n + 1)
                n += 1
        return res

    def get_corners_twist(self):
        """Ориентация углов описывается числом от 0 до 2186 (3^7 - 1)"""
        res = 0
        for i in range(7):
            res = 3 * res + self.corners[i].o
        return res

    def get_edges_flip(self):
        """Ориентация ребер описывается числом от 0 до 2047 (2^11 - 1)"""
        res = 0
        for i in range(11):
            res = 2 * res + self.edges[i].o
        return res

    def get_ud_slice_sorted(self):
        """Get the permutation and location of the UD-slice edges FR,FL,BL and BR.
            0 <= slice_sorted < 11880 in phase 1, 0 <= slice_sorted < 24 in phase 2, slice_sorted = 0 for solved cube."""
        a = x = 0
        edge4 = [0] * 4
        # First compute the index a < (12 choose 4) and the permutation array perm.
        for j in range(BR, UR - 1, -1):
            if FR <= self.edges[j].c <= BR:
                a += comb(11 - j, x + 1)
                edge4[3 - x] = self.edges[j].c
                x += 1
        # Then compute the index b < 4! for the permutation in edge4
        b = 0
        for j in range(3, 0, -1):
            k = 0
            while edge4[j] != j + 8:
                u.rotate_left(edge4, 0, j)
                k += 1
            b = (j + 1)*b + k
        return 24*a + b

    # # ДЛЯ ПРОВЕРКИ
    # def get_ud_slice_sorted(self):
    #     j = 0
    #     pos = [0 for _ in range(4)]
    #     for i in range(UR, BR + 1):
    #         if self.edges[i].c in [FR, FL, BL, BR]:
    #             pos[j] = self.edges[i].c
    #             j += 1
    #     c_res = 0
    #     for j in range(3, 0, -1):
    #         s = 0
    #         for k in range(j - 1, -1, -1):
    #             if pos[k] > pos[j]:
    #                 s += 1
    #         c_res = (c_res + s) * j
    #     return 24 * self.get_ud_slice_coord() + c_res

    # def __get_edges__(self, start, end):
    #     j = 0
    #     pos = [0 for _ in range(4)]
    #     edges = list(range(start, end + 1))
    #     for i in range(UR, BR + 1):
    #         if self.edges[i].c in edges:
    #             pos[j] = self.edges[i].c
    #             j += 1
    #     c_res = 0
    #     for j in range(3, 0, -1):
    #         s = 0
    #         for k in range(j - 1, -1, -1):
    #             if pos[k] > pos[j]:
    #                 s += 1
    #         c_res = (c_res + s) * j
    #     return 24 * self.__edges_coord__(start, end) + c_res

    def get_corners(self):
        """http://kociemba.org/math/coordlevel.htm
           Перестановки 8 углов
           Фаза 1,2: от 0 до 40320
           Решенный куб: 0"""
        # res = 0
        # for i in range(DRB, URF, -1):
        #     s = 0
        #     for j in range(i - 1, URF - 1, -1):
        #         if self.corners[j].c > self.corners[i].c:
        #             s += 1
        #     res = (res + s) * i
        # return res
        perm = list([corner.c for corner in self.corners])  # duplicate cp
        b = 0
        for j in range(DRB, URF, -1):
            k = 0
            while perm[j] != j:
                u.rotate_left(perm, 0, j)
                k += 1
            b = (j + 1) * b + k
        return b

    def get_ud_edges(self):
        """http://kociemba.org/math/coordlevel.htm
           Перестановки 8 ребер (верхних и нижних)
           Фаза 1: не определено
           Фаза 2: от 0 до 40320
           Решенный куб: 0"""
        # res = 0
        # for i in range(DB, UR, -1):
        #     s = 0
        #     for j in range(i - 1, UR - 1, -1):
        #         if self.edges[j].c > self.edges[i].c:
        #             s += 1
        #     res = (res + s) * i
        # return res
        perm = list([edge.c for edge in self.edges[0:8]])  # duplicate first 8 elements of ep
        b = 0
        for j in range(DB, UR, -1):
            k = 0
            while perm[j] != j:
                u.rotate_left(perm, 0, j)
                k += 1
            b = (j + 1) * b + k
        return b

    def __mul__(self, other):
        self.corner_multiply(other)
        self.edge_multiply(other)

    def __str__(self) -> str:
        return ", ".join([f"({corner})" for corner in self.corners]) + '\n' + \
               ", ".join([f"({edge})" for edge in self.edges])

    def __eq__(self, other) -> bool:
        return self.edges == other.edges and self.corners == other.corners
