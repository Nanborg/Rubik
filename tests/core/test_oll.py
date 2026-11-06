
import unittest

from common.cube import apply_move
from common.moves import SOLVED, inverse_move
from solving.f2l import is_f2l_solved
from solving.oll import is_oll_solved, build_oll_table, solve_oll, load_oll_algorithms
from pathlib import Path

class TestOLL(unittest.TestCase):
    def test_solved_cube(self):
        self.assertTrue(is_oll_solved(SOLVED))
    def test_last_layer_turn(self):
        state = apply_move(SOLVED, "D")
        self.assertTrue(is_oll_solved(state))
    def test_unoriented_last_layer(self):
        state = list(SOLVED)
        for move in ("R", "D", "R'", "D", "R", "D2", "R'"):
            state = apply_move(state, move)
        self.assertTrue(is_f2l_solved(state))
        self.assertFalse(is_oll_solved(state))

    def test_solve_oll(self):
        path = Path(__file__).resolve().parents[2] / "data/cfop/oll.txt"
        algorithms = load_oll_algorithms(path)
        self.assertTrue(algorithms)
        table = build_oll_table(algorithms)
        for algorithm in algorithms:
            for setup in ((), ("D",), ("D2",), ("D'",)):
                with self.subTest(algorithm=algorithm, setup=setup):
                    state = list(SOLVED)
                    for move in reversed(algorithm):
                        state = apply_move(state, inverse_move(move))
                    for move in setup:
                        state = apply_move(state, move)
                    initial = list(state)
                    solution = solve_oll(state, table)
                    self.assertEqual(state, initial)
                    for move in solution:
                        state = apply_move(state, move)
                    self.assertTrue(is_oll_solved(state))
