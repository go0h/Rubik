
import rubik.CubieCube as cc
import rubik.Utils as u
from rubik.Corner import URF, UFL, ULB, UBR, DFR, DLF, DBL, DRB, Corner
from rubik.Edge import UR, UF, UL, UB, DR, DF, DL, DB, FR, FL, BL, BR, Edge

# S_URF3,   120-градусный разворот куба вокруг оси между URF углом и DBL углом
# S_F2,     180-градусный разворот куба вокруг оси между передним (F) центром и задним центром (B)
# S_U4,     90-градусный разворот куба вокруг оси между верхним (U) центром и нижним центром (D)
# S_LR2,    зеркальное отражение относительно RL среза

S_URF3, S_F2, S_U4, S_LR2 = range(4)

SYM_N = 48

# (координата, ориентация)
CORNER_CUBIE_SYM = {
    S_URF3: [(URF, 1), (DFR, 2), (DLF, 1), (UFL, 2), (UBR, 2), (DRB, 1), (DBL, 2), (ULB, 1)],
    S_F2: [(DLF, 0), (DFR, 0), (DRB, 0), (DBL, 0), (UFL, 0), (URF, 0), (UBR, 0), (ULB, 0)],
    S_U4: [(UBR, 0), (URF, 0), (UFL, 0), (ULB, 0), (DRB, 0), (DFR, 0), (DLF, 0), (DBL, 0)],
    S_LR2: [(UFL, 3), (URF, 3), (UBR, 3), (ULB, 3), (DLF, 3), (DFR, 3), (DRB, 3), (DBL, 3)]
}

# (координата, ориентация)
EDGE_CUBIE_SYM = {
    S_URF3: [(UF, 1), (FR, 0), (DF, 1), (FL, 0), (UB, 1), (BR, 0), (DB, 1), (BL, 0), (UR, 1), (DR, 1), (DL, 1),
             (UL, 1)],
    S_F2: [(DL, 0), (DF, 0), (DR, 0), (DB, 0), (UL, 0), (UF, 0), (UR, 0), (UB, 0), (FL, 0), (FR, 0), (BR, 0), (BL, 0)],
    S_U4: [(UB, 0), (UR, 0), (UF, 0), (UL, 0), (DB, 0), (DR, 0), (DF, 0), (DL, 0), (BR, 1), (FR, 1), (FL, 1), (BL, 1)],
    S_LR2: [(UL, 0), (UF, 0), (UR, 0), (UB, 0), (DL, 0), (DF, 0), (DR, 0), (DB, 0), (FL, 0), (FR, 0), (BR, 0), (BL, 0)]
}


def corner_wrapper(sym):
    raw = CORNER_CUBIE_SYM[sym]
    return list(map(lambda x: Corner(x[0], x[1]), raw))


def edge_wrapper(sym):
    raw = EDGE_CUBIE_SYM[sym]
    return list(map(lambda x: Edge(x[0], x[1]), raw))


BASIC_SYM_CUBE = {
    S_URF3: cc.CubieCube(corner_wrapper(S_URF3), edge_wrapper(S_URF3)),
    S_F2:   cc.CubieCube(corner_wrapper(S_F2), edge_wrapper(S_F2)),
    S_U4:   cc.CubieCube(corner_wrapper(S_U4), edge_wrapper(S_U4)),
    S_LR2:  cc.CubieCube(corner_wrapper(S_LR2), edge_wrapper(S_LR2))
}

# Вычисляем 48 симметрий путем перебора базовых симметрий
# (S_URF3)x1 * (S_F2)x2 * (S_U4)x3 * (S_LR2)x4
SYM_CUBIES = []
cubie = cc.CubieCube()
for _ in range(3):  # S_URF3
    for _ in range(2):  # S_F2
        for _ in range(4):  # S_U4
            for _ in range(2):  # S_LR2
                SYM_CUBIES.append(cc.CubieCube(cubie.corners, cubie.edges))
                cubie.multiply(BASIC_SYM_CUBE[S_LR2])
            cubie.multiply(BASIC_SYM_CUBE[S_U4])
        cubie.multiply(BASIC_SYM_CUBE[S_F2])
    cubie.multiply(BASIC_SYM_CUBE[S_URF3])

# вычиляем индексы кубов для обратной симметрии
# SYM_CUBIES[INV_IDX[ic]] == SYM_CUBIES[i]^(-1)
INV_IDX = [0 for _ in range(SYM_N)]
for j in range(SYM_N):
    for i in range(SYM_N):
        c1 = cc.CubieCube(SYM_CUBIES[j].corners, SYM_CUBIES[j].edges)
        c1.corner_multiply(SYM_CUBIES[i])
        if c1.corners[URF].c == URF and c1.corners[UFL].c == UFL and c1.corners[ULB].c == ULB:
            INV_IDX[j] = i
            break


# def get_symmetries(cub: cc.CubieCube):
#     symmetries = []
#     inv = cc.CubieCube()
#     for s in range(SYM_N):
#         c = cc.CubieCube(SYM_CUBIES[s].corners, SYM_CUBIES[s].edges)
#         c.multiply(cub)
#         c.multiply(SYM_CUBIES[INV_IDX[s]])
#         if cub == c:
#             symmetries.append(s)
#         c.inverse_cubie(inv)
#         if cub == c:
#             symmetries.append(s + SYM_N)
#     return symmetries