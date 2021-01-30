
# Вращение стороны кубика рубика по часовой стрелке
def rotate_side(side=list):
    size = len(side)

    for i in range(int(size / 2)):
        for j in range(i, size - i - 1):
            # top left <-> top right
            side[i][j], side[j][size - 1 - i] = side[j][size - 1 - i], side[i][j]
            # top left <-> bottom right
            side[i][j], side[size - 1 - i][size - 1 - j] = side[size - 1 - i][size - 1 - j], side[i][j]
            # top left <-> bottom left
            side[i][j], side[size - 1 - j][i] = side[size - 1 - j][i], side[i][j]
    return side
