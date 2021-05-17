
import unittest
from rubik.Tables import *


class LoadTablesTest(unittest.TestCase):

    def test_load_move_tables(self):

        self.assertTrue(len(move_twist) == 2187 * 18)
        self.assertTrue(len(move_flip) == 2048 * 18)
        self.assertTrue(len(move_slice_sorted) == 11880 * 18)
        self.assertTrue(len(move_ud_edges) == 40320 * 18)
        self.assertTrue(len(move_corners) == 40320 * 18)

    def test_load_sym_tables(self):

        self.assertTrue(len(twist_conj) == 2187 * 16)
        self.assertTrue(len(conj_ud_edges) == 40320 * 16)

        self.assertTrue(len(fs_classidx) == 2048 * 495)
        self.assertTrue(len(fs_sym) == 2048 * 495)

        self.assertTrue(len(co_classidx) == 40320)
        self.assertTrue(len(co_sym) == 40320)

    def test_load_pruning_tables(self):
        self.assertTrue(len(phase1_prun) == 64430 * 2187 // 16 + 1)
        self.assertTrue(len(phase2_prun) == 6975360)
