
import rubik.FaceletCube as fc
from rubik.Utils import rotate_left, rotate_right, MOVES, MOVES_S, get_random_moves, get_random_moves_2
from rubik.Edge import *
from rubik.Corner import *
from math import comb  # биномиальный коэффициент

# приращение координаты и ориентации углов и ребер путем вращения
CUBIE_MOVE = [
    # U
    [[(UBR, 0), (URF, 0), (UFL, 0), (ULB, 0), (DFR, 0), (DLF, 0), (DBL, 0), (DRB, 0)],
     [(UB, 0), (UR, 0), (UF, 0), (UL, 0), (DR, 0), (DF, 0), (DL, 0), (DB, 0), (FR, 0), (FL, 0), (BL, 0), (BR, 0)]],
    # U2
    [[(ULB, 0), (UBR, 0), (URF, 0), (UFL, 0), (DFR, 0), (DLF, 0), (DBL, 0), (DRB, 0)],
     [(UL, 0), (UB, 0), (UR, 0), (UF, 0), (DR, 0), (DF, 0), (DL, 0), (DB, 0), (FR, 0), (FL, 0), (BL, 0), (BR, 0)]],
    # U'
    [[(UFL, 0), (ULB, 0), (UBR, 0), (URF, 0), (DFR, 0), (DLF, 0), (DBL, 0), (DRB, 0)],
     [(UF, 0), (UL, 0), (UB, 0), (UR, 0), (DR, 0), (DF, 0), (DL, 0), (DB, 0), (FR, 0), (FL, 0), (BL, 0), (BR, 0)]],
    # R
    [[(DFR, 2), (UFL, 0), (ULB, 0), (URF, 1), (DRB, 1), (DLF, 0), (DBL, 0), (UBR, 2)],
     [(FR, 0), (UF, 0), (UL, 0), (UB, 0), (BR, 0), (DF, 0), (DL, 0), (DB, 0), (DR, 0), (FL, 0), (BL, 0), (UR, 0)]],
    # R2
    [[(DRB, 0), (UFL, 0), (ULB, 0), (DFR, 0), (UBR, 0), (DLF, 0), (DBL, 0), (URF, 0)],
     [(DR, 0), (UF, 0), (UL, 0), (UB, 0), (UR, 0), (DF, 0), (DL, 0), (DB, 0), (BR, 0), (FL, 0), (BL, 0), (FR, 0)]],
    # R'
    [[(UBR, 2), (UFL, 0), (ULB, 0), (DRB, 1), (URF, 1), (DLF, 0), (DBL, 0), (DFR, 2)],
     [(BR, 0), (UF, 0), (UL, 0), (UB, 0), (FR, 0), (DF, 0), (DL, 0), (DB, 0), (UR, 0), (FL, 0), (BL, 0), (DR, 0)]],
    # F
    [[(UFL, 1), (DLF, 2), (ULB, 0), (UBR, 0), (URF, 2), (DFR, 1), (DBL, 0), (DRB, 0)],
     [(UR, 0), (FL, 1), (UL, 0), (UB, 0), (DR, 0), (FR, 1), (DL, 0), (DB, 0), (UF, 1), (DF, 1), (BL, 0), (BR, 0)]],
    # F2
    [[(DLF, 0), (DFR, 0), (ULB, 0), (UBR, 0), (UFL, 0), (URF, 0), (DBL, 0), (DRB, 0)],
     [(UR, 0), (DF, 0), (UL, 0), (UB, 0), (DR, 0), (UF, 0), (DL, 0), (DB, 0), (FL, 0), (FR, 0), (BL, 0), (BR, 0)]],
    # F'
    [[(DFR, 1), (URF, 2), (ULB, 0), (UBR, 0), (DLF, 2), (UFL, 1), (DBL, 0), (DRB, 0)],
     [(UR, 0), (FR, 1), (UL, 0), (UB, 0), (DR, 0), (FL, 1), (DL, 0), (DB, 0), (DF, 1), (UF, 1), (BL, 0), (BR, 0)]],
    # D
    [[(URF, 0), (UFL, 0), (ULB, 0), (UBR, 0), (DLF, 0), (DBL, 0), (DRB, 0), (DFR, 0)],
     [(UR, 0), (UF, 0), (UL, 0), (UB, 0), (DF, 0), (DL, 0), (DB, 0), (DR, 0), (FR, 0), (FL, 0), (BL, 0), (BR, 0)]],
    # D2
    [[(URF, 0), (UFL, 0), (ULB, 0), (UBR, 0), (DBL, 0), (DRB, 0), (DFR, 0), (DLF, 0)],
     [(UR, 0), (UF, 0), (UL, 0), (UB, 0), (DL, 0), (DB, 0), (DR, 0), (DF, 0), (FR, 0), (FL, 0), (BL, 0), (BR, 0)]],
    # D'
    [[(URF, 0), (UFL, 0), (ULB, 0), (UBR, 0), (DRB, 0), (DFR, 0), (DLF, 0), (DBL, 0)],
     [(UR, 0), (UF, 0), (UL, 0), (UB, 0), (DB, 0), (DR, 0), (DF, 0), (DL, 0), (FR, 0), (FL, 0), (BL, 0), (BR, 0)]],
    # L
    [[(URF, 0), (ULB, 1), (DBL, 2), (UBR, 0), (DFR, 0), (UFL, 2), (DLF, 1), (DRB, 0)],
     [(UR, 0), (UF, 0), (BL, 0), (UB, 0), (DR, 0), (DF, 0), (FL, 0), (DB, 0), (FR, 0), (UL, 0), (DL, 0), (BR, 0)]],
    # L2
    [[(URF, 0), (DBL, 0), (DLF, 0), (UBR, 0), (DFR, 0), (ULB, 0), (UFL, 0), (DRB, 0)],
     [(UR, 0), (UF, 0), (DL, 0), (UB, 0), (DR, 0), (DF, 0), (UL, 0), (DB, 0), (FR, 0), (BL, 0), (FL, 0), (BR, 0)]],
    # L'
    [[(URF, 0), (DLF, 1), (UFL, 2), (UBR, 0), (DFR, 0), (DBL, 2), (ULB, 1), (DRB, 0)],
     [(UR, 0), (UF, 0), (FL, 0), (UB, 0), (DR, 0), (DF, 0), (BL, 0), (DB, 0), (FR, 0), (DL, 0), (UL, 0), (BR, 0)]],
    # B
    [[(URF, 0), (UFL, 0), (UBR, 1), (DRB, 2), (DFR, 0), (DLF, 0), (ULB, 2), (DBL, 1)],
     [(UR, 0), (UF, 0), (UL, 0), (BR, 1), (DR, 0), (DF, 0), (DL, 0), (BL, 1), (FR, 0), (FL, 0), (UB, 1), (DB, 1)]],
    # B2
    [[(URF, 0), (UFL, 0), (DRB, 0), (DBL, 0), (DFR, 0), (DLF, 0), (UBR, 0), (ULB, 0)],
     [(UR, 0), (UF, 0), (UL, 0), (DB, 0), (DR, 0), (DF, 0), (DL, 0), (UB, 0), (FR, 0), (FL, 0), (BR, 0), (BL, 0)]],
    # B'
    [[(URF, 0), (UFL, 0), (DBL, 1), (ULB, 2), (DFR, 0), (DLF, 0), (DRB, 2), (UBR, 1)],
     [(UR, 0), (UF, 0), (UL, 0), (BL, 1), (DR, 0), (DF, 0), (DL, 0), (BR, 1), (FR, 0), (FL, 0), (DB, 1), (UB, 1)]]
]


