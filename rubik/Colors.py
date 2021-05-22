
NONE, UP, RIGHT, FRONT, DOWN, LEFT, BACK = range(-1, 6)
U, R, F, D, L, B = range(6)

SIDE = {R: "R", L: "L", B: "B", F: "F", U: "U", D: "D"}

RED = '\033[41m  '
ORANGE = '\033[43m  '
GREEN = '\033[42m  '
BLUE = '\33[44m  '
YELLOW = '\033[103m  '
WHITE = '\033[107m  '
DROP = '\033[0m'


colors = {
    NONE: DROP,
    RIGHT: RED,
    LEFT: ORANGE,
    BACK: GREEN,
    FRONT: BLUE,
    UP: YELLOW,
    DOWN: WHITE,
}


# Противоположная сторона
opposite = {
    DOWN: UP,
    UP: DOWN,
    FRONT: BACK,
    BACK: FRONT,
    RIGHT: LEFT,
    LEFT: RIGHT
}

# Левая сторона относительно текущей, если Белая сторона это верх
# Правая вычисляется opposite[left[side]]
left = {
    DOWN: BACK,
    UP: BACK,
    BACK: LEFT,
    RIGHT: BACK,
    FRONT: RIGHT,
    LEFT: FRONT
}

# Верхняя сторона относительно текущей, если Белая сторона это верх
# Нижняя вычисляется opposite[up[side]]
up = {
    BACK: DOWN,
    RIGHT: DOWN,
    FRONT: DOWN,
    LEFT: DOWN,
    DOWN: LEFT,
    UP: RIGHT
}
