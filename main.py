from rubik.Rubik import Rubik
from rubik.Colors import *


if __name__ == '__main__':

    r = Rubik()

    r.white.side[2][0] = ORANGE
    r.red.side[2][0] = GREEN
    r.yellow.side[2][0] = RED
    r.orange.side[2][2] = BLUE

    print(r)

    r.move("2L")
    print(r)