class CubieCube:
    """http://kociemba.org/math/cubielevel.htm"""
    def __init__(self, corners=None, edges=None):
        if corners is None:
            self.corners = [Corner(i) for i in range(8)]
        else:
            self.corners = [Corner(c.c, c.o) for c in corners]
        if edges is None:
            self.edges = [Edge(i) for i in range(12)]
        else:
            self.edges = [Edge(e.c, e.o) for e in edges]

    def apply_moves(self, moves) -> None:
        for move in moves:
            if move in MOVES:
                self.move(move)
            else:
                raise ValueError(f"Can't recognize move {move}. Allowed moves in range 0-17")

    def scramble(self, scramble: str) -> None:
        """Разрешенные действия F R U B L D - F' R' U' B' L' D'"""
        if len(scramble.strip()) == 0:
            return
        moves = scramble.strip().split(" ")
        if len(moves) == 0:
            return
        for move in moves:
            if move in MOVES_S:
                self.move(MOVES_S.index(move.upper()))
            else:
                raise ValueError(f"Can't recognize move {move}")

    def move(self, move):
        """Разрешенные действия 0-17"""
        c_m = CUBIE_MOVE[move][0]
        e_m = CUBIE_MOVE[move][1]
        c = [(c.c, c.o) for c in self.corners]
        e = [(e.c, e.o) for e in self.edges]

        i = 0
        while i < 8:
            t = c[c_m[i][0]]
            self.corners[i].c = t[0]
            self.corners[i].o = (t[1] + c_m[i][1]) % 3
            i += 1

        i = 0
        while i < 12:
            t = e[e_m[i][0]]
            self.edges[i].c = t[0]
            self.edges[i].o = (t[1] + e_m[i][1]) % 2
            i += 1

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

    def check_in_phase2(self):
        return self.get_edges_flip() == 0 and \
               self.get_corners_twist() == 0 and \
               self.get_ud_slice_coord() == 0

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

    def set_ud_slice_coord(self, idx):
        slice_edge = list(range(FR, BR + 1))
        other_edge = [UR, UF, UL, UB, DR, DF, DL, DB]
        a = idx
        for e in self.edges:
            e.c = -1  # Invalidate all edge positions

        x = 4  # set slice edges
        for j in range(12):
            if a - comb(11 - j, x) >= 0:
                self.edges[j].c = slice_edge[4 - x]
                a -= comb(11 - j, x)
                x -= 1

        x = 0  # set the remaining edges UR..DB
        for j in range(12):
            if self.edges[j].c == -1:
                self.edges[j].c = other_edge[x]
                x += 1

    # def __edges_coord__(self, start, end):
    #     from collections import deque
    #     res, n = 0, 0
    #     edges = deque(self.edges[:])
    #     if start == UR or start == DR:
    #         edges.rotate(4)
    #     for i in range(BR, UR - 1, -1):
    #         if start <= edges[i].c <= end:
    #             res += comb(11 - i, n + 1)
    #             n += 1
    #     return res

    def get_corners_twist(self):
        """Ориентация углов описывается числом от 0 до 2186 (3^7 - 1)"""
        res = 0
        for i in range(7):
            res = 3 * res + self.corners[i].o
        return res

    def set_corners_twist(self, twist):
        parity = 0
        for i in range(DRB - 1, URF - 1, -1):
            self.corners[i].o = twist % 3
            parity += self.corners[i].o
            twist //= 3
        self.corners[DRB].o = ((3 - parity % 3) % 3)

    def get_edges_flip(self):
        """Ориентация ребер описывается числом от 0 до 2047 (2^11 - 1)"""
        res = 0
        for i in range(11):
            res = 2 * res + self.edges[i].o
        return res

    def set_edges_flip(self, flip):
        parity = 0
        for i in range(BR - 1, UR - 1, -1):
            self.edges[i].o = flip % 2
            parity += self.edges[i].o
            flip //= 2
        self.edges[BR].o = ((2 - parity % 2) % 2)

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
                rotate_left(edge4, 0, j)
                k += 1
            b = (j + 1) * b + k
        return 24 * a + b

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
        perm = list([corner.c for corner in self.corners])
        b, j = 0, DRB
        while j > -1:
            k = 0
            while perm[j] != j:
                rotate_left(perm, 0, j)
                k += 1
            b = (j + 1) * b + k
            j -= 1
        return b

    def set_corners(self, idx):
        for i in range(8):
            self.corners[i].c = i

        for j in range(8):
            k = idx % (j + 1)
            idx //= j + 1
            while k > 0:
                rotate_right(self.corners, 0, j)
                k -= 1

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

        # res = 0
        # for i in range(DB, UR - 1, -1):
        #     s = 0
        #     for j in range(i - 1, UR - 1, -1):
        #         if self.edges[j].c > self.edges[i].c:
        #             s += 1
        #     res = (res + s) * i
        # return res
        perm = list([edge.c for edge in self.edges[0:8]])
        b, j = 0, DB
        while j > -1:
            k = 0
            while perm[j] != j:
                rotate_left(perm, 0, j)
                k += 1
            b = (j + 1) * b + k
            j -= 1
        return b

    def set_ud_edges(self, ud_edge):
        # ребра FR FL BL BR не учитываются
        for i in range(0, 8):
            self.edges[i].c = i
        for j in range(0, 8):
            k = ud_edge % (j + 1)
            ud_edge //= j + 1
            while k > 0:
                rotate_right(self.edges, 0, j)
                k -= 1

    def __mul__(self, other):
        self.corner_multiply(other)
        self.edge_multiply(other)

    def __str__(self) -> str:
        return ", ".join([f"({corner})" for corner in self.corners]) + '\n' + \
               ", ".join([f"({edge})" for edge in self.edges])

    def __eq__(self, other) -> bool:
        return self.edges == other.edges and self.corners == other.corners


def get_random_cubie():
    cubie = CubieCube()
    cubie.apply_moves(get_random_moves())
    return cubie


def get_random_cubie_2():
    cubie = CubieCube()
    cubie.apply_moves(get_random_moves_2())
    return cubie
