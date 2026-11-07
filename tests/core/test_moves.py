
import unittest

from common.moves import simplify_move

class TestMoves(unittest.TestCase):
    # Verifie les fusions et annulations sans modifier la liste fournie
    def test_simplfy_moves(self):
        cases = (
        ([], []),
        (["R", "R"], ["R2"]),
        (["R", "R'"], []),
        (["R2", "R"], ["R'"]),
        (["R2", "R2"], []),
        (["R", "U", "U'", "R"], ["R2"]),
        (["R", "U"], ["R", "U"]),
        )
        for moves, expected in cases:
            with self.subTest(moves=moves):
                initial = list(moves)

                self.assertEqual(simplify_move(moves), expected)
                self.assertEqual(moves, initial)
