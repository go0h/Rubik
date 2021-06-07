from rubik.Symmetries import SYM_CUBIES, INV_IDX
from rubik.Utils import MOVES, PHASE2_MOVES
import rubik.CubieCube as cc
import rubik.Tables as t
import numpy as np
from ctypes import CDLL
import os


def create_pruning1_table_p():

    total = 64430 * 2187
    # fs_twist_depth[64430][2187] = 140689710
    fs_twist_depth = [[20 for _ in range(2187)] for _ in range(64430)]

    # создаем таблицу симетрий fs_class
    cub = cc.CubieCube()
    fs_rep = list(dict.fromkeys([t.fs_classidx[i][2] for i in range(len(t.fs_classidx))]))
    fs_sym = [0 for _ in range(64430)]
    for i in range(64430):

        rep = fs_rep[i]
        cub.set_ud_slice_coord(rep >> 11)   # rep // 2048
        cub.set_edges_flip(rep & 0x7FF)     # rep % 2048

        for s in range(16):
            sym_cubie = cc.CubieCube(SYM_CUBIES[s].corners, SYM_CUBIES[s].edges)
            sym_cubie.edge_multiply(cub)  # s * cc
            sym_cubie.edge_multiply(SYM_CUBIES[INV_IDX[s]])  # s * cc * s^-1
            if sym_cubie.get_ud_slice_coord() == rep >> 11 and sym_cubie.get_edges_flip() == rep & 0x7FF:
                fs_sym[i] |= 1 << s

    fs_twist_depth[0][0] = 0
    done = 1
    depth = 0
    while done != total:
        print(f"Depth - {depth} done")

        for classidx in range(64430):
            twist = 0
            while twist < 2187:

                if fs_twist_depth[classidx][twist] == depth:
                    fs = fs_rep[classidx]
                    flip = fs & 0x7FF     # fs % 2048
                    slice = fs >> 11      # fs // 2048

                    for move in MOVES:

                        twist1 = t.move_twist[twist][move]
                        flip1 = t.move_flip[flip][move]
                        slice1 = t.move_slice_sorted[24 * slice][move] // 24

                        fs1 = (slice1 << 11) + flip1
                        classidx1 = t.fs_classidx[fs1][0]
                        fs_sym1 = t.fs_classidx[fs1][1]

                        twist1 = t.conj_twist[twist1][fs_sym1]

                        if fs_twist_depth[classidx1][twist1] == 20:
                            fs_twist_depth[classidx1][twist1] = depth + 1
                            done += 1
                            # симметрия может иметь несколько представлений
                            sym = fs_sym[classidx1]
                            if sym != 1:
                                for j in range(1, 16):
                                    sym >>= 1
                                    if sym & 1 == 1:
                                        twist2 = t.conj_twist[twist1][j]

                                        if fs_twist_depth[classidx1][twist2] == 20:
                                            fs_twist_depth[classidx1][twist2] = depth + 1
                                            done += 1
                twist += 1
        depth += 1
    return fs_twist_depth


def create_pruning2_table_p():

    # co_ud_edges_depth[2768][40320] = 111605760
    co_ud_edges_depth = [[20 for _ in range(40320)] for _ in range(2768)]

    # создаем таблицу ссиметрий fs_class
    cub = cc.CubieCube()
    co_sym = [0 for _ in range(2768)]
    co_rep = list(dict.fromkeys([t.co_classidx[i][2] for i in range(len(t.co_classidx))]))
    for i in range(2768):
        rep = co_rep[i]
        cub.set_corners(rep)
        for s in range(16):
            sym_cubie = cc.CubieCube(SYM_CUBIES[s].corners, SYM_CUBIES[s].edges)
            sym_cubie.corner_multiply(cub)  # s * cc
            sym_cubie.corner_multiply(SYM_CUBIES[INV_IDX[s]])  # s * cc * s^-1
            if sym_cubie.get_corners() == rep:
                co_sym[i] |= 1 << s

    depth = 0
    co_ud_edges_depth[0][0] = 0
    while depth < 10:
        print(f"Depth - {depth} done")

        for co_classidx in range(2768):

            corner = co_rep[co_classidx]
            ud_edge = 0
            while ud_edge < 40320:

                if co_ud_edges_depth[co_classidx][ud_edge] == depth:

                    for move in PHASE2_MOVES:

                        ud_edge1 = t.move_ud_edges[ud_edge][move]
                        corner1 = t.move_corners[corner][move]
                        classidx1 = t.co_classidx[corner1][0]
                        co_sym1 = t.co_classidx[corner1][1]

                        ud_edge1 = t.conj_ud_edges[ud_edge1][co_sym1]

                        if co_ud_edges_depth[classidx1][ud_edge1] == 20:

                            co_ud_edges_depth[classidx1][ud_edge1] = depth + 1
                            # симметрия может иметь несколько представлений
                            sym = co_sym[classidx1]
                            if sym != 1:
                                for j in range(1, 16):
                                    sym >>= 1
                                    if sym & 1 == 1:
                                        ud_edge2 = t.conj_ud_edges[ud_edge1][j]
                                        if co_ud_edges_depth[classidx1][ud_edge2] == 20:
                                            co_ud_edges_depth[classidx1][ud_edge2] = depth + 1

                ud_edge += 1
        depth += 1
    return co_ud_edges_depth


