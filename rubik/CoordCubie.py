import rubik.CubieCube as cc
import rubik.Tables as tb
import rubik.Utils as u


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

        # перестановки и ориентация UD-среза
        self.fs_classidx = tb.fs_classidx[2048 * (self.slice_sorted // 24) + self.edge_flip]
        # номер симметрии
        self.fs_sym = tb.fs_sym[2048 * (self.slice_sorted // 24) + self.edge_flip]
        # первое вхождение класса эквивалентности
        self.fs_rep = tb.fs_rep[self.fs_classidx]

        # перестановки 8 углов
        self.co_classidx = tb.co_classidx[self.corners]
        # номер симметрии
        self.co_sym = tb.co_sym[self.corners]
        # первое вхождение класса эквивалентности
        self.co_rep = tb.co_rep[self.co_classidx]

    def get_phase1_depth(self):
        """@:return Миимальное количество ходов требуемое для достижения рандомного кубика фазы 2"""
        slice_ = self.slice_sorted // 24
        flip_ = self.edge_flip
        twist_ = self.corner_twist
        fs_ = 2048 * slice_ + flip_
        classidx_ = tb.fs_classidx[fs_]
        sym = tb.fs_sym[fs_]
        # 3^7 * класс экв + ориентация 8 углов
        depth_mod3 = tb.get_fs_twist_depth3(2187 * classidx_ + tb.twist_conj[(twist_ << 4) + sym])

        depth = 0
        # первая фаза, считается законченой, когда ориентации всех углов и ребер равны 0
        while twist_ != 0 or flip_ != 0 or slice_ != 0:
            # print(f"twist = {twist_}, flip = {flip_}, slice = {slice_}")
            if depth_mod3 == 0:
                depth_mod3 = 3
            # для текущего состояния применяем всех ходы поочередно
            # и вычисляем количество ходов небходимое для достижения Фазы 2
            for move in range(18):
                twist1 = tb.move_twist[18 * twist_ + move]
                flip1 = tb.move_flip[18 * flip_ + move]
                slice1 = tb.move_slice_sorted[18 * slice_ * 24 + move] // 24
                fs1 = 2048 * slice1 + flip1
                classidx1 = tb.fs_classidx[fs1]
                sym = tb.fs_sym[fs1]
                if tb.get_fs_twist_depth3(2187 * classidx1 + tb.twist_conj[(twist1 << 4) + sym]) == depth_mod3 - 1:
                    depth += 1
                    twist_ = twist1
                    flip_ = flip1
                    slice_ = slice1
                    depth_mod3 = depth_mod3 - 1
                    break
        return depth

    @staticmethod
    def get_phase2_depth(corners, ud_edges):
        classidx = tb.co_classidx[corners]
        sym = tb.co_sym[corners]
        depth_mod3 = tb.get_co_ud_edges_depth3(40320 * classidx + tb.conj_ud_edges[(ud_edges << 4) + sym])

        if depth_mod3 == 3:
            return 11

        depth = 0
        while corners != 0 or ud_edges != 0:
            if depth_mod3 == 0:
                depth_mod3 = 3
            for move in u.PHASE2_MOVES:
                corners1 = tb.move_corners[18 * corners + move]
                ud_edges1 = tb.move_ud_edges[18 * ud_edges + move]
                classidx1 = tb.co_classidx[corners1]
                sym = tb.co_sym[corners1]

                if tb.get_co_ud_edges_depth3(40320 * classidx1 + tb.conj_ud_edges[(ud_edges1 << 4) + sym]) == depth_mod3 - 1:
                    depth += 1
                    corners = corners1
                    ud_edges = ud_edges1
                    depth_mod3 = depth_mod3 - 1
                    break
        return depth

