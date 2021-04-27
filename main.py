from rubik.FaceletCube import FaceletCube
from rubik.CubieCube import CubieCube
from rubik.Colors import *


if __name__ == '__main__':

    r = FaceletCube()

    res = r.__copy__()
    print(r)
    r.scramble("U' R U F R' B' F2 L2 B F L2 B' U L R' U B' U2 L D2 R' B F2 U B2 F2 U B' L' B2")
    print(r)
    cubie = CubieCube()
    print(cubie)
