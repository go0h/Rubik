import unittest
from rubik.Tables import *
from math import factorial


class LoadTablesTest(unittest.TestCase):

    def test_load_sym_tables(self):
        self.assertTrue(len(conj_twist) == 3 ** 7)
        self.assertTrue(len(conj_ud_edges) == factorial(8))
        self.assertTrue(len(fs_classidx) == 2048 * 495)
        self.assertTrue(len(co_classidx) == factorial(8))

    def test_load_pruning_tables(self):
        self.assertTrue(len(phase1_prun) == 64430 + 1)
        self.assertTrue(len(phase2_prun) == 2768)

    def test_load_moves_tables(self):
        self.assertTrue(len(move_twist) == 3 ** 7)

        self.assertTrue(len(move_flip) == 2 ** 11)
        self.assertTrue(len(move_slice_sorted) == 12 * 11 * 10 * 9)

        self.assertTrue(len(move_corners) == factorial(8))
        self.assertTrue(len(move_ud_edges) == factorial(8))
