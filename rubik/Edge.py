
from rubik.Colors import B, L, U, R, D, F
from collections import deque

# coordinate of Edges
UR, UF, UL, UB, DR, DF, DL, DB, FR, FL, BL, BR = range(12)

EDGES = {UF: "UF", UL: "UL", UB: "UB", UR: "UR",
         DF: "DF", DL: "DL", DB: "DB", DR: "DR",
         FL: "FL", FR: "FR", BL: "BL", BR: "BR"}

EDGE_SIDES = {
    UR: [U, R], UF: [U, F], UL: [U, L], UB: [U, B], DR: [D, R], DF: [D, F],
    DL: [D, L], DB: [D, B], FR: [F, R], FL: [F, L], BL: [B, L], BR: [B, R]
}

EDGE_FACES_COORDS = {
    UR: [[1, 2], [0, 1]],
    UF: [[2, 1], [0, 1]],
    UL: [[1, 0], [0, 1]],
    UB: [[0, 1], [0, 1]],
    DR: [[1, 2], [2, 1]],
    DF: [[0, 1], [2, 1]],
    DL: [[1, 0], [2, 1]],
    DB: [[2, 1], [2, 1]],
    FR: [[1, 2], [1, 0]],
    FL: [[1, 0], [1, 2]],
    BL: [[1, 2], [1, 0]],
    BR: [[1, 0], [1, 2]]
}

EDGE_BY_SIDES = {
    U: {R: UR, F: UF, L: UL, B: UB},
    D: {R: DR, F: DF, L: DL, B: DB},
    F: {R: FR, L: FL},
    B: {L: BL, R: BR}
}


class Edge:

    def __init__(self, num, flip=0):
        # c - coordinate
        self.c = num
        # o - orientation
        self.o = flip

    def rotate(self, coord, flip) -> None:
        self.c = coord
        self.o += flip
        if self.o > 1:
            self.o -= 2

    def get_coordinates(self, position) -> list:
        c1, c2 = [EDGE_SIDES[self.c][(i + self.o) % 2] for i in range(2)]
        return [EDGE_FACES_COORDS[position][0] + [c1],
                EDGE_FACES_COORDS[position][1] + [c2]]

    def set_coordinate(self, position, sides) -> None:
        # получаем лицевые стороны угла, в зависимости от позиции
        f1, f2 = EDGE_SIDES[position]
        # получаем сслыки на объект Side
        s1, s2 = sides[f1], sides[f2]

        # получаем координаты где располагаются ребра
        c1, c2 = EDGE_FACES_COORDS[position]

        # получаем текущие стороны которые располжены в углу
        e_sides = deque([s1.side[c1[0]][c1[1]], s2.side[c2[0]][c2[1]]])

        # вычисляем ориентацию угла
        while e_sides[0] not in EDGE_BY_SIDES.keys():
            e_sides.rotate(1)
            self.o += 1

        while e_sides[1] not in EDGE_BY_SIDES[e_sides[0]].keys():
            e_sides.rotate(1)
            self.o += 1

        # получаем реальную координату угла
        self.c = EDGE_BY_SIDES[e_sides[0]][e_sides[1]]

    def __str__(self) -> str:
        return EDGES[self.c] + "," + str(self.o)

    def __eq__(self, other) -> bool:
        return self.o == other.o and self.c == other.c
