import unittest

from common.cube import SOLVED, apply_moves
from common.moves import parse_moves
from solving.cfop import solve


class TestSolutions(unittest.TestCase):
    def test_complete_solution(self):
        scramble = parse_moves("R U F2 L' D B2 R2 U' F D2")
        solution = solve(scramble)
        state = apply_moves(SOLVED, scramble)
        state = apply_moves(state, solution)
        self.assertEqual(state, SOLVED)
    def test_solved_cube(self):
        self.assertEqual(solve(()), [])
