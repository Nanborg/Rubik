import unittest

from common.cube import apply_move
from common.moves import SOLVED
from solving.f2l import is_f2l_solved, f2l_actions, F2L_PAIRS, f2l_transitions, f2l_key, solve_pair, is_pair_solved
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

    def test_action_transitions(self):
        initial = list(SOLVED)

        for move in ("R", "D", "R'", "F'", "D2", "F"):
            initial = apply_move(initial, move)

        for action in f2l_actions():
            with self.subTest(action=action):
                table = f2l_transitions(action)
                key = f2l_key(initial, F2L_PAIRS)
                expected = tuple(table[piece] for piece in key)
                state = list(initial)
                for move in action:
                    state = apply_move(state, move)
                self.assertEqual(f2l_key(state, F2L_PAIRS), expected)

    def test_solve_pair(self):
        pair = F2L_PAIRS[0]
        state = list(SOLVED)

        for move in ("R'", "D", "R"):
            state = apply_move(state, move)
        self.assertFalse(is_pair_solved(state, *pair))
        initial = list(state)
        solution = solve_pair(state, pair)
        self.assertEqual(state, initial)
        for move in solution:
            state = apply_move(state, move)
        self.assertTrue(is_pair_solved(state, *pair))
        self.assertTrue(is_cross_solved(state))
