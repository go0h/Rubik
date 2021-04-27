
# coordinate of Edges
UR, UF, UL, UB, DR, DF, DL, DB, FR, FL, BL, BR = range(12)

EDGES = {UF: "UF", UL: "UL", UB: "UB", UR: "UR",
         DF: "DF", DL: "DL", DB: "DB", DR: "DR",
         FL: "FL", FR: "FR", BL: "BL", BR: "BR"}


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

    def __str__(self) -> str:
        return EDGES[self.c] + "," + str(self.o)

    def __eq__(self, other) -> bool:
        return self.o == other.o and self.c == other.c
