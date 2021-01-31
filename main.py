from rubik.Rubik import Rubik
from rubik.Colors import *


if __name__ == '__main__':

    r = Rubik()

    res = r.__copy__()
    print(r)
    r.exec_scramble("B2 F' L2 R D2 U F' R' F2 D' U L2 B2 D2 U' L' D U2 F' D' L2 B' D2 B D F2 U' R D U'")
    print(r)
