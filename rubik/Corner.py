
from rubik.Colors import B, L, U, R, D, F

# coordinate of Corners
URF, UFL, ULB, UBR, DFR, DLF, DBL, DRB = range(8)

CORNERS = {URF: "URF", UFL: "UFL", ULB: "ULB", UBR: "UBR",
           DFR: "DFR", DLF: "DLF", DBL: "DBL", DRB: "DRB"}

CORNERS_FACES = {
    URF: [U, R, F], UFL: [U, F, L], ULB: [U, L, B], UBR: [U, B, R],
    DFR: [D, F, R], DLF: [D, L, F], DBL: [D, B, L], DRB: [D, R, B]
}


class Corner:

    def __init__(self, num, orient=0):
        # c - coordinate
        self.c = num
        # o - orientation
        self.o = orient

    def rotate(self, coord, num) -> None:
        self.c = coord
        self.o += num
        if self.o > 2:
            self.o -= 3

    def get_coordinates(self, position) -> list:
        # URF, UFL, ULB, UBR, DFR, DLF, DBL, DRB
        c1, c2, c3 = [CORNERS_FACES[self.c][(i + self.o) % 3] for i in range(3)]
        corners_to_side_pos = {
            URF: [[2, 2, c1], [0, 0, c2], [0, 2, c3]],
            UFL: [[2, 0, c1], [0, 0, c2], [0, 2, c3]],
            ULB: [[0, 0, c1], [0, 0, c2], [0, 2, c3]],
            UBR: [[0, 2, c1], [0, 0, c2], [0, 2, c3]],
            DFR: [[0, 2, c1], [2, 2, c2], [2, 0, c3]],
            DLF: [[0, 0, c1], [2, 2, c2], [2, 0, c3]],
            DBL: [[2, 0, c1], [2, 2, c2], [2, 0, c3]],
            DRB: [[2, 2, c1], [2, 2, c2], [2, 0, c3]]
        }
        return corners_to_side_pos[position]

    def __str__(self) -> str:
        return CORNERS[self.c] + "," + str(self.o)

    def __eq__(self, other) -> bool:
        return self.o == other.o and self.c == other.c
