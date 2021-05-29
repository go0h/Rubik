import rubik.CubieCube as cc
import rubik.CoordCubie as crd
import rubik.Utils as u
import rubik.Tables as tb
from copy import deepcopy
from datetime import datetime


class TwoPhaseSolver:

    def __init__(self, cubie: cc.CubieCube):
        self.cubie = deepcopy(cubie)
        self.moves_p1 = []
        self.moves_p2 = []
        self.solved = False

        self.start_phase1_time = None
        self.end_phase1_time = None
        self.end_phase2_time = None

    def solve(self) -> list:

        self.start_phase1_time = datetime.now()

        phase1_dist = crd.get_phase1_depth(self.cubie)

        self.search_phase1(self.cubie.get_corners_twist(),
                           self.cubie.get_edges_flip(),
                           self.cubie.get_ud_slice_sorted(),
                           phase1_dist,
                           phase1_dist)

        p1 = self.end_phase1_time - self.start_phase1_time
        p2 = self.end_phase2_time - self.end_phase1_time
        all = p1 + p2
        print(f"PHASE_1 = {p1}s")
        print(f"PHASE_2 = {p2}s")
        print(f"ALL = {all}")

        return [u.MOVES_S[x] for x in self.moves_p1 + self.moves_p2]

    def search_phase1(self, twist, flip, slice_sorted, phase1_dist, left):

        if twist == 0 and flip == 0 and slice_sorted < 24 and left == 0:

            temp = deepcopy(self.cubie)
            temp.apply_moves(self.moves_p1)

            ud_edges = temp.get_ud_edges()
            corners = temp.get_corners()

            dist2 = crd.get_phase2_depth(temp)

            self.end_phase1_time = datetime.now()
            for left in range(dist2, 30 - phase1_dist):
                self.search_phase2(corners, ud_edges, slice_sorted, dist2, left)
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

                twist1 = tb.move_twist[twist][move]
                flip1 = tb.move_flip[flip][move]
                slice_sorted1 = tb.move_slice_sorted[slice_sorted][move]

                fs = 2048 * (slice_sorted1 // 24) + flip1
                classidx1 = tb.fs_classidx[fs][0]
                sym = tb.fs_classidx[fs][1]
                dist_mod3 = tb.get_fs_twist_depth3(2187 * classidx1 + tb.conj_twist[twist1][sym])
                dist1 = tb.distance[3 * phase1_dist + dist_mod3]

                if dist1 >= left:
                    continue

                self.moves_p1.append(move)
                self.search_phase1(twist1, flip1, slice_sorted1, dist1, left - 1)
                if not u.check_cubie_in_phase2(self.cubie, self.moves_p1):
                    self.moves_p1.pop(-1)
                if self.solved:
                    break

    def search_phase2(self, corners, ud_edges, slice_sorted, dist2, left):

        if corners == 0 and ud_edges == 0 and slice_sorted == 0 and not self.solved:
            self.solved = True
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

            corners1 = tb.move_corners[corners][move]
            ud_edges1 = tb.move_ud_edges[ud_edges][move]
            slice_sorted1 = tb.move_slice_sorted[slice_sorted][move]

            classidx = tb.co_classidx[corners1][0]
            sym = tb.co_classidx[corners1][1]
            dist2_new = tb.phase2_prun[classidx][tb.conj_ud_edges[ud_edges1][sym]]

            if dist2_new >= left:
                continue

            self.moves_p2.append(move)
            self.search_phase2(corners1, ud_edges1, slice_sorted1, dist2_new, left - 1)
            if not self.solved:
                self.moves_p2.pop(-1)
            else:
                break
