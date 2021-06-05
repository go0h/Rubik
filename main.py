import rubik.CubieCube as cc
from rubik.Utils import get_random_scramble, SUPER_FLIP
import solver.TwoPhaseSolver as tfs
import solver.TwoPhaseSolverSlow as tfss
import rubik.Tables as t

if __name__ == '__main__':

    # scramble = "R B' L2 L' U R2 R' U U L F B' D F2 U D' U2 D' B2 F2 B2 L2 L' L' R U R D' L U'"
    # scramble = "B R' B B2 U2 R' D2 F R' U' "
    # scramble = get_random_scramble()
    scramble = SUPER_FLIP
    print(f"SCRAMBLE = \"{scramble}\"")
    cubie = cc.CubieCube()

    cubie.scramble(scramble)

    f1 = cubie.to_facelet_cube()
    print(f1)

    solver = tfs.TwoPhaseSolver(cubie)

    moves = solver.solve()
    scramble = ' '.join([i for i in moves])
    print(scramble)
    print(len(moves))
    f1.scramble(scramble)
    print(f1)
