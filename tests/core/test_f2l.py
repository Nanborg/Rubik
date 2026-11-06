import unittest

from common.cube import apply_move, SOLVED
from solving.f2l import is_f2l_solved, f2l_actions, F2L_PAIRS, f2l_transitions, f2l_key, solve_pair, is_pair_solved, solve_f2l
from solving.cross import is_cross_solved, solve_cross
from random import Random

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

    def test_solve_pair_preserve_others(self):
        pair = F2L_PAIRS[0]
        protected = F2L_PAIRS[1:]
        state = list(SOLVED)

        for move in ("R'", "D", "R"):
            state = apply_move(state, move)
        for corner, edge in protected:
            self.assertTrue(is_pair_solved(state, corner, edge))
        solution = solve_pair(state, pair, protected)
        for move in solution:
            state = apply_move(state, move)
        self.assertTrue(is_f2l_solved(state))

    def test_solve_f2l(self):
        state = list(SOLVED)
        for move in ("R'", "D", "R", "L", "D2", "L'"):
            state = apply_move(state, move)
        self.assertTrue(is_cross_solved(state))
        self.assertFalse(is_f2l_solved(state))
        initial = list(state)
        solution = solve_f2l(state)
        self.assertEqual(state, initial)
        for move in solution:
            state = apply_move(state, move)
        self.assertTrue(is_f2l_solved(state))

    def test_cross_and_f2l(self):
        moves = tuple(
            face + suffix
            for face in "UDLRFB"
            for suffix in ("", "'", "2")
        )

        for seed in range(10):
            with self.subTest(seed=seed):
                random = Random(seed)
                state = list(SOLVED)

                for _ in range(20):
                    state = apply_move(state, random.choice(moves))
                for solver in (solve_cross, solve_f2l):
                    for move in solver(state):
                        state = apply_move(state, move)
                self.assertTrue(is_f2l_solved(state))
