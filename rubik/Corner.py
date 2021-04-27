
# coordinate of Corners
URF, UFL, ULB, UBR, DFR, DLF, DBL, DRB = range(8)

CORNERS = {URF: "URF", UFL: "UFL", ULB: "ULB", UBR: "UBR",
           DFR: "DFR", DLF: "DLF", DBL: "DBL", DRB: "DRB"}

# CORNERS_COLORS = {
#     URF: "URF", UFL: "UFL", ULB: "ULB", UBR: "UBR",
#     DFR: "DFR", DLF: "DLF", DBL: "DBL", DRB: "DRB"
# }

# CORNERS_TO_SIDE_POS = {
#     URF: [()]
# }

class Corner:

    def __init__(self, num, orient=0):
        # c - coordinate
        self.c = num
        # o - orientation
        self.o = orient

    def rotate(self, coord, num):
        self.c = coord
        self.o += num
        if self.o > 2:
            self.o -= 3

    def __str__(self):
        return CORNERS[self.c] + "," + str(self.o)

    def __eq__(self, other) -> bool:
        return self.o == other.o and self.c == other.c
