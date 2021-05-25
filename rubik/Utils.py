import copy
import random

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

INV_MOVE = [2, 1, 0, 5, 4, 3, 8, 7, 6, 11, 10, 9, 14, 13, 12, 17, 16, 15]

PHASE2_MOVES = [0, 1, 2, 4, 7, 9, 10, 11, 13, 16]

PHASE2_MOVES_S = ["U", "U2", "U'", "R2", "F2", "D", "D2", "D'", "L2", "B2"]


def get_random_moves():
    moves = []
    for i in range(random.randint(1, 30)):
        moves.append(random.choice(MOVES))
    return moves


def get_random_moves_2():
    moves = []
    for i in range(random.randint(1, 30)):
        moves.append(random.choice(PHASE2_MOVES))
    return moves


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


def moves_to_scramble(moves):
    str_moves = list(map(lambda x: MOVES_S[x], moves))
    scramble = ' '.join(i for i in str_moves)
    return scramble.strip()


def rotate_left(arr, left, right):
    """"Вращение массива влево между [left, right]"""
    temp = arr[left]
    for i in range(left, right):
        arr[i] = arr[i + 1]
    arr[right] = temp


def rotate_right(arr, left, right):
    """"Вращение массива вправо межу [left, right]"""
    temp = arr[right]
    for i in range(right, left, -1):
        arr[i] = arr[i - 1]
    arr[left] = temp


def check_cubie_in_phase2(cubie, moves):
    c = copy.deepcopy(cubie)
    c.apply_moves(moves)
    return c.get_edges_flip() == 0 and c.get_corners_twist() == 0 and c.get_ud_slice_coord() == 0