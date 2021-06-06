import rubik.CubieCube as cc
import rubik.Utils as u
import rubik.Tables as t
from copy import deepcopy
from datetime import datetime


class TwoPhaseSolver:

    def __init__(self, cubie: cc.CubieCube, max_moves=None):
        self.cubie = deepcopy(cubie)
        self.moves_p1 = []
        self.moves_p2 = []
        self.solutions = []
        self.solved = False

        if max_moves is None:
            self.max_moves = 40
        else:
            self.max_moves = max_moves

        self.start_phase1_time = None
        self.end_phase1_time = None
        self.end_phase2_time = None

    def solve(self, debug=False, print_moves=False) -> list:

        self.start_phase1_time = datetime.now()

        phase1_dist = get_phase1_depth(self.cubie)

        for left in range(phase1_dist, 13):
            self.search_phase1(self.cubie.get_corners_twist(),
                               self.cubie.get_edges_flip(),
                               self.cubie.get_ud_slice_sorted(),
                               phase1_dist,
                               left)
            if self.solved:
                break
            self.moves_p1 = []
            self.moves_p2 = []

        if debug or print_moves:
            time_p1 = self.end_phase1_time - self.start_phase1_time
            time_p2 = self.end_phase2_time - self.end_phase1_time
            total_time = time_p1 + time_p2

            print("Initial permutation:")
            print(self.cubie.to_facelet_cube())

            debug_cubie = deepcopy(self.cubie)

            print(f"Phase 1 permutation: {u.moves_to_scramble(self.moves_p1)}")
            if print_moves:
                for m in self.moves_p1:
                    print(f"Move {u.MOVES_S[m]}")
                    debug_cubie.move(m)
                    print(debug_cubie.to_facelet_cube())
            else:
                debug_cubie.apply_moves(self.moves_p1)
                print(debug_cubie.to_facelet_cube())
            print(f"Time spend on Phase 1 = {time_p1}s")

            print(f"Phase 2 permutation: {u.moves_to_scramble(self.moves_p2)}")
            if print_moves:
                for m in self.moves_p2:
                    print(f"Move {u.MOVES_S[m]}")
                    debug_cubie.move(m)
                    print(debug_cubie.to_facelet_cube())
            else:
                debug_cubie.apply_moves(self.moves_p2)
                print(debug_cubie.to_facelet_cube())
            print(f"Time spend on Phase 2 = {time_p2}s")

            print(f"Total time spend = {total_time}")
            print(f"Total moves = {len(self.moves_p1) + len(self.moves_p2)}")

        return [u.MOVES_S[x] for x in self.moves_p1 + self.moves_p2]

    def search_phase1(self, twist, flip, slice_sorted, phase1_dist, left):

        if twist == 0 and flip == 0 and slice_sorted < 24 and left == 0:

            temp = deepcopy(self.cubie)
            temp.apply_moves(self.moves_p1)

            ud_edges = temp.get_ud_edges()
            corners = temp.get_corners()
            dist2 = get_phase2_depth(temp)

            self.end_phase1_time = datetime.now()
            for left in range(dist2, self.max_moves - len(self.moves_p1) + 1):
                self.search_phase2(corners, ud_edges, slice_sorted, left)
                if self.solved:
                    self.end_phase2_time = datetime.now()
                    break
                else:
                    self.moves_p2 = []

        else:
            for move in u.MOVES:
                if phase1_dist == 0 and left < 5 and move in u.PHASE2_MOVES:
                    continue

                # исключаем из последовательности взаимоисклюдающие действия
                # или не влияющие друг на друга действия
                # пример одна сторона U - U' - U2 или противоположные стороны U - D
                if len(self.moves_p1) > 0:
                    last = self.moves_p1[-1] // 3 - move // 3
                    if last == 0 or last == 3:
                        continue

                twist1 = t.move_twist[twist][move]
                flip1 = t.move_flip[flip][move]
                slice_sorted1 = t.move_slice_sorted[slice_sorted][move]

                fs = 2048 * (slice_sorted1 // 24) + flip1
                classidx1 = t.fs_classidx[fs][0]
                sym = t.fs_classidx[fs][1]
                dist1 = t.phase1_prun[classidx1][t.conj_twist[twist1][sym]]

                if dist1 >= left:
                    continue

                self.moves_p1.append(move)
                self.search_phase1(twist1, flip1, slice_sorted1, dist1, left - 1)
                if self.solved:
                    break
                else:
                    self.moves_p1.pop(-1)

    def search_phase2(self, corners, ud_edges, slice_sorted, left):

        if corners == 0 and ud_edges == 0 and slice_sorted == 0 and not self.solved:
            solution = u.moves_to_scramble(self.moves_p1 + self.moves_p2)
            if solution not in self.solutions:
                self.solutions += [solution]
                if len(self.moves_p1) + len(self.moves_p2) <= self.max_moves:
                    self.solved = True
            return
        elif left == 0:
            return

        for move in u.PHASE2_MOVES:
            if len(self.moves_p2) > 0:
                last = self.moves_p2[-1] // 3 - move // 3
                if last == 0 or last == 3:
                    continue
            else:
                if len(self.moves_p1) > 0:
                    last = self.moves_p1[-1] // 3 - move // 3
                    if last == 0 or last == 3:
                        continue

            corners1 = t.move_corners[corners][move]
            ud_edges1 = t.move_ud_edges[ud_edges][move]
            slice_sorted1 = t.move_slice_sorted[slice_sorted][move]

            classidx = t.co_classidx[corners1][0]
            sym = t.co_classidx[corners1][1]
            dist2_new = t.phase2_prun[classidx][t.conj_ud_edges[ud_edges1][sym]]

            if dist2_new >= left:
                continue

            self.moves_p2.append(move)
            self.search_phase2(corners1, ud_edges1, slice_sorted1, left - 1)
            if not self.solved:
                self.moves_p2.pop(-1)
            else:
                break


def get_phase1_depth(cubie):
    """@:return Минимальное количество ходов требуемое для достижения рандомного кубика фазы 2"""

    slice = cubie.get_ud_slice_sorted() // 24
    flip = cubie.get_edges_flip()
    twist = cubie.get_corners_twist()

    fs = (slice << 11) + flip
    classidx = t.fs_classidx[fs][0]
    sym = t.fs_classidx[fs][1]
    # 3^7 * класс экв + ориентация 8 углов

    depth = 0
    depth_end = t.phase1_prun[classidx][t.conj_twist[twist][sym]]
    # первая фаза, считается законченой, когда ориентации всех углов и ребер равны 0
    while twist != 0 or flip != 0 or slice != 0:

        # для текущего состояния применяем всех ходы поочередно
        # и вычисляем количество ходов небходимое для достижения Фазы 2
        for move in u.MOVES:

            twist1 = t.move_twist[twist][move]
            flip1 = t.move_flip[flip][move]
            slice1 = t.move_slice_sorted[24 * slice][move] // 24

            fs1 = (slice1 << 11) + flip1
            classidx1 = t.fs_classidx[fs1][0]
            sym = t.fs_classidx[fs1][1]

            if t.phase1_prun[classidx1][t.conj_twist[twist1][sym]] == depth_end - 1:
                depth += 1
                twist = twist1
                flip = flip1
                slice = slice1
                depth_end = depth_end - 1
                break
    return depth


def get_phase2_depth(cubie):

    corners = cubie.get_corners()
    ud_edges = cubie.get_ud_edges()

    classidx = t.co_classidx[corners][0]
    sym = t.co_classidx[corners][1]
    depth_end = t.phase2_prun[classidx][t.conj_ud_edges[ud_edges][sym]]

    if depth_end == 20:
        return 11

    depth = 0
    while corners != 0 or ud_edges != 0:

        for move in u.PHASE2_MOVES:

            corners1 = t.move_corners[corners][move]
            ud_edges1 = t.move_ud_edges[ud_edges][move]

            classidx1 = t.co_classidx[corners1][0]
            sym = t.co_classidx[corners1][1]

            if t.phase2_prun[classidx1][t.conj_ud_edges[ud_edges1][sym]] == depth_end - 1:
                depth += 1
                corners = corners1
                ud_edges = ud_edges1
                depth_end = depth_end - 1
                break
    return depth
