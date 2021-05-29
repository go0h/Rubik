import unittest
import rubik.CubieCube as cc
import solver.TwoPhaseSolver as tfs
from rubik.Utils import *


class CubieCubeTest(unittest.TestCase):

    def test_get_depth_p1_1(self):

        for _ in range(1000):
            cubie = cc.get_random_cubie()
            self.assertTrue(tfs.get_phase1_depth(cubie) <= 12)

    def test_get_depth_p1_2(self):

        for _ in range(1000):
            cubie = cc.get_random_cubie_2()
            self.assertTrue(tfs.get_phase1_depth(cubie) == 0)

    def test_phase_1(self):

        for i in range(1000):
            print(f"TEST #{i}")
            cubie = cc.get_random_cubie()
            solver = tfs.TwoPhaseSolver(cubie)

            phase1_dist = tfs.get_phase1_depth(cubie)

            cubie2 = cc.CubieCube(cubie.corners, cubie.edges)
            solver.search_phase1(cubie.get_corners_twist(),
                                 cubie.get_edges_flip(),
                                 cubie.get_ud_slice_sorted(),
                                 phase1_dist,
                                 phase1_dist)

            cubie2.apply_moves(solver.moves_p1)

            self.assertTrue(cubie2.check_in_phase2())

    def test_solve(self):

        for i in range(1000):
            print(f"TEST #{i}")

            cubie = cc.get_random_cubie()
            solver = tfs.TwoPhaseSolver(cubie)

            moves = solver.solve()
            scramble = ' '.join([i for i in moves])

            cubie.scramble(scramble)

            self.assertTrue(cubie.solved())

    def test_special_cases_1(self):

        for scramble in [SUPER_FLIP, PONS_ASINORUM_SUPER_FLIP, PONS_ASINORUM]:
            cubie = cc.CubieCube()
            cubie.scramble(scramble)

            solver = tfs.TwoPhaseSolver(cubie)
            moves = solver.solve()
            scramble = ' '.join([i for i in moves])

            cubie.scramble(scramble)

            self.assertTrue(cubie.solved())