import unittest

from common.cube import apply_move
from common.moves import SOLVED
from solving.f2l import is_f2l_solved, f2l_actions
from solving.cross import is_cross_solved


class TestF2L(unittest.TestCase):
    def test_solved_cube(self):
        self.assertTrue(is_f2l_solved(SOLVED))
    def test_last_layer_move(self):
        state = apply_move(SOLVED, "D")
        self.assertTrue(is_f2l_solved(state))
    def test_broken_f2l(self):
        state = apply_move(SOLVED, "R")
        self.assertFalse(is_f2l_solved(state))

    def test_action_preserve_cross(self):
        for action in f2l_actions():
            with self.subTest(action=action):
                state = list(SOLVED)
                for move in action:
                    state = apply_move(state, move)
                self.assertTrue(is_cross_solved(state))
