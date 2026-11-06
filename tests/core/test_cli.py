import subprocess
import sys
import unittest
from pathlib import Path

from common.cube import SOLVED, apply_moves
from common.moves import parse_moves


RUBIK = Path(__file__).resolve().parents[2] / "rubik"


class TestCLI(unittest.TestCase):
    # Verifie les erreurs sans sortie de solution ni traceback
    def test_invalid_inputs(self):
        inputs = [[], ["R", "U"]]
        inputs += [[move] for move in ("R3", "R2'", "F''", "r", "M", "E", "S", "x", "y", "z")]
        for args in inputs:
            with self.subTest(args=args):
                result = subprocess.run([sys.executable, str(RUBIK), *args],
                                        capture_output=True, text=True, timeout=3)
                self.assertEqual(result.returncode, 1)
                self.assertEqual(result.stdout, "")
                self.assertTrue(result.stderr)
                self.assertNotIn("Traceback", result.stderr)

    # Verifie la sortie de solution et le cube deja resolu
    def test_valid_inputs(self):
        for scramble in ("R U F2", "", "R R'", "  D  L2   B'  "):
            with self.subTest(scramble=scramble):
                result = subprocess.run([sys.executable, str(RUBIK), scramble],
                                        capture_output=True, text=True, timeout=3)
                self.assertEqual(result.returncode, 0)
                self.assertEqual(result.stderr, "")
                self.assertEqual(result.stdout.count("\n"), 1)
                state = apply_moves(SOLVED, parse_moves(scramble))
                self.assertEqual(apply_moves(state, parse_moves(result.stdout)), SOLVED)
                if state == SOLVED:
                    self.assertEqual(result.stdout, "\n")
