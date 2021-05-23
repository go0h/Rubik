
import rubik.CubieCube as cc
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


def create_conj_twist():
    conj_twist = [[0 for _ in range(16)] for _ in range(2187)]
    for twist in range(2187):
        cub = cc.CubieCube()
        cub.set_corners_twist(twist)
        for s in range(16):
            sym_cubie = cc.CubieCube(SYM_CUBIES[s].corners, SYM_CUBIES[s].edges)
            sym_cubie.corner_multiply(cub)                      # s * t
            sym_cubie.corner_multiply(SYM_CUBIES[INV_IDX[s]])   # s * t * s^-1
            conj_twist[twist][s] = sym_cubie.get_corners_twist()
    return conj_twist


def create_conj_ud_edges():
    conj_ud_edges = [[0 for _ in range(16)] for _ in range(40320)]
    for ud_edge in range(40320):
        cub = cc.CubieCube()
        cub.set_ud_edges(ud_edge)
        for s in range(16):
            sym_cubie = cc.CubieCube(SYM_CUBIES[s].corners, SYM_CUBIES[s].edges)
            sym_cubie.edge_multiply(cub)                      # s * t
            sym_cubie.edge_multiply(SYM_CUBIES[INV_IDX[s]])   # s * t * s^-1
            conj_ud_edges[ud_edge][s] = sym_cubie.get_ud_edges()
    return conj_ud_edges


def create_fs_classidx():
    # fs_classidx[classidx][sym][first_classidx]
    fs_classidx = [[65535, 0, 0] for _ in range(495 * 2048)]
    classidx = 0
    cub = cc.CubieCube()
    # для каждой перестановки UD-разреза
    for sl in range(495):
        # выставляем перестановку
        cub.set_ud_slice_coord(sl)
        # для каждой ориентации ребер из 2048
        for flip in range(2048):
            # выставляем ориентацию
            cub.set_edges_flip(flip)

            # получаем индекс
            idx = 2048 * sl + flip
            # если класс эквивалентноти еще не занят
            if fs_classidx[idx][0] == 65535:
                # выставляем порядковый номер класса
                fs_classidx[idx][0] = classidx
                # номер симметрии
                fs_classidx[idx][1] = 0
                # сохраняем первый индекс класса эквивалентности
                fs_classidx[idx][2] = idx
            else:
                continue

            # генерируем 16 симметрий для каждого класса эквивалентности
            for s in range(16):

                sym = cc.CubieCube(SYM_CUBIES[INV_IDX[s]].corners, SYM_CUBIES[INV_IDX[s]].edges)
                sym.edge_multiply(cub)
                sym.edge_multiply(SYM_CUBIES[s])

                new_idx = 2048 * sym.get_ud_slice_coord() + sym.get_edges_flip()
                if fs_classidx[new_idx][0] == 65535:
                    fs_classidx[new_idx][0] = classidx
                    fs_classidx[new_idx][1] = s
                    fs_classidx[new_idx][2] = idx

            classidx += 1

    return fs_classidx


def create_co_classidx():
    # co_classidx[classidx][sym][first_classidx]
    co_classidx = [[65535, 0, 0] for _ in range(40320)]
    cub = cc.CubieCube()
    classidx = 0
    for idx in range(40320):

        cub.set_corners(idx)

        if co_classidx[idx][0] == 65535:
            co_classidx[idx][0] = classidx
            co_classidx[idx][1] = 0
            co_classidx[idx][2] = idx
        else:
            continue

        # генерируем 16 симметрий для каждого класса эквивалентности
        for s in range(16):

            sym = cc.CubieCube(SYM_CUBIES[INV_IDX[s]].corners, SYM_CUBIES[INV_IDX[s]].edges)
            sym.corner_multiply(cub)
            sym.corner_multiply(SYM_CUBIES[s])

            idx_new = sym.get_corners()
            if co_classidx[idx_new][0] == 65535:
                co_classidx[idx_new][0] = classidx
                co_classidx[idx_new][1] = s
                co_classidx[idx_new][2] = idx

        classidx += 1

    return co_classidx
