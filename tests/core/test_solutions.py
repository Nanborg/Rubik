import unittest
from random import Random

from common.cube import SOLVED, apply_moves
from common.moves import parse_moves
from solving.cfop import solve
from solving.cross import is_cross_solved
from solving.f2l import is_f2l_solved
from solving.oll import is_oll_solved


class TestSolutions(unittest.TestCase):
	# Verifie que melange et solution rendent le cube resolu
	def test_complete_solution(self):
		scramble = parse_moves("R U F2 L' D B2 R2 U' F D2")
		solution = solve(scramble)
		state = apply_moves(SOLVED, scramble)
		state = apply_moves(state, solution)
		self.assertEqual(state, SOLVED)
	# Verifie qu'un cube resolu ne demande aucun mouvement
	def test_solved_cube(self):
		self.assertEqual(solve(()), [])

	# Verifie la solution complete et le resultat de chaque etape
	def check_solution(self, scramble):
		solution, steps = solve(scramble, with_steps=True)
		initial = apply_moves(SOLVED, scramble)
		self.assertEqual(apply_moves(initial, solution), SOLVED)
		self.assertEqual(parse_moves(" ".join(solution)), tuple(solution))
		self.assertEqual(tuple(name for name, _ in steps), ("Croix", "F2L", "OLL", "PLL"))

		current = initial
		checks = (is_cross_solved, is_f2l_solved, is_oll_solved, lambda state: state == SOLVED)
		for (name, moves), check in zip(steps, checks):
			with self.subTest(stage=name):
				current = apply_moves(current, moves)
				self.assertTrue(check(current))

	# Verifie les melanges qui laissent le cube resolu
	def test_cancellations(self):
		for text in ("", "R R'", "F2 F2", "U U U U", "R U U' R'"):
			with self.subTest(scramble=text):
				scramble = parse_moves(text)
				self.assertEqual(solve(scramble), [])
				self.check_solution(scramble)

	# Verifie les melanges courts et longs avec des graines fixes
	def test_reproducible_scrambles(self):
		for seed in range(3):
			for length in (1, 4, 5, 20, 21, 30, 40, 80):
				random = Random(seed)
				scramble = []
				faces = "UDLRFB"
				for _ in range(length):
					face = random.choice(faces)
					scramble.append(face + random.choice(("", "'", "2")))
					faces = "UDLRFB".replace(face, "")
				with self.subTest(seed=seed, length=length, scramble=" ".join(scramble)):
					self.check_solution(tuple(scramble))

	# Verifie le superflip indique dans les points a verifier
	def test_superflip(self):
		scramble = parse_moves("U R2 F B R B2 R U2 L B2 R U' D' R2 F R' L B2 U2 F2")
		self.check_solution(scramble)
