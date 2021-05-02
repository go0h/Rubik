import unittest

from rubik.Utils import *


class CubieCubeTest(unittest.TestCase):

    def test_eq(self):
        cubie1 = CubieCube()
        cubie2 = CubieCube()
        self.assertEqual(cubie1, cubie2)

        cubie1.edges[1].rotate(1, 3)
        self.assertFalse(cubie1 == cubie2, "FAIL NOT EQUAL CUBIECUBE")

    def test_cubiecube_to_facelet_1(self):

        cubie = CubieCube()
        f1 = FaceletCube()
        f2 = cubie.to_facelet_cube()

        self.assertEqual(f1, f2)

    def test_facelet_to_cubie_1(self):
        facelet = FaceletCube()
        c1 = CubieCube()
        c2 = facelet.to_cubie_cube()
        self.assertEqual(c1, c2)

    def test_facelet_to_cubie_2(self):
        f1 = FaceletCube()
        f1.scramble("L' F D2 U' B2 L' B R' F' L' D2 L F L2 U F' L' B' U' L B D F L R D2 U2 L' R D'")
        c1 = f1.to_cubie_cube()
        f2 = c1.to_facelet_cube()
        self.assertEqual(f2, f1)

    def test_random_facelet_to_cubie(self):

        for _ in range(200):
            f1 = get_random_facelet()

            c1 = f1.to_cubie_cube()
            f2 = c1.to_facelet_cube()
            self.assertEqual(f1, f2)

            c2 = f2.to_cubie_cube()
            self.assertEqual(c1, c2)

    def test_all_rotation(self):

        for move in MOVES:
            f1 = FaceletCube()
            f1.scramble(move)

            c1 = CubieCube()
            c1.scramble(move)

            f2 = c1.to_facelet_cube()
            c2 = f1.to_cubie_cube()

            self.assertEqual(f1, f2)
            self.assertEqual(c1, c2)

    def test_random_rotation(self):

        for _ in range(200):
            scramble = get_random_scramble()

            f1 = FaceletCube()
            f1.scramble(scramble)

            c1 = CubieCube()
            c1.scramble(scramble)

            f2 = c1.to_facelet_cube()
            c2 = f1.to_cubie_cube()

            self.assertEqual(f1, f2)
            self.assertEqual(c1, c2)
