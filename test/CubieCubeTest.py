import unittest
import rubik.Utils as u
import rubik.CubieCube as cc
import rubik.FaceletCube as fc


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
            f1 = u.get_random_facelet()

            c1 = f1.to_cubie_cube()
            f2 = c1.to_facelet_cube()
            self.assertEqual(f1, f2)

            c2 = f2.to_cubie_cube()
            self.assertEqual(c1, c2)

    def test_all_rotation(self):

        for move in u.MOVES_S:
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
            scramble = u.get_random_scramble()

            f1 = fc.FaceletCube()
            f1.scramble(scramble)

            c1 = cc.CubieCube()
            c1.scramble(scramble)

            f2 = c1.to_facelet_cube()
            c2 = f1.to_cubie_cube()

            self.assertEqual(f1, f2)
            self.assertEqual(c1, c2)

    def test_ud_slice_coord_1(self):
        c = cc.CubieCube()
        self.assertEqual(c.get_ud_slice_coord(), 0)

    def test_ud_slice_coord_2(self):
        c = cc.CubieCube()
        c.scramble("R F L")
        print(c)
        self.assertEqual(c.get_ud_slice_coord(), 493)

    def test_ud_edges_coord_phase2(self):
        arr = []
        for _ in range(150):
            c = u.get_random_cubie_2()
            arr.append(c.get_ud_slice_sorted())
        m = max(arr)
        print(m)
        self.assertTrue(m < 24)

    def test_corner_perm(self):
        arr = []
        for _ in range(1):
            c = u.get_random_cubie()
            arr.append(c.get_corners())
        m = max(arr)
        print(m)
        self.assertTrue(m < 40320)

    def test_corner_perm_phase2(self):
        arr = []
        for _ in range(150):
            c = u.get_random_cubie_2()
            arr.append(c.get_corners())
        m = max(arr)
        print(m)
        self.assertTrue(m < 40320)

    def test_ud_edges_perm_phase2(self):
        arr = []
        for _ in range(150):
            c = u.get_random_cubie_2()
            arr.append(c.get_ud_edges())
        m = max(arr)
        print(m)
        self.assertTrue(m < 40320)

    def test_random_phase2_cube(self):
        for _ in range(100):
            c = u.get_random_cubie_2()
            self.assertTrue(c.get_edges_flip() == 0 and \
                            c.get_corners_twist() == 0 and \
                            c.get_ud_slice_coord() == 0)
