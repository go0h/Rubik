import rubik.FaceletCube as fc
import rubik.CubieCube as cc
import rubik.CoordCubie as coord
import rubik.Utils as u
from rubik.Utils import get_random_scramble, get_random_cubie, get_random_cubie_2
from rubik.Symmetries import BASIC_SYM_CUBE, S_URF3, S_F2, S_U4, S_LR2, SYM_CUBIES, SYM_N, INV_IDX
import solver.TwoPhaseSolver as ss
import solver.TwoPhaseSolverSlow as sss
from rubik.Tables import distance, twist_conj

# SF 37s
# HARD - "B' U2 R' U2 U F2 R D F2 " 1:43, 0:19
if __name__ == '__main__':

    scramble = "B' U2 R' U2 U F2 R D F2 " #get_random_scramble() #u.SUPER_FLIP #
    print(f"SCRAMBLE = \"{scramble}\"")
    cubie = cc.CubieCube()

    cubie.scramble(scramble)

    f1 = cubie.to_facelet_cube()
    print(f1)

    solver = sss.TwoPhaseSolverSlow(cubie)
    # solver = ss.TwoPhaseSolver(cubie)

    moves = solver.solve()
    scramble = ' '.join([i for i in moves])
    print(scramble)
    print(len(moves))
    f1.scramble(scramble)
    print(f1)
