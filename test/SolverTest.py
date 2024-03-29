import unittest
import rubik.CubieCube as cc
import rubik.CoordCubie as coord
import solver.TwoPhaseSolver as tfs
from rubik.Utils import *
from rubik.Edge import UR, UF, UL, UB, DR, DF, DL, DB, FR, FL, BL, BR


class CubieCubeTest(unittest.TestCase):

    def test_get_depth_p1_1(self):

        for _ in range(150):
            cubie = get_random_cubie()
            coord_cubie = coord.CoordCubie(cubie)
            self.assertTrue(coord_cubie.get_phase1_depth() <= 12)

    def test_get_depth_p1_2(self):

        for _ in range(150):
            cubie = get_random_cubie_2()
            coord_cubie = coord.CoordCubie(cubie)
            self.assertTrue(coord_cubie.get_phase1_depth() == 0)

    def test_phase_1(self):

        for _ in range(100):
            cubie = get_random_cubie()
            solver = tfs.TwoPhaseSolver(cubie)

            phase1_dist = solver.coord_cubie.get_phase1_depth()

            solver.search_phase1(solver.coord_cubie.corner_twist,
                                 solver.coord_cubie.edge_flip,
                                 solver.coord_cubie.slice_sorted,
                                 phase1_dist,
                                 phase1_dist)

            self.assertTrue(check_cubie_in_phase2(cubie, solver.moves_p1))

    def test_solve(self):

        for _ in range(300):

            cubie = get_random_cubie()
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