def create_pruning1_table_c():

    # создаем таблицу ссиметрий fs_class
    cub = cc.CubieCube()
    fs_rep = list(dict.fromkeys([t.fs_classidx[i][2] for i in range(len(t.fs_classidx))]))
    fs_sym = [0 for _ in range(64430)]
    for i in range(64430):

        rep = fs_rep[i]
        cub.set_ud_slice_coord(rep >> 11)   # rep // 2048
        cub.set_edges_flip(rep & 0x7FF)     # rep % 2048

        for s in range(16):
            sym_cubie = cc.CubieCube(SYM_CUBIES[s].corners, SYM_CUBIES[s].edges)
            sym_cubie.edge_multiply(cub)  # s * cc
            sym_cubie.edge_multiply(SYM_CUBIES[INV_IDX[s]])  # s * cc * s^-1
            if sym_cubie.get_ud_slice_coord() == rep >> 11 and sym_cubie.get_edges_flip() == rep & 0x7FF:
                fs_sym[i] |= 1 << s

    t8 = np.ctypeslib.ndpointer(dtype=np.int8, ndim=1)
    t32 = np.ctypeslib.ndpointer(dtype=np.int32, ndim=1)

    fs_twist_depth = np.array([20 for _ in range(2187 * 64430)], dtype=np.int8)
    conj_twist = t.conj_twist.flatten()

    moves = np.array(t.move_twist.flatten().tolist() +
                     t.move_flip.flatten().tolist() +
                     t.move_slice_sorted.flatten().tolist(),
                     dtype=np.int32)

    fs_classidx = np.array(t.fs_classidx[:, 0].flatten().tolist() +
                           t.fs_classidx[:, 1].flatten().tolist() +
                           fs_sym + fs_rep,
                           dtype=np.int32)

    create_phase1_prun.argtypes = [t8, t32, t32, t32]
    create_phase1_prun.restype = None

    create_phase1_prun(fs_twist_depth, moves, conj_twist, fs_classidx)

    return fs_twist_depth.reshape((64430, 2187))


def create_pruning2_table_c():

    # создаем таблицу ссиметрий fs_class
    cub = cc.CubieCube()
    co_sym = [0 for _ in range(2768)]
    co_rep = list(dict.fromkeys([t.co_classidx[i][2] for i in range(len(t.co_classidx))]))
    for i in range(2768):
        rep = co_rep[i]
        cub.set_corners(rep)
        for s in range(16):
            sym_cubie = cc.CubieCube(SYM_CUBIES[s].corners, SYM_CUBIES[s].edges)
            sym_cubie.corner_multiply(cub)  # s * cc
            sym_cubie.corner_multiply(SYM_CUBIES[INV_IDX[s]])  # s * cc * s^-1
            if sym_cubie.get_corners() == rep:
                co_sym[i] |= 1 << s

    t8 = np.ctypeslib.ndpointer(dtype=np.int8, ndim=1)
    t32 = np.ctypeslib.ndpointer(dtype=np.int32, ndim=1)

    # co_ud_edges_depth[2768][40320] = 111605760
    co_ud_edges_depth = np.array([20 for _ in range(2768 * 40320)], dtype=np.int8)
    conj_ud_edges = t.conj_ud_edges.flatten()

    moves = np.array(t.move_corners.flatten().tolist() +
                     t.move_ud_edges.flatten().tolist(),
                     dtype=np.int32)

    co_classidx = np.array(t.co_classidx[:, 0].flatten().tolist() +
                           t.co_classidx[:, 1].flatten().tolist() +
                           co_sym + co_rep,
                           dtype=np.int32)

    create_phase2_prun.argtypes = [t8, t32, t32, t32]
    create_phase2_prun.restype = None

    create_phase2_prun(co_ud_edges_depth, moves, co_classidx, conj_ud_edges)
    return co_ud_edges_depth.reshape((2768, 40320))


libname = "pruning.so"
dir = os.getcwd() + "/pruning_lib/"
if os.getcwd().endswith("test"):
    dir = dir.replace("/test", "")

if os.path.exists(dir + libname):
    lib_prun = CDLL(dir + libname)
    create_phase1_prun = lib_prun.create_phase1_prun
    create_phase2_prun = lib_prun.create_phase2_prun
    create_pruning1_table = create_pruning1_table_c
    create_pruning2_table = create_pruning2_table_c
else:
    create_pruning1_table = create_pruning1_table_p
    create_pruning2_table = create_pruning2_table_p
