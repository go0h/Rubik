import rubik.Tables as tb
import rubik.Utils as u
import rubik.CubieCube as cc


def get_phase1_depth(cubie):
    """@:return Минимальное количество ходов требуемое для достижения рандомного кубика фазы 2"""

    cub = cc.CubieCube(cubie.corners, cubie.edges)
    slice = cub.get_ud_slice_sorted() // 24
    flip = cub.get_edges_flip()
    twist = cub.get_corners_twist()

    fs_ = 2048 * slice + flip
    classidx_ = tb.fs_classidx[fs_][0]
    sym = tb.fs_classidx[fs_][1]
    # 3^7 * класс экв + ориентация 8 углов
    depth_mod3 = tb.get_fs_twist_depth3(2187 * classidx_ + tb.conj_twist[twist][sym])

    depth = 0
    # первая фаза, считается законченой, когда ориентации всех углов и ребер равны 0
    while twist != 0 or flip != 0 or slice != 0:

        if depth_mod3 == 0:
            depth_mod3 = 3
        # для текущего состояния применяем всех ходы поочередно
        # и вычисляем количество ходов небходимое для достижения Фазы 2
        for move in range(18):
            cub.move(move)
            twist1 = cub.get_corners_twist()
            flip1 = cub.get_edges_flip()
            slice1 = cub.get_ud_slice_sorted() // 24
            fs1 = 2048 * slice1 + flip1
            classidx1 = tb.fs_classidx[fs1][0]
            sym = tb.fs_classidx[fs1][1]
            if tb.get_fs_twist_depth3(2187 * classidx1 + tb.conj_twist[twist1][sym]) == depth_mod3 - 1:
                depth += 1
                twist = twist1
                flip = flip1
                slice = slice1
                depth_mod3 = depth_mod3 - 1
                break
            cub.move(u.INV_MOVE[move])
    return depth


def get_phase2_depth(cubie):

    corners = cubie.get_corners()
    ud_edges = cubie.get_ud_edges()

    classidx = tb.co_classidx[corners][0]
    sym = tb.co_classidx[corners][1]
    depth_mod3 = tb.get_co_ud_edges_depth3(40320 * classidx + tb.conj_ud_edges[ud_edges][sym])

    if depth_mod3 == 3:
        return 11

    depth = 0
    while corners != 0 or ud_edges != 0:

        if depth_mod3 == 0:
            depth_mod3 = 3

        for move in u.PHASE2_MOVES:

            corners1 = tb.move_corners[corners][move]
            ud_edges1 = tb.move_ud_edges[ud_edges][move]

            classidx1 = tb.co_classidx[corners1][0]
            sym = tb.co_classidx[corners1][1]

            if tb.get_co_ud_edges_depth3(40320 * classidx1 + tb.conj_ud_edges[ud_edges1][sym]) == depth_mod3 - 1:
                depth += 1
                corners = corners1
                ud_edges = ud_edges1
                depth_mod3 = depth_mod3 - 1
                break
    return depth
