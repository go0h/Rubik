from rubik.Rubik import Rubik
from rubik.Colors import *


if __name__ == '__main__':

    r = Rubik()
    print(r)
    print("FRONT")
    r.rotate(RED)
    print(r)

    r = Rubik()
    print("LEFT")
    r.rotate(GREEN)
    print(r)
