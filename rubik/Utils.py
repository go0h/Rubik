import random
import rubik.FaceletCube as fc
import rubik.CubieCube as cc
from copy import deepcopy


__all__ = ['SUPER_FLIP', 'PONS_ASINORUM', 'PONS_ASINORUM_SUPER_FLIP', 'MOVES', 'MOVES_S', 'PHASE2_MOVES',
           'PHASE2_MOVES_S', 'get_random_cubie', 'get_random_cubie_2', 'get_random_facelet', 'get_random_facelet_2',
           'get_random_scramble', 'get_random_scramble_2', 'moves_to_scramble', 'check_cubie_in_phase2',
           'rotate_left', 'rotate_right']


SUPER_FLIP = "D' R2 F' D2 F2 U2 L' R D' R2 B F R' U2 L' F2 R' U2 R' U'"
PONS_ASINORUM = "B2 F2 L2 R2 D2 U2"
PONS_ASINORUM_SUPER_FLIP = "R B L F D L R' B2 F D' U L D' U R' D' F' R' U'"

MOVES = [_ for _ in range(18)]

MOVES_S = ["U", "U2", "U'",
           "R", "R2", "R'",
           "F", "F2", "F'",
           "D", "D2", "D'",
           "L", "L2", "L'",
           "B", "B2", "B'"]

PHASE2_MOVES = [0, 1, 2, 4, 7, 9, 10, 11, 13, 16]

PHASE2_MOVES_S = ["U", "U2", "U'", "R2", "F2", "D", "D2", "D'", "L2", "B2"]


def get_random_scramble():
    random_scramble = ""
    for i in range(random.randint(1, 30)):
        random_scramble += random.choice(MOVES_S) + " "
    return random_scramble


def get_random_scramble_2():
    random_scramble = ""
    for i in range(random.randint(1, 30)):
        random_scramble += random.choice(PHASE2_MOVES_S) + " "
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


def moves_to_scramble(moves):
    str_moves = list(map(lambda x: MOVES_S[x], moves))
    scramble = ' '.join(i for i in str_moves)
    return scramble.strip()


def check_cubie_in_phase2(cubie, moves):
    c = deepcopy(cubie)
    c.scramble(moves_to_scramble(moves))
    # print(c.get_edges_flip())
    # print(c.get_corners_twist())
    # print(c.get_ud_slice_coord())
    return c.get_edges_flip() == 0 and c.get_corners_twist() == 0 and c.get_ud_slice_coord() == 0


def rotate_left(arr, l, r):
    """"Rotate array arr left between l and r. r is included."""
    temp = arr[l]
    for i in range(l, r):
        arr[i] = arr[i + 1]
    arr[r] = temp


def rotate_right(arr, l, r):
    """"Rotate array arr right between l and r. r is included."""
    temp = arr[r]
    for i in range(r, l, -1):
        arr[i] = arr[i-1]
    arr[l] = temp
