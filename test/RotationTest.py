import unittest

from rubik.Rubik import Rubik
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

        s1 = Side(3, RED, side1)
        s2 = Side(3, RED, side2)
        s1.rotate_90()

        self.assertEqual(s1, s2)

    def test_rotation_180_side(self):
        side1 = [[1, 2, 3],
                 [4, 5, 6],
                 [7, 8, 9]]
        side2 = [[9, 8, 7],
                 [4, 5, 6],
                 [3, 2, 1]]

        s1 = Side(3, RED, side1)
        s2 = Side(3, RED, side2)
        s1.rotate_180()

        self.assertEqual(s1, s2)

    def test_rotation_270_side(self):
        side1 = [[1, 2, 3],
                 [4, 5, 6],
                 [7, 8, 9]]
        side2 = [[3, 6, 9],
                 [2, 5, 8],
                 [1, 4, 7]]

        s1 = Side(3, RED, side1)
        s2 = Side(3, RED, side2)
        s1.rotate_270()

        self.assertEqual(s1, s2)

    def test_front_rotation(self):
        r = Rubik()

        r.green.side[0][2] = ORANGE
        r.green.side[1][2] = BLUE
        r.green.side[2][2] = RED
        r.blue.side[0][0] = ORANGE
        r.blue.side[1][0] = BLUE
        r.blue.side[2][0] = RED

        res = r.__copy__()
        for _ in range(4):
            r.move("F")

        self.assertEqual(r, res)

    def test_front_reverse_rotation(self):
        r = Rubik()

        r.green.side[0][2] = ORANGE
        r.green.side[1][2] = BLUE
        r.green.side[2][2] = RED
        r.blue.side[0][0] = ORANGE
        r.blue.side[1][0] = BLUE
        r.blue.side[2][0] = RED

        res = r.__copy__()
        for _ in range(4):
            r.move("F'")

        self.assertEqual(r, res)

    def test_front_180_rotation(self):

        r = Rubik()

        r.white.side[2][0] = ORANGE
        r.white.side[2][1] = BLUE
        r.white.side[2][2] = RED

        r.green.side[0][2] = ORANGE
        r.green.side[1][2] = BLUE
        r.green.side[2][2] = RED

        r.blue.side[0][0] = ORANGE
        r.blue.side[1][0] = BLUE
        r.blue.side[2][0] = RED

        res = r.__copy__()
        for _ in range(2):
            r.move("2F")

        self.assertEqual(r, res)

    def test_common_front_rotation(self):
        r = Rubik()

        r.white.side[0][2] = RED
        r.green.side[2][0] = BLUE
        r.blue.side[2][2] = RED
        r.yellow.side[2][2] = BLUE

        r2 = r.__copy__()
        r.move("F")
        r.move("F'")
        self.assertEqual(r, r2)
        r.move("F")
        r.move("F")
        r2.move("2F")
        self.assertEqual(r, r2)

    def test_back_rotation(self):
        r = Rubik()

        r.white.side[0][2] = RED
        r.green.side[2][0] = BLUE
        r.blue.side[2][2] = RED
        r.yellow.side[2][2] = BLUE

        res = r.__copy__()
        r.move("B")
        self.assertEqual(r.green.side[0][0], RED)
        self.assertEqual(r.white.side[0][2], RED)
        self.assertEqual(r.blue.side[0][2], BLUE)
        self.assertEqual(r.yellow.side[2][2], BLUE)

        for _ in range(3):
            r.move("B")

        self.assertEqual(r, res)

    def test_back_reverse_rotation(self):
        r = Rubik()

        r.white.side[0][2] = RED
        r.green.side[2][0] = BLUE
        r.blue.side[2][2] = RED
        r.yellow.side[2][2] = BLUE

        res = r.__copy__()
        r.move("B'")
        self.assertEqual(r.green.side[2][0], BLUE)
        self.assertEqual(r.white.side[0][0], BLUE)
        self.assertEqual(r.blue.side[2][2], RED)
        self.assertEqual(r.yellow.side[2][0], RED)

        for _ in range(3):
            r.move("B'")

        self.assertEqual(r, res)

    def test_back_180_rotation(self):
        r = Rubik()

        r.white.side[0][2] = RED
        r.green.side[2][0] = BLUE
        r.blue.side[2][2] = RED
        r.yellow.side[2][2] = BLUE

        res = r.__copy__()
        r.move("2B")
        self.assertEqual(r.green.side[0][0], RED)
        self.assertEqual(r.white.side[0][0], BLUE)
        self.assertEqual(r.blue.side[2][0], BLUE)
        self.assertEqual(r.yellow.side[2][0], RED)

        r.move("2B")

        self.assertEqual(r, res)

    def test_up_rotation(self):
        r = Rubik()

        r.green.side[0][0] = ORANGE
        r.red.side[0][2] = GREEN
        r.blue.side[0][2] = RED
        r.orange.side[0][2] = BLUE

        res = r.__copy__()
        r.move("U")
        self.assertEqual(r.green.side[0][2], GREEN)
        self.assertEqual(r.red.side[0][2], RED)
        self.assertEqual(r.blue.side[0][2], BLUE)
        self.assertEqual(r.orange.side[0][0], ORANGE)

        for i in range(3):
            r.move("U")

        self.assertEqual(r, res)

    def test_up_reverse_rotation(self):
        r = Rubik()

        r.green.side[0][0] = ORANGE
        r.red.side[0][2] = GREEN
        r.blue.side[0][2] = RED
        r.orange.side[0][2] = BLUE

        res = r.__copy__()
        r.move("U'")
        self.assertEqual(r.green.side[0][2], BLUE)
        self.assertEqual(r.red.side[0][0], ORANGE)
        self.assertEqual(r.blue.side[0][2], GREEN)
        self.assertEqual(r.orange.side[0][2], RED)

        for i in range(3):
            r.move("U'")

        self.assertEqual(r, res)

    def test_up_180_rotation(self):
        r = Rubik()

        r.green.side[0][2] = ORANGE
        r.red.side[0][2] = GREEN
        r.blue.side[0][2] = RED
        r.orange.side[0][2] = BLUE

        res = r.__copy__()
        r.move("2U")
        self.assertEqual(r.green.side[0][2], RED)
        self.assertEqual(r.red.side[0][2], BLUE)
        self.assertEqual(r.blue.side[0][2], ORANGE)
        self.assertEqual(r.orange.side[0][2], GREEN)

        r.move("2U")

        self.assertEqual(r, res)

    def test_down_rotation(self):
        r = Rubik()

        r.green.side[2][2] = ORANGE
        r.red.side[2][2] = GREEN
        r.blue.side[2][2] = RED
        r.orange.side[2][2] = BLUE

        res = r.__copy__()
        r.move("D")
        self.assertEqual(r.green.side[2][2], BLUE)
        self.assertEqual(r.red.side[2][2], ORANGE)
        self.assertEqual(r.blue.side[2][2], GREEN)
        self.assertEqual(r.orange.side[2][2], RED)

        for i in range(3):
            r.move("D")

        self.assertEqual(r, res)

    def test_down_reverse_rotation(self):
        r = Rubik()

        r.green.side[2][2] = ORANGE
        r.red.side[2][2] = GREEN
        r.blue.side[2][2] = RED
        r.orange.side[2][2] = BLUE

        res = r.__copy__()
        r.move("D'")
        self.assertEqual(r.green.side[2][2], GREEN)
        self.assertEqual(r.red.side[2][2], RED)
        self.assertEqual(r.blue.side[2][2], BLUE)
        self.assertEqual(r.orange.side[2][2], ORANGE)

        for i in range(3):
            r.move("D'")

        self.assertEqual(r, res)

    def test_down_180_rotation(self):
        r = Rubik()

        r.green.side[2][2] = ORANGE
        r.red.side[2][2] = GREEN
        r.blue.side[2][2] = RED
        r.orange.side[2][2] = BLUE

        res = r.__copy__()
        r.move("2D")
        self.assertEqual(r.green.side[2][2], RED)
        self.assertEqual(r.red.side[2][2], BLUE)
        self.assertEqual(r.blue.side[2][2], ORANGE)
        self.assertEqual(r.orange.side[2][2], GREEN)

        r.move("2D")

        self.assertEqual(r, res)

    def test_right_rotation(self):
        r = Rubik()

        r.white.side[2][2] = ORANGE
        r.red.side[2][2] = GREEN
        r.yellow.side[2][2] = RED
        r.orange.side[2][0] = BLUE

        res = r.__copy__()
        r.move("R")
        self.assertEqual(r.white.side[2][2], GREEN)
        self.assertEqual(r.red.side[2][2], RED)
        self.assertEqual(r.yellow.side[0][2], BLUE)
        self.assertEqual(r.orange.side[0][0], ORANGE)

        for i in range(3):
            r.move("R")

        self.assertEqual(r, res)

    def test_right_reverse_rotation(self):
        r = Rubik()

        r.white.side[2][2] = ORANGE
        r.red.side[2][2] = GREEN
        r.yellow.side[2][2] = RED
        r.orange.side[2][0] = BLUE

        res = r.__copy__()
        r.move("R'")
        self.assertEqual(r.white.side[0][2], BLUE)
        self.assertEqual(r.red.side[2][2], ORANGE)
        self.assertEqual(r.yellow.side[2][2], GREEN)
        self.assertEqual(r.orange.side[0][0], RED)

        for i in range(3):
            r.move("R'")

        self.assertEqual(r, res)

    def test_right_180_rotation(self):
        r = Rubik()

        r.white.side[2][2] = ORANGE
        r.red.side[2][2] = GREEN
        r.yellow.side[2][2] = RED
        r.orange.side[2][0] = BLUE

        res = r.__copy__()
        r.move("2R")
        self.assertEqual(r.white.side[2][2], RED)
        self.assertEqual(r.red.side[0][2], BLUE)
        self.assertEqual(r.yellow.side[2][2], ORANGE)
        self.assertEqual(r.orange.side[0][0], GREEN)

        r.move("2R")

        self.assertEqual(r, res)

    def test_left_rotation(self):
        r = Rubik()

        r.white.side[2][0] = ORANGE
        r.red.side[2][0] = GREEN

        r.yellow.side[2][0] = RED
        r.orange.side[2][2] = BLUE

        res = r.__copy__()
        r.move("L")
        self.assertEqual(r.white.side[0][0], BLUE)
        self.assertEqual(r.red.side[2][0], ORANGE)
        self.assertEqual(r.yellow.side[2][0], GREEN)
        self.assertEqual(r.orange.side[0][2], RED)

        for i in range(3):
            r.move("L")

        self.assertEqual(r, res)

    def test_left_reverse_rotation(self):
        r = Rubik()

        r.white.side[2][0] = ORANGE
        r.red.side[2][0] = GREEN
        r.yellow.side[2][0] = RED
        r.orange.side[2][2] = BLUE

        res = r.__copy__()
        r.move("L'")
        self.assertEqual(r.white.side[2][0], GREEN)
        self.assertEqual(r.red.side[2][0], RED)
        self.assertEqual(r.yellow.side[0][0], BLUE)
        self.assertEqual(r.orange.side[0][2], ORANGE)

        for i in range(3):
            r.move("L'")

        self.assertEqual(r, res)

    def test_left_180_rotation(self):
        r = Rubik()

        r.white.side[2][0] = ORANGE
        r.red.side[2][0] = GREEN

        r.yellow.side[2][0] = RED
        r.orange.side[2][2] = BLUE

        res = r.__copy__()
        r.move("2L")
        self.assertEqual(r.white.side[2][0], RED)
        self.assertEqual(r.red.side[0][0], BLUE)
        self.assertEqual(r.yellow.side[2][0], ORANGE)
        self.assertEqual(r.orange.side[0][2], GREEN)

        r.move("2L")

        self.assertEqual(r, res)


if __name__ == '__main__':
    unittest.main()
