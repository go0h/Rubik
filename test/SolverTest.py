import unittest
import rubik.CubieCube as cc
import solver.TwoPhaseSolver as tfs
from rubik.Utils import *
from rubik.Edge import UR, UF, UL, UB, DR, DF, DL, DB, FR, FL, BL, BR

class CubieCubeTest(unittest.TestCase):

    def test_phase_1(self):

        for _ in range(100):
            cubie = get_random_cubie()
            solver = tfs.TwoPhaseSolver(cubie)

            phase1_dist = solver.coord_cubie.get_phase1_depth()
            print(f"phase1_dist = {phase1_dist}")

            solver.search_phase1(solver.coord_cubie.corner_twist,
                                 solver.coord_cubie.edge_flip,
                                 solver.coord_cubie.slice_sorted,
                                 phase1_dist,
                                 phase1_dist)

            self.assertTrue(check_cubie_in_phase2(cubie, solver.moves_p1))

    def test_solve(self):

        cubie = get_random_cubie()
        solver = tfs.TwoPhaseSolver(cubie)

        scramble = moves_to_scramble(solver.solve())

        print(scramble)
        # cubie.scramble(scramble)

        # self.assertTrue(cubie.solved())
