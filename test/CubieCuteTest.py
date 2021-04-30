import unittest

from rubik.FaceletCube import FaceletCube
from rubik.CubieCube import CubieCube
from rubik.Colors import *
from rubik.Side import Side


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
