import rubik.FaceletCube as fc
import rubik.CubieCube as cc
from rubik.Utils import get_random_scramble, get_random_cubie, SUPER_FLIP
from rubik.Symmetries import BASIC_SYM_CUBE, S_URF3, S_F2, S_U4, S_LR2, SYM_CUBIES, SYM_N, INV_IDX, get_symmetries
import solver.TwoPhaseSolver as ss
from rubik.Tables import fs_classidx

if __name__ == '__main__':

    # print(fc.FaceletCube())

    print(len(set(fs_classidx)))