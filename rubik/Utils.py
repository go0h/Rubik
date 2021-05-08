
import random
import rubik.FaceletCube as fc
import rubik.CubieCube as cc

SUPER_FLIP = "D' R2 F' D2 F2 U2 L' R D' R2 B F R' U2 L' F2 R' U2 R' U'"
PONS_ASINORUM = "B2 F2 L2 R2 D2 U2"
PONS_ASINORUM_SUPER_FLIP = "R B L F D L R' B2 F D' U L D' U R' D' F' R' U'"

MOVES = ["F", "B", "U", "D", "R", "L",
         "F'", "B'", "U'", "D'", "R'", "L'",
         "F2", "B2", "U2", "D2", "R2", "L2"]

PHASE2_MOVES = ["U", "D", "F2", "B2", "U2", "D2", "R2", "L2"]


def get_random_scramble():
    random_scramble = ""
    for i in range(random.randint(1, 30)):
        random_scramble += random.choice(MOVES) + " "
    return random_scramble


def get_random_scramble_2():
    random_scramble = ""
    for i in range(random.randint(1, 30)):
        random_scramble += random.choice(PHASE2_MOVES) + " "
    return random_scramble


def get_random_facelet():
    facelet = fc.FaceletCube()
    facelet.scramble(get_random_scramble())
    return facelet


def get_random_facelet_2():
    facelet = fc.FaceletCube()
    facelet.scramble(get_random_scramble_2())
    return facelet


def get_random_cubie():
    cubie = cc.CubieCube()
    cubie.scramble(get_random_scramble())
    return cubie


def get_random_cubie_2():
    cubie = cc.CubieCube()
    cubie.scramble(get_random_scramble_2())
    return cubie
