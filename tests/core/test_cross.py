
import unittest

from common.cube import apply_move, Positions
from common.moves import SOLVED
from solving.cross import is_cross_solved, find_edge, cross_key, solve_cross


class TestCross(unittest.TestCase):
    def test_solved_cube(self):
        self.assertTrue(is_cross_solved(SOLVED))

    def test_misaligned_cross(self):
        state = apply_move(SOLVED, "U")

        self.assertFalse(is_cross_solved(state))

    def test_find_moved_edge(self):
        state = apply_move(SOLVED, "F")
        position = find_edge(state, SOLVED[Positions.UF])

        self.assertEqual(position, Positions.FR)

    def test_cross_key(self):
        state = apply_move(SOLVED, "F'")

        self.assertEqual(
            cross_key(state),
            (
                (Positions.FL, 1),
                (Positions.UR, 0),
                (Positions.UB, 0),
                (Positions.UL, 0),
            ),
        )

    def test_solve_cross(self):
        state = apply_move(SOLVED, "F")
        initial = list(state)
        solution = solve_cross(state)

        for move in solution:
            state = apply_move(state, move)

        self.assertTrue(is_cross_solved(state))
        self.assertEqual(len(solution), 1)
        self.assertEqual(initial, apply_move(SOLVED, "F"))
