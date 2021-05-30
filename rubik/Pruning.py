from rubik.Symmetries import SYM_CUBIES, INV_IDX
from rubik.Utils import MOVES, PHASE2_MOVES
import rubik.CubieCube as cc
import rubik.Tables as t
import numpy as np
from ctypes import CDLL
import os

libname = "pruning.so"
dir = os.getcwd() + "/pruning_on_c/"
if os.getcwd().endswith("test"):
    dir = dir.replace("/test", "")

lib_prun = CDLL(dir + libname)
create_phase1_prun_c = lib_prun.create_phase1_prun
create_phase2_prun_c = lib_prun.create_phase2_prun


def create_pruning1_table():

    total = 64430 * 2187
    # fs_twist_depth[64430][2187] = 140689710
    fs_twist_depth = [[20 for _ in range(2187)] for _ in range(64430 + 1)]

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

    fs_twist_depth[0][0] = 0
    done = 1
    depth = 0
    back_search = False
    while done != total:
        print(f"Depth - {depth} done")

        if depth == 9:
            back_search = True

        for classidx in range(64430):
            twist = 0
            while twist < 2187:

                if back_search:
                    match = fs_twist_depth[classidx][twist] == 20
                else:
                    match = fs_twist_depth[classidx][twist] == depth

                if match:
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

                        if not back_search:

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

                        else:
                            if fs_twist_depth[classidx1][twist1] == depth:
                                fs_twist_depth[classidx][twist] = depth + 1
                                done += 1
                                break
                twist += 1
        depth += 1
    return fs_twist_depth


def create_pruning2_table():

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

    # fs_twist_depth[64430][2187] = 140689710
    fs_twist_depth = np.array([20 for _ in range(2187 * 64430)], dtype=np.int8)
    move_twist = t.move_twist.flatten()
    move_flip = t.move_flip.flatten()
    move_slice_sorted = t.move_slice_sorted.flatten()
    conj_twist = t.conj_twist.flatten()
    fs_classidx = t.fs_classidx[:, 0].flatten()
    fs_sym_idx = t.fs_classidx[:, 1].flatten()
    fs_sym = np.array(fs_sym, dtype=np.int32)
    fs_rep = np.array(fs_rep, dtype=np.int32)

    create_phase1_prun_c.argtypes = [t8, t32, t32, t32, t32, t32, t32, t32, t32]
    create_phase1_prun_c.restype = None

    create_phase1_prun_c(fs_twist_depth,
                         move_twist, move_flip, move_slice_sorted,
                         conj_twist, fs_classidx, fs_sym_idx, fs_sym, fs_rep)

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
    move_ud_edges = t.move_ud_edges.flatten()
    move_corners = t.move_corners.flatten()
    conj_ud_edges = t.conj_ud_edges.flatten()
    co_classidx = t.co_classidx[:, 0].flatten()
    co_sym_idx = t.co_classidx[:, 1].flatten()
    co_sym = np.array(co_sym, dtype=np.int32)
    co_rep = np.array(co_rep, dtype=np.int32)

    create_phase2_prun_c.argtypes = [t8, t32, t32, t32, t32, t32, t32, t32]
    create_phase2_prun_c.restype = None

    create_phase2_prun_c(co_ud_edges_depth, move_ud_edges, move_corners, co_classidx,
                         co_sym_idx, co_sym, co_rep, conj_ud_edges)

    return co_ud_edges_depth.reshape((2768, 40320))
