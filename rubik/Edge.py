
from rubik.Colors import B, L, U, R, D, F

# coordinate of Edges
UR, UF, UL, UB, DR, DF, DL, DB, FR, FL, BL, BR = range(12)

EDGES = {UF: "UF", UL: "UL", UB: "UB", UR: "UR",
         DF: "DF", DL: "DL", DB: "DB", DR: "DR",
         FL: "FL", FR: "FR", BL: "BL", BR: "BR"}

EDGE_FACES = {
    UR: [U, R], UF: [U, F], UL: [U, L], UB: [U, B], DR: [D, R], DF: [D, F],
    DL: [D, L], DB: [D, B], FR: [F, R], FL: [F, L], BL: [B, L], BR: [B, R]
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
        # UR, UF, UL, UB, DR, DF, DL, DB, FR, FL, BL, BR
        c1, c2 = [EDGE_FACES[self.c][(i + self.o) % 2] for i in range(2)]
        edges_to_side_pos = {
            UR: [[1, 2, c1], [0, 1, c2]],
            UF: [[2, 1, c1], [0, 1, c2]],
            UL: [[1, 0, c1], [0, 1, c2]],
            UB: [[0, 1, c1], [0, 1, c2]],
            DR: [[1, 2, c1], [2, 1, c2]],
            DF: [[0, 1, c1], [2, 1, c2]],
            DL: [[1, 0, c1], [2, 1, c2]],
            DB: [[2, 1, c1], [2, 1, c2]],
            FR: [[1, 2, c1], [1, 0, c2]],
            FL: [[1, 0, c1], [1, 2, c2]],
            BL: [[1, 2, c1], [1, 0, c2]],
            BR: [[1, 0, c1], [1, 2, c2]]
        }
        return edges_to_side_pos[position]

    def __str__(self) -> str:
        return EDGES[self.c] + "," + str(self.o)

    def __eq__(self, other) -> bool:
        return self.o == other.o and self.c == other.c
