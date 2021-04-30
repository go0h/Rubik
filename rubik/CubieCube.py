from rubik.Edge import *
from rubik.Corner import *
from rubik.FaceletCube import *

C = Corner
E = Edge

basic_cube_moves = {
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

    def to_facelet_cube(self) -> FaceletCube:
        facelet = FaceletCube()
        for i in range(len(self.corners)):
            facelet.set_corner(i, self.corners[i])
        for i in range(len(self.edges)):
            facelet.set_edge(i, self.edges[i])
        return facelet

    def __str__(self) -> str:
        return ", ".join([f"({corner})" for corner in self.corners]) + '\n' + \
               " ".join([f"({edge})" for edge in self.edges])

    def __eq__(self, other) -> bool:
        return self.edges == other.edges and self.corners == other.corners
