import unittest
import rubik.CubieCube as cc
import rubik.FaceletCube as fc
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
        num_tests = 1000
        max_moves = 0
        avg_scramble = 0
        avg_solution = 0
        for i in range(num_tests):
            print(f"TEST #{i}")
            scramble = cc.get_random_moves()

            cubie = cc.CubieCube()
            cubie.apply_moves(scramble)

            face = fc.FaceletCube()
            face.apply_moves(scramble)

            solver = tfs.TwoPhaseSolver(cubie)
            moves = solver.solve()

            max_moves = max(len(moves), max_moves)
            avg_scramble += len(scramble)
            avg_solution += len(moves)

            scramble = ' '.join([i for i in moves])
            cubie.scramble(scramble)
            face.scramble(scramble)

            self.assertTrue(cubie.solved())
            self.assertTrue(face.solved())

        print(f"AVG scramble = {round(avg_scramble / num_tests)}")
        print(f"AVG solution = {round(avg_solution / num_tests)}")
        print(f"MAX moves    = {max_moves}")

    def test_special_cases_1(self):

        for scramble in [SUPER_FLIP, PONS_ASINORUM_SUPER_FLIP, PONS_ASINORUM]:
            cubie = cc.CubieCube()
            cubie.scramble(scramble)

            solver = tfs.TwoPhaseSolver(cubie)
            moves = solver.solve()
            scramble = ' '.join([i for i in moves])

            cubie.scramble(scramble)

            self.assertTrue(cubie.solved())
