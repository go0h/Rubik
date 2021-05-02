from rubik.Corner import URF, UFL, ULB, UBR, DFR, DLF, DBL, DRB
from rubik.Edge import UR, UF, UL, UB, DR, DF, DL, DB, FR, FL, BL, BR

# S_URF3, a 120 degree turn of the cube around an axis through the URF-corner and DBL-corner,
# S_F2, a 180 degree turn of the cube around an axis through the F-center and B-center,
# S_U4, a 90 degree turn of the cube around an axis through the U-center and the D-center
# S_LR2, a reflection at the RL-slice plane.

S_URF3, S_F2, S_U4, S_LR2 = range(4)

SYM_N = 48

# (permutation, orientation)
CORNER_CUBIE_SYM = {
  S_URF3: [(URF, 1), (DFR, 2), (DLF, 1), (UFL, 2), (UBR, 2), (DRB, 1), (DBL, 2), (ULB, 1)],
  S_F2:   [(DLF, 0), (DFR, 0), (DRB, 0), (DBL, 0), (UFL, 0), (URF, 0), (UBR, 0), (ULB, 0)],
  S_U4:   [(UBR, 0), (URF, 0), (UFL, 0), (ULB, 0), (DRB, 0), (DFR, 0), (DLF, 0), (DBL, 0)],
  S_LR2:  [(UFL, 3), (URF, 3), (UBR, 3), (ULB, 3), (DLF, 3), (DFR, 3), (DRB, 3), (DBL, 3)]
}

# (permutation, orientation)
EDGE_CUBIE_SYM = {
  S_URF3: [(UF, 1), (FR, 0), (DF, 1), (FL, 0), (UB, 1), (BR, 0), (DB, 1), (BL, 0), (UR, 1), (DR, 1), (DL, 1), (UL, 1)],
  S_F2:   [(DL, 0), (DF, 0), (DR, 0), (DB, 0), (UL, 0), (UF, 0), (UR, 0), (UB, 0), (FL, 0), (FR, 0), (BR, 0), (BL, 0)],
  S_U4:   [(UB, 0), (UR, 0), (UF, 0), (UL, 0), (DB, 0), (DR, 0), (DF, 0), (DL, 0), (BR, 1), (FR, 1), (FL, 1), (BL, 1)],
  S_LR2:  [(UL, 0), (UF, 0), (UR, 0), (UB, 0), (DL, 0), (DF, 0), (DR, 0), (DB, 0), (FL, 0), (FR, 0), (BR, 0), (BL, 0)]
}
