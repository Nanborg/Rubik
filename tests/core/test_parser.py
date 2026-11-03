# TODO(shared): tester les mouvements valides, invalides et les espaces.

import unittest

from common.moves import parse_moves

class TestParser(unittest.TestCase):
    def test_valid_moves(self):
        self.assertEqual(
            parse_moves("U U' U2 D D' D2 L L' L2 R R' R2 F F' F2 B B' B2"),
            (
                "U", "U'", "U2", "D", "D'", "D2",
                "L", "L'", "L2", "R", "R'", "R2",
                "F", "F'", "F2", "B", "B'", "B2",
            ),
        )

    def test_extra_spaces(self):
        self.assertEqual(
            parse_moves (" D  L2   B'   "),
            ("D", "L2", "B'"),
        )

    def test_invalid_move(self):
        for move in ("X", "u", "R3", "U2'", "F''", "UD", "M"):
            with self.subTest(move=move):
                with self.assertRaises(ValueError):
                    parse_moves(move)

    def test_invalid_move_in_sequence(self):
        with self.assertRaises(ValueError):
            parse_moves("U X R2")
