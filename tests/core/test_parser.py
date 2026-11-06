# TODO(shared): tester les mouvements valides, invalides et les espaces.

import unittest

from common.moves import parse_moves

class TestParser(unittest.TestCase):
    # Verifie que les 18 mouvements sont acceptes
    # Verifie que leur ordre est conserve
    def test_valid_moves(self):
        self.assertEqual(
            parse_moves("U U' U2 D D' D2 L L' L2 R R' R2 F F' F2 B B' B2"),
            (
                "U", "U'", "U2", "D", "D'", "D2",
                "L", "L'", "L2", "R", "R'", "R2",
                "F", "F'", "F2", "B", "B'", "B2",
            ),
        )

    # Verifie que les espcaes en trop sont ignores
    def test_extra_spaces(self):
        self.assertEqual(
            parse_moves (" D  L2   B'   "),
            ("D", "L2", "B'"),
        )

    # Verifie que les notations interdites sont refusees
    def test_invalid_move(self):
        for move in ("X", "u", "R3", "U2'", "F''", "UD", "M"):
            with self.subTest(move=move):
                with self.assertRaises(ValueError):
                    parse_moves(move)

    # Verifie que toute la suite est refusee si un mouvement est invalide
    def test_invalid_move_in_sequence(self):
        with self.assertRaises(ValueError):
            parse_moves("U X R2")
