import unittest

from common.cube import SOLVED, apply_move
from solving.oll import is_oll_solved
from solving.pll import is_cube_solved, solve_pll, build_pll_table
from common.moves import inverse_move

class TestPLL(unittest.TestCase):
    def test_solve_cube(self):
        self.assertTrue(is_cube_solved(SOLVED))
    def test_last_layer_alignement(self):
        state = apply_move(SOLVED, "D")
        self.assertTrue(is_oll_solved(state))
        self.assertFalse(is_cube_solved(state))

    def test_solve_alignement(self):
        table = build_pll_table(())
        for move in ("D", "D2", "D'"):
            with self.subTest(move=move):
                state = apply_move(SOLVED, move)
                initial = list(state)
                solution = solve_pll(state, table)
                self.assertEqual(state, initial)
                for step in solution:
                    state = apply_move(state, step)
                self.assertTrue(is_cube_solved(state))
                self.assertEqual(len(solution), 1)
    def test_solve_permutation(self):
        algorithm = (
            "R", "D", "R'", "D'", "R'", "B" , "R2",
            "D'", "R'", "D'", "R", "D", "R'", "B'",
        )
        table = build_pll_table((algorithm,))
        for setup in ((), ("D",), ("D2",), ("D'",)):
            with self.subTest(setup=setup):
                state = list(SOLVED)
                for move in reversed(algorithm):
                    state = apply_move(state, inverse_move(move))
                for move in setup:
                    state = apply_move(state, move)
                self.assertTrue(is_oll_solved(state))
                self.assertFalse(is_cube_solved(state))
                initial = list(state)
                solution = solve_pll(state, table)
                self.assertEqual(state, initial)
                for move in solution:
                    state = apply_move(state, move)
                self.assertTrue(is_cube_solved(state))
