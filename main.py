from rubik.FaceletCube import FaceletCube
from rubik.CubieCube import CubieCube
from rubik.Utils import get_random_scramble


if __name__ == '__main__':

    scramble = get_random_scramble()

    f1 = FaceletCube()
    f1.scramble(scramble)

    c1 = CubieCube()
    c1.scramble(scramble)

    f2 = c1.to_facelet_cube()
    c2 = f1.to_cubie_cube()
    print(f1 == f2)
    print(c1 == c2)

