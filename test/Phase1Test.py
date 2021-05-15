
import unittest
from rubik.Tables import *
from rubik.Utils import get_random_cubie, get_random_cubie_2
import rubik.CubieCube as cc
import rubik.CoordCubie as coord


class Phase1Test(unittest.TestCase):

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

