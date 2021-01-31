
DROP, RED, ORANGE, GREEN, BLUE, YELLOW, WHITE = range(-1, 6)

__RED__ = '\033[41m  '
__ORANGE__ = '\033[43m  '
__GREEN__ = '\033[42m  '
__BLUE__ = '\33[44m  '
__YELLOW__ = '\033[103m  '
__WHITE__ = '\033[107m  '
__DROP__ = '\033[0m'


colors = {
    DROP: __DROP__,
    RED: __RED__,
    ORANGE: __ORANGE__,
    GREEN: __GREEN__,
    BLUE: __BLUE__,
    YELLOW: __YELLOW__,
    WHITE: __WHITE__,
}


# Противоположная сторона
opposite = {
    WHITE: YELLOW,
    YELLOW: WHITE,
    BLUE: GREEN,
    GREEN: BLUE,
    RED: ORANGE,
    ORANGE: RED
}

# Левая сторона относительно текущей, если Белая сторона это верх
# Правая вычисляется opposite[left[side]]
left = {
    WHITE: GREEN,
    YELLOW: GREEN,
    GREEN: ORANGE,
    RED: GREEN,
    BLUE: RED,
    ORANGE: BLUE
}

# Верхняя сторона относительно текущей, если Белая сторона это верх
# Нижняя вычисляется opposite[up[side]]
up = {
    GREEN: WHITE,
    RED: WHITE,
    BLUE: WHITE,
    ORANGE: WHITE,
    WHITE: ORANGE,
    YELLOW: RED
}
