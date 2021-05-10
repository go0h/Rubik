import rubik.CubieCube as cc
import rubik.Tables as tb


class CoordCubie:
    """http://kociemba.org/math/coordlevel.htm
        Представление перестановок и ориетанция углов и ребер куба, с помощью натуральных чисел"""
    def __init__(self, cubie: cc.CubieCube = None):
        self.cubie = cubie
        self.corner_twist = cubie.get_corners_twist()
        self.edge_flip = cubie.get_edges_flip()
        self.slice_sorted = cubie.get_ud_slice_sorted()
        self.u_edges = cubie.get_u_edges()
        self.d_edges = cubie.get_d_edges()
        self.corners = cubie.get_corners()
        if self.slice_sorted < 24:
            self.ud_edges = cubie.get_ud_edges()
        else:
            self.ud_edges = -1

        self.fs_classidx = tb.fs_classidx[2048 * (self.slice_sorted // 24) + self.edge_flip]
        self.fs_sym = tb.fs_sym[2048 * (self.slice_sorted // 24) + self.edge_flip]
        self.fs_rep = tb.fs_rep[self.fs_classidx]

        self.co_classidx = tb.co_classidx[self.corners]
        self.co_sym = tb.co_sym[self.corners]
        self.co_rep = tb.co_rep[self.co_classidx]
