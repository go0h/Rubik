import rubik.CubieCube as cc
from rubik.Utils import get_random_scramble, SUPER_FLIP
import solver.TwoPhaseSolver as tfs
from rubik.Tables import fs_classidx

# HARD - "B' U2 R' U2 U F2 R D F2 " 1:43, 0:19, 0:14, 0:12

if __name__ == '__main__':

    scramble = "B' U2 R' U2 U F2 R D F2 "
    # scramble = get_random_scramble()
    # scramble = SUPER_FLIP
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

