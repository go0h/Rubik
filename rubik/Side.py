from rubik.Colors import *


class Side:
    """Сторона кубика"""

    def __init__(self, size, color, side=None):
        self.size = size
        self.color = color
        if side is None:
            self.side = [[color for _ in range(self.size)] for _ in range(self.size)]
        else:
            self.side = side

    def rotate_90(self) -> None:
        """Вращение стороны по часовой стрелке на 90 градусов"""
        for i in range(self.size // 2):
            for j in range(i, self.size - i - 1):
                # top left <-> top right
                self.side[i][j], self.side[j][self.size - 1 - i] = self.side[j][self.size - 1 - i], self.side[i][j]
                # top left <-> bottom right
                self.side[i][j], self.side[self.size - 1 - i][self.size - 1 - j] = self.side[self.size - 1 - i][self.size - 1 - j], self.side[i][j]
                # top left <-> bottom left
                self.side[i][j], self.side[self.size - 1 - j][i] = self.side[self.size - 1 - j][i], self.side[i][j]

    def rotate_180(self) -> None:
        """Вращение стороны по часовой стрелке на 180 градусов"""
        for i in range(self.size // 2 + (self.size % 2)):
            for j in range(i, self.size):
                # top left <-> bottom right
                self.side[i][j], self.side[self.size - 1 - i][self.size - 1 - j] = self.side[self.size - 1 - i][self.size - 1 - j], self.side[i][j]

    def rotate_270(self) -> None:
        """Вращение стороны по часовой стрелке на 270 градусов"""
        for i in range(self.size // 2):
            for j in range(i, self.size - i - 1):
                # top left <-> bottom left
                self.side[i][j], self.side[self.size - 1 - j][i] = self.side[self.size - 1 - j][i], self.side[i][j]
                # top left <-> bottom right
                self.side[i][j], self.side[self.size - 1 - i][self.size - 1 - j] = self.side[self.size - 1 - i][self.size - 1 - j], self.side[i][j]
                # top left <-> top right
                self.side[i][j], self.side[j][self.size - 1 - i] = self.side[j][self.size - 1 - i], self.side[i][j]

    def get_row(self, num, reverse=False):
        row = self.side[num].copy()
        if reverse:
            row.reverse()
        return row

    def get_col(self, num, reverse=False):
        col = [self.side[i][num] for i in range(self.size)]
        if reverse:
            col.reverse()
        return col

    def set_row(self, num, row, reverse=False):
        old_row = self.get_row(num, reverse)
        for i in range(self.size):
            self.side[num][i] = row[i]
        return old_row

    def set_col(self, num, col, reverse=False):
        old_col = self.get_col(num, reverse)
        for i in range(self.size):
            self.side[i][num] = col[i]
        return old_col

    def __str__(self):
        res = ""
        for line in self.side:
            res += ''.join(colors[i] for i in line) + colors[DROP] + colors[DROP] + "\n"
        return res

    def __eq__(self, other):
        if self.side != other.side:
            return False
        for i in range(self.size):
            if self.side[i] != self.side[i]:
                return False
        return True

    def __copy__(self):
        copy = Side(self.size, self.color)
        for i in range(self.size):
            for j in range(self.size):
                copy.side[i][j] = self.side[i][j]
        return copy
