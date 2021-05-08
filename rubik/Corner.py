
from collections import deque
from rubik.Colors import B, L, U, R, D, F

# Угловые координаты
# Пример: URF - UP, RIGHT, FRONT (верхний правый передний угол)
URF, UFL, ULB, UBR, DFR, DLF, DBL, DRB = range(8)

CORNERS = {URF: "URF", UFL: "UFL", ULB: "ULB", UBR: "UBR",
           DFR: "DFR", DLF: "DLF", DBL: "DBL", DRB: "DRB"}

# лицевые стороны угла
CORNERS_SIDES = {
    URF: [U, R, F], UFL: [U, F, L], ULB: [U, L, B], UBR: [U, B, R],
    DFR: [D, F, R], DLF: [D, L, F], DBL: [D, B, L], DRB: [D, R, B]
}

# координаты угла на гранях
CORNER_FACES_COORDS = {
    URF: [[2, 2], [0, 0], [0, 2]],
    UFL: [[2, 0], [0, 0], [0, 2]],
    ULB: [[0, 0], [0, 0], [0, 2]],
    UBR: [[0, 2], [0, 0], [0, 2]],
    DFR: [[0, 2], [2, 2], [2, 0]],
    DLF: [[0, 0], [2, 2], [2, 0]],
    DBL: [[2, 0], [2, 2], [2, 0]],
    DRB: [[2, 2], [2, 2], [2, 0]]
}

# получение координаты угла по двум сторонам
CORNER_BY_SIDES = {
    U: {R: URF, F: UFL, L: ULB, B: UBR},
    D: {F: DFR, L: DLF, B: DBL, R: DRB}
}


class Corner:

    def __init__(self, coord, orient=0):
        # c - координата
        self.c = coord
        # o - ориентация
        self.o = orient

    def rotate(self, coord, num) -> None:
        self.c = coord
        self.o += num
        if self.o > 2:
            self.o -= 3

    def get_coordinates(self, position) -> list:
        c1, c2, c3 = [CORNERS_SIDES[self.c][abs((i - self.o) % 3)] for i in range(3)]
        return [CORNER_FACES_COORDS[position][0] + [c1],
                CORNER_FACES_COORDS[position][1] + [c2],
                CORNER_FACES_COORDS[position][2] + [c3]]

    def set_coordinate(self, position, sides) -> None:
        # получаем лицевые стороны угла, в зависимости от позиции
        f1, f2, f3 = CORNERS_SIDES[position]
        # получаем сслыки на объект Side
        s1, s2, s3 = sides[f1], sides[f2], sides[f3]

        # получаем координаты где располагаются углы
        c1, c2, c3 = CORNER_FACES_COORDS[position]

        # получаем текущие стороны которые располжены в углу
        corner_sides = deque([s1.side[c1[0]][c1[1]], s2.side[c2[0]][c2[1]], s3.side[c3[0]][c3[1]]])

        # вычисляем ориентацию угла
        while corner_sides[0] != U and corner_sides[0] != D:
            corner_sides.rotate(1)
            self.o += 1

        if self.o == 2:
            self.o = 1
        elif self.o == 1:
            self.o = 2

        # получаем реальную координату угла
        self.c = CORNER_BY_SIDES[corner_sides[0]][corner_sides[1]]

    def __str__(self) -> str:
        return CORNERS[self.c] + "," + str(self.o)

    def __eq__(self, other) -> bool:
        return self.o == other.o and self.c == other.c
