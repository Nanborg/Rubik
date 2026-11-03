# TODO(shared): tester les 18 mouvements avec des états attendus indépendants.

import unittest
from common.cube import apply_move
from common.moves import SOLVED
from rotation_reference import to_stickers, reference_move

MOVES = (
    "U", "U'", "U2",
    "D", "D'", "D2",
    "L", "L'", "L2",
    "R", "R'", "R2",
    "F", "F'", "F2",
    "B", "B'", "B2",
)

def inverse_move(move):
    if move.endswith("2"):
        return move
    if move.endswith("'"):
        return move[0]

    return move + "'"

def play_sequence(state, moves, move_function=apply_move):
    result = state.copy()

    for move in moves:
        result = move_function(result, move)
    return result

class TestRotations(unittest.TestCase):
    def test_u(self):
        expected = [
            SOLVED[3], SOLVED[1], SOLVED[2], SOLVED[6],
            SOLVED[4], SOLVED[5], SOLVED[9], SOLVED[7],
            SOLVED[8], SOLVED[0], SOLVED[10], SOLVED[11],
            SOLVED[14], SOLVED[12], SOLVED[15], SOLVED[13],
            SOLVED[16], SOLVED[17], SOLVED[18], SOLVED[19],
        ]

        self.assertEqual(apply_move(SOLVED, "U"), expected)

    def test_repeated_moves(self):
        for move in MOVES:
            with self.subTest(move=move):
                count = 2 if move.endswith("2") else 4
                result = play_sequence(SOLVED, (move,) * count)
                self.assertEqual(result, SOLVED)

    def test_move_and_inverse(self):
        for move in MOVES:
            with self.subTest(move=move):
                sequence = (move, inverse_move(move))
                result = play_sequence(SOLVED, sequence)

                self.assertEqual(result, SOLVED)

    def test_moves_against_reference(self):
        for move in MOVES:
            with self.subTest(move=move):
                expected = play_sequence(
                    to_stickers(SOLVED), (move,), reference_move
                )
                actual = to_stickers(play_sequence(SOLVED, (move,)))
                self.assertEqual(actual, expected)
