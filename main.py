from rubik.FaceletCube import FaceletCube
from rubik.CubieCube import CubieCube
from rubik.Utils import get_random_scramble, get_random_cubie, SUPER_FLIP
from rubik.Corner import Corner
from rubik.Symmetries import BASIC_SYM_CUBE, S_URF3, S_F2, S_U4, S_LR2, SYM_CUBIES, SYM_N, INV_IDX, get_symmetries
import random
import math

if __name__ == '__main__':

    c = CubieCube()
    # UR, UF, UL, UB, DR, DF, DL, DB, FR, FL, BL, BR
    c.scramble("R F L B'")
    print(c)
    # self.assertEqual(c.get_ud_slice_coord(), 0)




