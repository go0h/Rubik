import rubik.CubieCube as cc
import rubik.FaceletCube as fc
import rubik.CoordCubie as crd
import rubik.Utils as u
import rubik.Tables as tb
from copy import deepcopy


class TwoPhaseSolver:

    def __init__(self, cubie: cc.CubieCube):
        self.cubie = deepcopy(cubie)
        self.coord_cubie = crd.CoordCubie(self.cubie)
        self.corner_save = 0
        self.moves_p1 = []
        self.moves_p2 = []
        self.solved = False

    def solve(self) -> list:

        phase1_dist = self.coord_cubie.get_phase1_depth()
        print(f"phase1_dist = {phase1_dist}")

        self.search_phase1(self.coord_cubie.corner_twist,
                           self.coord_cubie.edge_flip,
                           self.coord_cubie.slice_sorted,
                           phase1_dist,
                           phase1_dist)

        s1 = u.moves_to_scramble(self.moves_p1)
        s2 = u.moves_to_scramble(self.moves_p2)
        print(f"phase1 = {s1}")
        print(f"phase2 = {s2}")

        return list(map(lambda x: u.MOVES_S[x], self.moves_p1)) + \
               list(map(lambda x: u.MOVES_S[x], self.moves_p2))

    def search_phase1(self, twist, flip, slice_sorted, phase1_dist, togo1):

        if twist == 0 and flip == 0 and slice_sorted < 24 and togo1 == 0:

            last_move = 0
            if self.moves_p1:
                last_move = self.moves_p1[-1]

            corners = None
            if last_move in [5, 8, 14, 17]:
                corners = tb.move_corners[18 * self.corner_save + last_move - 1]
            else:
                corners = self.coord_cubie.corners
                for move in self.moves_p1:
                    corners = tb.move_corners[18 * corners + move]
                self.corner_save = corners

            print(u.moves_to_scramble(self.moves_p1))
            temp = deepcopy(self.cubie)
            for move in self.moves_p1:
                temp.move(u.MOVES_S[move])
            print("PHASE 2 PREPARE")
            print(temp.to_facelet_cube())

            ud_edges = temp.get_ud_edges()
            corners = temp.get_corners()

            dist2 = self.coord_cubie.get_phase2_depth(corners, ud_edges)
            print(f"phase1 is {u.check_cubie_in_phase2(self.cubie, self.moves_p1)}")
            print(u.moves_to_scramble(self.moves_p1))
            print(f"phase2_dist = {dist2}")
            for togo2 in range(dist2, 25 - phase1_dist):
                self.search_phase2(corners, ud_edges, slice_sorted, dist2, togo2)
                if self.solved:
                    break
                else:
                    self.moves_p2 = []

        else:
            for move in u.MOVES:
                if phase1_dist == 0 and togo1 < 5 and move in u.PHASE2_MOVES:
                    continue

                # исключаем из последовательности взаимоисклюдающие действия
                # или не влияющие друг на друга действия
                # пример одна сторона U - U' - U2 или противоположные стороны U - D
                if len(self.moves_p1) > 0:
                    last = self.moves_p1[-1] // 3 - move // 3
                    if last == 0 or last == 3:
                        continue

                twist1 = tb.move_twist[18 * twist + move]
                flip1 = tb.move_flip[18 * flip + move]
                slice_sorted1 = tb.move_slice_sorted[18 * slice_sorted + move]

                fs = 2048 * (slice_sorted1 // 24) + flip1
                classidx1 = tb.fs_classidx[fs]
                sym = tb.fs_sym[fs]
                dist_mod3 = tb.get_fs_twist_depth3(2187 * classidx1 + tb.twist_conj[(twist1 << 4) + sym])
                dist1 = tb.distance[3 * phase1_dist + dist_mod3]

                if dist1 >= togo1:
                    continue

                self.moves_p1.append(move)
                self.search_phase1(twist1, flip1, slice_sorted1, dist1, togo1 - 1)
                if not u.check_cubie_in_phase2(self.cubie, self.moves_p1):
                    self.moves_p1.pop(-1)
                if self.solved:
                    break

    def search_phase2(self, corners, ud_edges, slice_sorted, dist2, togo2):

        if corners == 0 and ud_edges == 0 and slice_sorted == 0 and not self.solved:
            self.solved = True
            print("SOLVED")
            print(u.moves_to_scramble(self.moves_p2) + " " + u.moves_to_scramble(self.moves_p2))
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

            corners1 = tb.move_corners[18 * corners + move]
            ud_edges1 = tb.move_ud_edges[18 * ud_edges + move]
            slice_sorted1 = tb.move_slice_sorted[18 * slice_sorted + move]

            classidx = tb.co_classidx[corners1]
            sym = tb.co_sym[corners1]
            dist_mod3 = tb.get_co_ud_edges_depth3(40320 * classidx + tb.conj_ud_edges[(ud_edges1 << 4) + sym])

            dist2_new = tb.distance[3 * dist2 + dist_mod3]
            # if max(dist2_new, tb.phase2_cornsliceprun[24 * corners1 + slice_sorted1]) >= togo2:
            if dist2_new >= togo2:
                # print(dist2_new, togo2)
                continue

            self.moves_p2.append(move)
            self.search_phase2(corners1, ud_edges1, slice_sorted1, dist2_new, togo2 - 1)
            if not self.solved:
                self.moves_p2.pop(-1)
            else:
                break

