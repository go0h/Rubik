import rubik.CubieCube as cc


class CoordCubie:
    """http://kociemba.org/math/coordlevel.htm
        Представление перестановок и ориетанция углов и ребер куба, с помощью натуральных чисел"""
    def __init__(self, cubie: cc.CubieCube = None):
        self.cubie = cubie
        self.corner_twist = 0
        self.edge_flip = 0
        self.slice = 0


