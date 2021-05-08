import unittest
from rubik.Utils import *
from rubik.Edge import UR, UF, UL, UB, DR, DF, DL, DB, FR, FL, BL, BR


class CubieCubeTest(unittest.TestCase):

    def test_eq(self):
        cubie1 = cc.CubieCube()
        cubie2 = cc.CubieCube()
        self.assertEqual(cubie1, cubie2)

        cubie1.edges[1].rotate(1, 3)
        self.assertFalse(cubie1 == cubie2, "FAIL NOT EQUAL CUBIECUBE")

    def test_cubiecube_to_facelet_1(self):

        cubie = cc.CubieCube()
        f1 = fc.FaceletCube()
        f2 = cubie.to_facelet_cube()

        self.assertEqual(f1, f2)

    def test_facelet_to_cubie_1(self):
        facelet = fc.FaceletCube()
        c1 = cc.CubieCube()
        c2 = facelet.to_cubie_cube()
        self.assertEqual(c1, c2)

    def test_facelet_to_cubie_2(self):
        f1 = fc.FaceletCube()
        f1.scramble("L' F D2 U' B2 L' B R' F' L' D2 L F L2 U F' L' B' U' L B D F L R D2 U2 L' R D'")
        c1 = f1.to_cubie_cube()
        f2 = c1.to_facelet_cube()
        self.assertEqual(f2, f1)

    def test_random_facelet_to_cubie(self):

        for _ in range(150):
            f1 = get_random_facelet()

            c1 = f1.to_cubie_cube()
            f2 = c1.to_facelet_cube()
            self.assertEqual(f1, f2)

            c2 = f2.to_cubie_cube()
            self.assertEqual(c1, c2)

    def test_all_rotation(self):

        for move in MOVES:
            f1 = fc.FaceletCube()
            f1.scramble(move)

            c1 = cc.CubieCube()
            c1.scramble(move)

            f2 = c1.to_facelet_cube()
            c2 = f1.to_cubie_cube()

            self.assertEqual(f1, f2)
            self.assertEqual(c1, c2)

    def test_random_rotation(self):

        for _ in range(150):
            scramble = get_random_scramble()

            f1 = fc.FaceletCube()
            f1.scramble(scramble)

            c1 = cc.CubieCube()
            c1.scramble(scramble)

            f2 = c1.to_facelet_cube()
            c2 = f1.to_cubie_cube()

            self.assertEqual(f1, f2)
            self.assertEqual(c1, c2)

    def test_inverse_cubie(self):

        c1 = get_random_cubie()
        c2 = cc.CubieCube()
        c1.inverse_cubie(c2)

        c3 = cc.CubieCube()
        c2.inverse_cubie(c3)
        self.assertEqual(c1, c3)

    def test_ud_slice_coord_1(self):
        c = cc.CubieCube()
        self.assertEqual(c.get_ud_slice_coord(), 0)

    def test_ud_slice_coord_2(self):
        c = cc.CubieCube()
        c.scramble("R F L")
        print(c)
        self.assertEqual(c.get_ud_slice_coord(), 493)

    def test_edges_coord(self):
        for _ in range(150):
            c = get_random_cubie()
            self.assertEqual(c.get_ud_slice_coord(), c.__edges_coord__(FR, BR))
            self.assertEqual(c.get_ud_slice_sorted(), c.__get_edges__(FR, BR))

    def test_u_edges_coord(self):
        c = cc.CubieCube()
        self.assertEqual(1656, c.get_u_edges())
        arr = []
        for _ in range(150):
            c = get_random_cubie()
            arr.append(c.get_u_edges())
        m = max(arr)
        print(m)
        self.assertTrue(m < 11880)

    def test_d_edges_coord(self):
        c = cc.CubieCube()
        self.assertEqual(0, c.get_d_edges())
        arr = []
        for _ in range(150):
            c = get_random_cubie()
            arr.append(c.get_d_edges())
        m = max(arr)
        print(m)
        self.assertTrue(m < 11880)

    def test_ud_edges_coord_phase2(self):
        arr = []
        for _ in range(150):
            c = get_random_cubie_2()
            arr.append(c.get_ud_slice_sorted())
        m = max(arr)
        print(m)
        self.assertTrue(m < 24)

    def test_u_edges_coord_phase2(self):
        arr = []
        for _ in range(150):
            c = get_random_cubie_2()
            arr.append(c.get_u_edges())
        m = max(arr)
        print(m)
        self.assertTrue(m < 1680)

    def test_d_edges_coord_phase2(self):
        arr = []
        for _ in range(150):
            c = get_random_cubie_2()
            arr.append(c.get_d_edges())
        m = max(arr)
        print(m)
        self.assertTrue(m < 1680)

    def test_corner_perm(self):
        arr = []
        for _ in range(150):
            c = get_random_cubie()
            arr.append(c.get_corner())
        m = max(arr)
        print(m)
        self.assertTrue(m < 40320)

    def test_corner_perm_phase2(self):
        arr = []
        for _ in range(150):
            c = get_random_cubie_2()
            arr.append(c.get_corner())
        m = max(arr)
        print(m)
        self.assertTrue(m < 40320)

    def test_ud_edges_perm_phase2(self):
        arr = []
        for _ in range(150):
            c = get_random_cubie_2()
            arr.append(c.get_ud_edges())
        m = max(arr)
        print(m)
        self.assertTrue(m < 40320)