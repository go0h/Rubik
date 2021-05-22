import rubik.CubieCube as cc
import rubik.CoordCubie as crd
import rubik.Utils as u
import rubik.Tables as tb
from datetime import datetime


class TwoPhaseSolverSlow:

    def __init__(self, cubie: cc.CubieCube):
        self.cubie = cubie
        self.coord_cubie = crd.CoordCubie(self.cubie)
        self.corner_save = 0
        self.moves_p1 = []
        self.moves_p2 = []
        self.solved = False

        self.start_phase1_time = None
        self.end_phase1_time = None
        self.end_phase2_time = None

    def solve(self) -> list:

        phase1_dist = self.coord_cubie.get_phase1_depth()

        self.start_phase1_time = datetime.now()
        self.search_phase1(self.cubie, phase1_dist, phase1_dist)

        p1 = self.end_phase1_time - self.start_phase1_time
        p2 = self.end_phase2_time - self.end_phase1_time
        all = p1 + p2
        print(f"PHASE_1 = {p1}s")
        print(f"PHASE_2 = {p2}s")
        print(f"ALL = {all}")

        return list(map(lambda x: u.MOVES_S[x], self.moves_p1)) + \
               list(map(lambda x: u.MOVES_S[x], self.moves_p2))

    def search_phase1(self, cubie, phase1_dist, left):

        if cubie.get_corners_twist() == 0 and \
                cubie.get_edges_flip() == 0 and \
                cubie.get_ud_slice_sorted() < 24 and left == 0:

            ud_edges = cubie.get_ud_edges()
            corners = cubie.get_corners()

            dist2 = self.coord_cubie.get_phase2_depth(corners, ud_edges)
            self.end_phase1_time = datetime.now()
            for left in range(dist2, 30 - phase1_dist):
                self.search_phase2(cubie, dist2, left)
                if self.solved:
                    self.end_phase2_time = datetime.now()
                    break
                else:
                    self.moves_p2 = []

        else:
            temp = cc.CubieCube(cubie.corners, cubie.edges)
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

                temp.move(move)

                twist1 = temp.get_corners_twist()
                flip1 = temp.get_edges_flip()
                slice_sorted1 = temp.get_ud_slice_sorted()

                fs = 2048 * (slice_sorted1 // 24) + flip1
                classidx1 = tb.fs_classidx[fs]
                sym = tb.fs_sym[fs]
                dist_mod3 = tb.get_fs_twist_depth3(2187 * classidx1 + tb.twist_conj[(twist1 << 4) + sym])
                dist1 = tb.distance[3 * phase1_dist + dist_mod3]

                if dist1 >= left:
                    temp.move(u.INV_MOVE[move])
                    continue

                self.moves_p1.append(move)
                self.search_phase1(temp, dist1, left - 1)

                if not u.check_cubie_in_phase2(self.cubie, self.moves_p1):
                    self.moves_p1.pop(-1)
                    temp.move(u.INV_MOVE[move])
                if self.solved:
                    break

    def search_phase2(self, cubie, dist2, left):

        if cubie.solved():
            self.solved = True
            return

        temp = cc.CubieCube(cubie.corners, cubie.edges)
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
            temp.move(move)

            ud_edges = temp.get_ud_edges()
            corners = temp.get_corners()

            classidx = tb.co_classidx[corners]
            sym = tb.co_sym[corners]
            dist_mod3 = tb.get_co_ud_edges_depth3(40320 * classidx + tb.conj_ud_edges[(ud_edges << 4) + sym])

            dist2_new = tb.distance[3 * dist2 + dist_mod3]
            if dist2_new >= left:
                temp.move(u.INV_MOVE[move])
                continue

            self.moves_p2.append(move)
            self.search_phase2(temp, dist2_new, left - 1)
            if not self.solved:
                self.moves_p2.pop(-1)
                temp.move(u.INV_MOVE[move])
            else:
                break
