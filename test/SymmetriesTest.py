
import unittest
import rubik.CubieCube as cc
from rubik.Symmetries import BASIC_SYM_CUBE, S_URF3, S_F2, S_U4, S_LR2, SYM_CUBIES, INV_IDX


class SymmetriesTest(unittest.TestCase):

    def test_URF3(self):
        c1 = cc.CubieCube()
        c2 = cc.CubieCube()
        for _ in range(3):
            c1.multiply(BASIC_SYM_CUBE[S_URF3])
        self.assertEqual(c1, c2)

    def test_F2(self):
        c1 = cc.CubieCube()
        c2 = cc.CubieCube()
        for _ in range(2):
            c1.multiply(BASIC_SYM_CUBE[S_F2])
        self.assertEqual(c1, c2)

    def test_U4(self):
        c1 = cc.CubieCube()
        c2 = cc.CubieCube()
        for _ in range(4):
            c1.multiply(BASIC_SYM_CUBE[S_U4])
        self.assertEqual(c1, c2)

    def test_LR2(self):
        c1 = cc.CubieCube()
        c2 = cc.CubieCube()
        for _ in range(2):
            c1.multiply(BASIC_SYM_CUBE[S_LR2])
        self.assertEqual(c1, c2)

    def test_inverse_symmetry(self):
        for n in range(48):
            c1 = cc.CubieCube()
            c2 = cc.CubieCube()
            c2.multiply(SYM_CUBIES[n])
            c2.multiply(SYM_CUBIES[INV_IDX[n]])
            self.assertEqual(c1, c2)
