import random
from rubik.FaceletCube import FaceletCube
from rubik.CubieCube import CubieCube

MOVES = ["F", "B", "U", "D", "R", "L",
         "F'", "B'", "U'", "D'", "R'", "L'",
         "F2", "B2", "U2", "D2", "R2", "L2"]


def get_random_scramble():
    random_scramble = ""
    for i in range(random.randint(1, 30)):
        random_scramble += random.choice(MOVES) + " "
    return random_scramble


def get_random_facelet():
    facelet = FaceletCube()
    facelet.scramble(get_random_scramble())
    return facelet


def get_random_cubie():
    cubie = CubieCube()
    cubie.scramble(get_random_scramble())
    return cubie
