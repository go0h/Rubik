import unittest

from rubik.FaceletCube import FaceletCube
from rubik.Colors import *
from rubik.Side import Side


class RotationTest(unittest.TestCase):

    def test_rotation_90_side(self):
        side1 = [[1, 2, 3],
                 [4, 5, 6],
                 [7, 8, 9]]
        side2 = [[7, 4, 1],
                 [8, 5, 2],
                 [9, 6, 3]]

        s1 = Side(3, RIGHT, side1)
        s2 = Side(3, RIGHT, side2)
        s1.rotate_90()

        self.assertEqual(s1, s2)

    def test_rotation_180_side(self):
        side1 = [[1, 2, 3],
                 [4, 5, 6],
                 [7, 8, 9]]
        side2 = [[9, 8, 7],
                 [6, 5, 4],
                 [3, 2, 1]]

        s1 = Side(3, RIGHT, side1)
        s2 = Side(3, RIGHT, side2)
        s1.rotate_180()

        self.assertEqual(s1, s2)

    def test_rotation_270_side(self):
        side1 = [[1, 2, 3],
                 [4, 5, 6],
                 [7, 8, 9]]
        side2 = [[3, 6, 9],
                 [2, 5, 8],
                 [1, 4, 7]]

        s1 = Side(3, RIGHT, side1)
        s2 = Side(3, RIGHT, side2)
        s1.rotate_270()

        self.assertEqual(s1, s2)

    def test_front_rotation(self):
        r = FaceletCube()

        r.left.side[0][2] = LEFT
        r.left.side[1][2] = FRONT
        r.left.side[2][2] = RIGHT
        r.right.side[0][0] = LEFT
        r.right.side[1][0] = FRONT
        r.right.side[2][0] = RIGHT

        res = r.__copy__()
        for _ in range(4):
            r.str_move("F")

        self.assertEqual(r, res)

    def test_front_reverse_rotation(self):
        r = FaceletCube()

        r.left.side[0][2] = LEFT
        r.left.side[1][2] = FRONT
        r.left.side[2][2] = RIGHT
        r.right.side[0][0] = LEFT
        r.right.side[1][0] = FRONT
        r.right.side[2][0] = RIGHT

        res = r.__copy__()
        for _ in range(4):
            r.str_move("F'")

        self.assertEqual(r, res)

    def test_front_180_rotation(self):

        r = FaceletCube()

        r.up.side[2][0] = LEFT
        r.up.side[2][1] = FRONT
        r.up.side[2][2] = RIGHT

        r.left.side[0][2] = LEFT
        r.left.side[1][2] = FRONT
        r.left.side[2][2] = RIGHT

        r.right.side[0][0] = LEFT
        r.right.side[1][0] = FRONT
        r.right.side[2][0] = RIGHT

        res = r.__copy__()
        for _ in range(2):
            r.str_move("F2")

        self.assertEqual(r, res)

    def test_common_front_rotation(self):
        r = FaceletCube()

        r.up.side[0][2] = RIGHT
        r.left.side[2][0] = FRONT
        r.right.side[2][2] = RIGHT
        r.down.side[2][2] = FRONT

        r2 = r.__copy__()
        r.str_move("F")
        r.str_move("F'")
        self.assertEqual(r, r2)
        r.str_move("F")
        r.str_move("F")
        r2.str_move("F2")
        self.assertEqual(r, r2)

    def test_back_rotation(self):
        r = FaceletCube()

        r.up.side[0][2] = RIGHT
        r.left.side[2][0] = FRONT
        r.right.side[2][2] = RIGHT
        r.down.side[2][2] = FRONT

        res = r.__copy__()
        r.str_move("B")
        self.assertEqual(r.left.side[0][0], RIGHT)
        self.assertEqual(r.up.side[0][2], RIGHT)
        self.assertEqual(r.right.side[0][2], FRONT)
        self.assertEqual(r.down.side[2][2], FRONT)

        for _ in range(3):
            r.str_move("B")

        self.assertEqual(r, res)

    def test_back_reverse_rotation(self):
        r = FaceletCube()

        r.up.side[0][2] = RIGHT
        r.left.side[2][0] = FRONT
        r.right.side[2][2] = RIGHT
        r.down.side[2][2] = FRONT

        res = r.__copy__()
        r.str_move("B'")
        self.assertEqual(r.left.side[2][0], FRONT)
        self.assertEqual(r.up.side[0][0], FRONT)
        self.assertEqual(r.right.side[2][2], RIGHT)
        self.assertEqual(r.down.side[2][0], RIGHT)

        for _ in range(3):
            r.str_move("B'")

        self.assertEqual(r, res)

    def test_back_180_rotation(self):
        r = FaceletCube()

        r.up.side[0][2] = RIGHT
        r.left.side[2][0] = FRONT
        r.right.side[2][2] = LEFT
        r.down.side[2][2] = FRONT

        res = r.__copy__()
        r.str_move("B2")
        self.assertEqual(r.left.side[0][0], LEFT)
        self.assertEqual(r.up.side[0][0], FRONT)
        self.assertEqual(r.right.side[0][2], FRONT)
        self.assertEqual(r.down.side[2][0], RIGHT)

        r.str_move("B2")

        self.assertEqual(r, res)

    def test_up_rotation(self):
        r = FaceletCube()

        r.left.side[0][0] = LEFT
        r.front.side[0][2] = BACK
        r.right.side[0][2] = RIGHT
        r.back.side[0][2] = FRONT

        res = r.__copy__()
        r.str_move("U")
        self.assertEqual(r.left.side[0][2], BACK)
        self.assertEqual(r.front.side[0][2], RIGHT)
        self.assertEqual(r.right.side[0][2], FRONT)
        self.assertEqual(r.back.side[0][0], LEFT)

        for i in range(3):
            r.str_move("U")

        self.assertEqual(r, res)

    def test_up_reverse_rotation(self):
        r = FaceletCube()

        r.left.side[0][0] = LEFT
        r.front.side[0][2] = BACK
        r.right.side[0][2] = RIGHT
        r.back.side[0][2] = FRONT

        res = r.__copy__()
        r.str_move("U'")
        self.assertEqual(r.left.side[0][2], FRONT)
        self.assertEqual(r.front.side[0][0], LEFT)
        self.assertEqual(r.right.side[0][2], BACK)
        self.assertEqual(r.back.side[0][2], RIGHT)

        for i in range(3):
            r.str_move("U'")

        self.assertEqual(r, res)

    def test_up_180_rotation(self):
        r = FaceletCube()

        r.left.side[0][2] = LEFT
        r.front.side[0][2] = BACK
        r.right.side[0][2] = RIGHT
        r.back.side[0][2] = FRONT

        res = r.__copy__()
        r.str_move("U2")
        self.assertEqual(r.left.side[0][2], RIGHT)
        self.assertEqual(r.front.side[0][2], FRONT)
        self.assertEqual(r.right.side[0][2], LEFT)
        self.assertEqual(r.back.side[0][2], BACK)

        r.str_move("U2")

        self.assertEqual(r, res)

    def test_down_rotation(self):
        r = FaceletCube()

        r.left.side[2][2] = LEFT
        r.front.side[2][2] = BACK
        r.right.side[2][2] = RIGHT
        r.back.side[2][2] = FRONT

        res = r.__copy__()
        r.str_move("D")
        self.assertEqual(r.left.side[2][2], FRONT)
        self.assertEqual(r.front.side[2][2], LEFT)
        self.assertEqual(r.right.side[2][2], BACK)
        self.assertEqual(r.back.side[2][2], RIGHT)

        for i in range(3):
            r.str_move("D")

        self.assertEqual(r, res)

    def test_down_reverse_rotation(self):
        r = FaceletCube()

        r.left.side[2][2] = LEFT
        r.front.side[2][2] = BACK
        r.right.side[2][2] = RIGHT
        r.back.side[2][2] = FRONT

        res = r.__copy__()
        r.str_move("D'")
        self.assertEqual(r.left.side[2][2], BACK)
        self.assertEqual(r.front.side[2][2], RIGHT)
        self.assertEqual(r.right.side[2][2], FRONT)
        self.assertEqual(r.back.side[2][2], LEFT)

        for i in range(3):
            r.str_move("D'")

        self.assertEqual(r, res)

    def test_down_180_rotation(self):
        r = FaceletCube()

        r.left.side[2][2] = LEFT
        r.front.side[2][2] = BACK
        r.right.side[2][2] = RIGHT
        r.back.side[2][2] = FRONT

        res = r.__copy__()
        r.str_move("D2")
        self.assertEqual(r.left.side[2][2], RIGHT)
        self.assertEqual(r.front.side[2][2], FRONT)
        self.assertEqual(r.right.side[2][2], LEFT)
        self.assertEqual(r.back.side[2][2], BACK)

        r.str_move("D2")

        self.assertEqual(r, res)

    def test_right_rotation(self):
        r = FaceletCube()

        r.up.side[2][2] = LEFT
        r.front.side[2][2] = BACK
        r.down.side[2][2] = RIGHT
        r.back.side[2][0] = FRONT

        res = r.__copy__()
        r.str_move("R")
        self.assertEqual(r.up.side[2][2], BACK)
        self.assertEqual(r.front.side[2][2], RIGHT)
        self.assertEqual(r.down.side[0][2], FRONT)
        self.assertEqual(r.back.side[0][0], LEFT)

        for i in range(3):
            r.str_move("R")

        self.assertEqual(r, res)

    def test_right_reverse_rotation(self):
        r = FaceletCube()

        r.up.side[2][2] = LEFT
        r.front.side[2][2] = BACK
        r.down.side[2][2] = RIGHT
        r.back.side[2][0] = FRONT

        res = r.__copy__()
        r.str_move("R'")
        self.assertEqual(r.up.side[0][2], FRONT)
        self.assertEqual(r.front.side[2][2], LEFT)
        self.assertEqual(r.down.side[2][2], BACK)
        self.assertEqual(r.back.side[0][0], RIGHT)

        for i in range(3):
            r.str_move("R'")

        self.assertEqual(r, res)

    def test_right_180_rotation(self):
        r = FaceletCube()

        r.up.side[2][2] = LEFT
        r.front.side[2][2] = BACK
        r.down.side[2][2] = RIGHT
        r.back.side[2][0] = FRONT

        res = r.__copy__()
        r.str_move("R2")
        self.assertEqual(r.up.side[2][2], RIGHT)
        self.assertEqual(r.front.side[0][2], FRONT)
        self.assertEqual(r.down.side[2][2], LEFT)
        self.assertEqual(r.back.side[0][0], BACK)

        r.str_move("R2")

        self.assertEqual(r, res)

    def test_left_rotation(self):
        r = FaceletCube()

        r.up.side[2][0] = LEFT
        r.front.side[2][0] = BACK

        r.down.side[2][0] = RIGHT
        r.back.side[2][2] = FRONT

        res = r.__copy__()
        r.str_move("L")
        self.assertEqual(r.up.side[0][0], FRONT)
        self.assertEqual(r.front.side[2][0], LEFT)
        self.assertEqual(r.down.side[2][0], BACK)
        self.assertEqual(r.back.side[0][2], RIGHT)

        for i in range(3):
            r.str_move("L")

        self.assertEqual(r, res)

    def test_left_reverse_rotation(self):
        r = FaceletCube()

        r.up.side[2][0] = LEFT
        r.front.side[2][0] = BACK
        r.down.side[2][0] = RIGHT
        r.back.side[2][2] = FRONT

        res = r.__copy__()
        r.str_move("L'")
        self.assertEqual(r.up.side[2][0], BACK)
        self.assertEqual(r.front.side[2][0], RIGHT)
        self.assertEqual(r.down.side[0][0], FRONT)
        self.assertEqual(r.back.side[0][2], LEFT)

        for i in range(3):
            r.str_move("L'")

        self.assertEqual(r, res)

    def test_left_180_rotation(self):
        r = FaceletCube()

        r.up.side[2][0] = LEFT
        r.front.side[2][0] = BACK

        r.down.side[2][0] = RIGHT
        r.back.side[2][2] = FRONT

        res = r.__copy__()
        r.str_move("L2")
        self.assertEqual(r.up.side[2][0], RIGHT)
        self.assertEqual(r.front.side[0][0], FRONT)
        self.assertEqual(r.down.side[2][0], LEFT)
        self.assertEqual(r.back.side[0][2], BACK)

        r.str_move("L2")

        self.assertEqual(r, res)

    def test_right_algo(self):
        r = FaceletCube()

        res = r.__copy__()
        for _ in range(6):
            r.str_move("R")
            r.str_move("U")
            r.str_move("R'")
            r.str_move("U'")

        self.assertEqual(res, r)

    def test_left_algo(self):
        r = FaceletCube()

        res = r.__copy__()
        for _ in range(6):
            r.str_move("L'")
            r.str_move("U'")
            r.str_move("L")
            r.str_move("U")

        self.assertEqual(res, r)


if __name__ == '__main__':
    unittest.main()
