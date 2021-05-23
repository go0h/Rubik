import rubik.CubieCube as cc
from rubik.CoordCubie import get_phase1_depth, get_phase2_depth
from rubik.Utils import MOVES, PHASE2_MOVES, MOVES_S, INV_MOVE
import rubik.Tables as tb
from datetime import datetime


class TwoPhaseSolver:

    def __init__(self, cubie: cc.CubieCube):
        self.cubie = cubie
        self.moves_p1 = []
        self.moves_p2 = []
        self.solved = False

        self.start_phase1_time = None
        self.end_phase1_time = None
        self.end_phase2_time = None

    def solve(self) -> list:

        phase1_dist = get_phase1_depth(self.cubie)

        self.start_phase1_time = datetime.now()

        cubie = cc.CubieCube(self.cubie.corners, self.cubie.edges)
        self.search_phase1(cubie, phase1_dist, phase1_dist)

        p1 = self.end_phase1_time - self.start_phase1_time
        p2 = self.end_phase2_time - self.end_phase1_time
        all = p1 + p2
        print(f"PHASE_1 = {p1}s")
        print(f"PHASE_2 = {p2}s")
        print(f"ALL = {all}")

        return [MOVES_S[x] for x in self.moves_p1 + self.moves_p2]

    def search_phase1(self, cubie, phase1_dist, left):

        if cubie.get_corners_twist() == 0 and \
                cubie.get_edges_flip() == 0 and \
                cubie.get_ud_slice_sorted() < 24 and left == 0:

            dist2 = get_phase2_depth(cubie)
            self.end_phase1_time = datetime.now()
            for left in range(dist2, 30 - phase1_dist):
                self.search_phase2(cubie, dist2, left)
                if self.solved:
                    self.end_phase2_time = datetime.now()
                    break
                else:
                    self.moves_p2 = []

        else:
            for move in MOVES:
                if phase1_dist == 0 and left < 5 and move in PHASE2_MOVES:
                    continue

                # исключаем из последовательности взаимоисклюдающие действия
                # или не влияющие друг на друга действия
                # пример одна сторона U - U' - U2 или противоположные стороны U - D
                if len(self.moves_p1) > 0:
                    last = self.moves_p1[-1] // 3 - move // 3
                    if last == 0 or last == 3:
                        continue
                cubie.move(move)

                twist1 = cubie.get_corners_twist()
                flip1 = cubie.get_edges_flip()
                slice_sorted1 = cubie.get_ud_slice_sorted()

                fs = 2048 * (slice_sorted1 // 24) + flip1
                classidx1 = tb.fs_classidx[fs][0]
                sym = tb.fs_classidx[fs][1]
                dist_mod3 = tb.get_fs_twist_depth3(2187 * classidx1 + tb.conj_twist[twist1][sym])
                dist1 = tb.distance[3 * phase1_dist + dist_mod3]

                if dist1 >= left:
                    cubie.move(INV_MOVE[move])
                    continue

                self.moves_p1.append(move)
                self.search_phase1(cubie, dist1, left - 1)

                if not cubie.check_in_phase2():
                    self.moves_p1.pop(-1)
                    cubie.move(INV_MOVE[move])
                if self.solved:
                    break

    def search_phase2(self, cubie, dist2, left):

        if cubie.solved():
            self.solved = True
            return

        for move in PHASE2_MOVES:

            if len(self.moves_p2) > 0:
                last = self.moves_p2[-1] // 3 - move // 3
                if last == 0 or last == 3:
                    continue
            else:
                if len(self.moves_p1) > 0:
                    last = self.moves_p1[-1] // 3 - move // 3
                    if last == 0 or last == 3:
                        continue
            cubie.move(move)

            ud_edges = cubie.get_ud_edges()
            corners = cubie.get_corners()

            classidx = tb.co_classidx[corners][0]
            sym = tb.co_classidx[corners][1]
            dist_mod3 = tb.get_co_ud_edges_depth3(40320 * classidx + tb.conj_ud_edges[ud_edges][sym])

            dist2_new = tb.distance[3 * dist2 + dist_mod3]
            if dist2_new >= left:
                cubie.move(INV_MOVE[move])
                continue

            self.moves_p2.append(move)
            self.search_phase2(cubie, dist2_new, left - 1)
            if not self.solved:
                self.moves_p2.pop(-1)
                cubie.move(INV_MOVE[move])
            else:
                break
