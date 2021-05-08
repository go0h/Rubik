
import rubik.CubieCube as cc
import rubik.FaceletCube as fc


class TwoPhaseSolver:

    def __init__(self, cubie: cc.CubieCube):
        self.cubie = cubie
        self.moves_p1 = []
        self.moves_p2 = []

    def solve(self) -> list:
        print("START TO SOLVE")
        return self.moves_p1 + self.moves_p2
