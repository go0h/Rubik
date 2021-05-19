import rubik.FaceletCube as fc
import rubik.CubieCube as cc
import rubik.CoordCubie as coord
import rubik.Utils as u
from rubik.Utils import get_random_scramble, get_random_cubie, get_random_cubie_2
from rubik.Symmetries import BASIC_SYM_CUBE, S_URF3, S_F2, S_U4, S_LR2, SYM_CUBIES, SYM_N, INV_IDX, get_symmetries
import solver.TwoPhaseSolver as ss
from rubik.Tables import distance

if __name__ == '__main__':

    scramble = get_random_scramble()
    print(f"SCRAMBLE = \"{scramble}\"")
    cubie = cc.CubieCube()

    cubie.scramble(scramble)

    f1 = cubie.to_facelet_cube()
    print(f1)

    solver = ss.TwoPhaseSolver(cubie)

    moves = solver.solve()
    scramble = ' '.join([i for i in moves])
    print(scramble)
    print(len(moves))
    f1.scramble(scramble)
    print(f1)
