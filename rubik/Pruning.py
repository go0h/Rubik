from rubik.Symmetries import SYM_CUBIES, INV_IDX
import rubik.CubieCube as cc
from rubik.Utils import MOVES, PHASE2_MOVES
import rubik.Tables as t


def get_fs_twist_depth3(table, index):
    """Возвращает количество ходов по модулю 3 для решения фазы 1 для куба с индексом index"""
    y = table[index // 16]
    y >>= (index % 16) * 2
    return y & 3


def set_fs_twist_depth3(table, ix, value):
    shift = (ix % 16) * 2
    base = ix >> 4
    table[base] &= ~(3 << shift) & 0xffffffff
    table[base] |= value << shift


def create_pruning1_table():

    total = 64430 * 2187  # 140.689.710
    fs_twist_depth = [0xffffffff for _ in range(total // 16 + 1)]

    # #################### создаем таблицу ссиметрий fs_class  ###############################
    cub = cc.CubieCube()
    fs_rep = list(dict.fromkeys([t.fs_classidx[i][2] for i in range(len(t.fs_classidx))]))
    fs_sym = [0 for _ in range(64430)]
    for i in range(64430):

        rep = fs_rep[i]
        cub.set_ud_slice_coord(rep // 2048)
        cub.set_edges_flip(rep % 2048)

        for s in range(16):
            sym_cubie = cc.CubieCube(SYM_CUBIES[s].corners, SYM_CUBIES[s].edges)
            sym_cubie.edge_multiply(cub)  # s * cc
            sym_cubie.edge_multiply(SYM_CUBIES[INV_IDX[s]])  # s * cc * s^-1
            if sym_cubie.get_ud_slice_coord() == rep // 2048 and sym_cubie.get_edges_flip() == rep % 2048:
                fs_sym[i] |= 1 << s
    # ##################################################################################################################

    set_fs_twist_depth3(fs_twist_depth, 0, 0)
    done = 1
    depth = 0
    back_search = False
    while done != total:
        print(f"Depth - {depth}, done {done}/{total}")
        depth3 = depth % 3
        if depth == 9:
            back_search = True

        idx = 0
        for classidx in range(64430):
            twist = 0
            while twist < 2187:

                # если таблице не заполнены записи, ускоряем, с помощь обратного поиска
                if not back_search and idx % 16 == 0 and fs_twist_depth[idx // 16] == 0xffffffff and twist < 2187 - 16:
                    twist += 16
                    idx += 16
                    continue
                ####################################################################################################

                if back_search:
                    match = (get_fs_twist_depth3(fs_twist_depth, idx) == 3)
                else:
                    match = (get_fs_twist_depth3(fs_twist_depth, idx) == depth3)

                if match:
                    fs = fs_rep[classidx]
                    flip = fs % 2048     # defs.N_FLIP = 2048
                    slice = fs >> 11     # defs.N_FLIP

                    for move in MOVES:

                        twist1 = t.move_twist[twist][move]
                        flip1 = t.move_flip[flip][move]
                        slice1 = t.move_slice_sorted[24 * slice][move] // 24  # defs.N_PERM_4 = 24, 18*24 = 432

                        fs1 = (slice1 << 11) + flip1
                        fs1_classidx = t.fs_classidx[fs1][0]

                        fs1_sym = t.fs_classidx[fs1][1]
                        twist1 = t.conj_twist[twist1][fs1_sym]

                        idx1 = 2187 * fs1_classidx + twist1  # defs.N_TWIST = 2187

                        if not back_search:
                            if get_fs_twist_depth3(fs_twist_depth, idx1) == 3:  # если еще не заполнен
                                set_fs_twist_depth3(fs_twist_depth, idx1, (depth + 1) % 3)
                                done += 1
                                # симметрия может иметь несколько представлений
                                sym = fs_sym[fs1_classidx]
                                if sym != 1:
                                    for j in range(1, 16):
                                        sym >>= 1
                                        if sym % 2 == 1:
                                            twist2 = t.conj_twist[twist1][j]
                                            idx2 = 2187 * fs1_classidx + twist2
                                            if get_fs_twist_depth3(fs_twist_depth, idx2) == 3:
                                                set_fs_twist_depth3(fs_twist_depth, idx2, (depth + 1) % 3)
                                                done += 1
                                ####################################################################################

                        else:  # backwards search
                            if get_fs_twist_depth3(fs_twist_depth, idx1) == depth3:
                                set_fs_twist_depth3(fs_twist_depth, idx, (depth + 1) % 3)
                                done += 1
                                break
                twist += 1
                idx += 1  # idx = defs.N_TWIST * fs_class + twist

        depth += 1
    return fs_twist_depth


def create_pruning2_table():

    co_ud_edges_depth = [[20 for _ in range(40320)] for _ in range(2768)]  # 111605760

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
                        c1_classidx = t.co_classidx[corner1][0]
                        c1_sym = t.co_classidx[corner1][1]

                        ud_edge1 = t.conj_ud_edges[ud_edge1][c1_sym]

                        if co_ud_edges_depth[c1_classidx][ud_edge1] == 20:

                            co_ud_edges_depth[c1_classidx][ud_edge1] = depth + 1
                            # симметрия может иметь несколько представлений
                            sym = co_sym[c1_classidx]
                            if sym != 1:
                                for j in range(1, 16):
                                    sym >>= 1
                                    if sym % 2 == 1:
                                        ud_edge2 = t.conj_ud_edges[ud_edge1][j]
                                        if co_ud_edges_depth[c1_classidx][ud_edge2] == 20:
                                            co_ud_edges_depth[c1_classidx][ud_edge2] = depth + 1

                ud_edge += 1
        depth += 1
    return co_ud_edges_depth
