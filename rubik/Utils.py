import random
from rubik.FaceletCube import FaceletCube
from rubik.CubieCube import CubieCube
import math

SUPER_FLIP = "D' R2 F' D2 F2 U2 L' R D' R2 B F R' U2 L' F2 R' U2 R' U'"
PONS_ASINORUM = "B2 F2 L2 R2 D2 U2"
PONS_ASINORUM_SUPER_FLIP = "R B L F D L R' B2 F D' U L D' U R' D' F' R' U'"

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


def binomial(n, k):
    if n < k:
        return 0
    res = math.factorial(n) // (math.factorial(k) * math.factorial(n - k))
    return res
