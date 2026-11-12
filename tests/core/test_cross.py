
import unittest

from common.cube import apply_move, Positions, SOLVED
from solving.cross import is_cross_solved, find_edge, cross_key, solve_cross
from random import Random

class TestCross(unittest.TestCase):
	# Verifie la croix du cube resolu
	def test_solved_cube(self):
		self.assertTrue(is_cross_solved(SOLVED))

	# Verifie la detection d'une croix decalee
	def test_misaligned_cross(self):
		state = apply_move(SOLVED, "U")

		self.assertFalse(is_cross_solved(state))

	# Verifie la position d'une arete deplacee
	def test_find_moved_edge(self):
		state = apply_move(SOLVED, "F")
		position = find_edge(state, SOLVED[Positions.UF])

		self.assertEqual(position, Positions.FR)

	# Verifie les positions et orientations des aretes blanches
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

	# Verifie la resolution de la croix sans modifier le cube fourni
	def test_solve_cross(self):
		#state = apply_move(SOLVED, "F")
		scrambles = (
			("F",),
			("R", "U"),
			("R", "U", "F2"),
			("R", "U", "F2", "L'", "D", "B2", "R2", "U'", "F", "D2",)
		)

		for scramble in scrambles:
			with self.subTest(scramble = scramble):
				state = list(SOLVED)

				for move in scramble:
					state = apply_move(state, move)
				initial = list(state)
				solution = solve_cross(state)

				self.assertEqual(state, initial)
				for move in solution:
					state = apply_move(state, move)

				self.assertTrue(is_cross_solved(state))
				self.assertLessEqual(len(solution), len(scramble))
				#self.assertEqual(initial, apply_move(SOLVED, "F"))

	# Verifie la croix sur des melanges reproductibles
	def test_random_scrambles(self):
		moves = tuple(
			face + suffix
			for face in "UDLRFB"
			for suffix in ("", "'", "2")
		)

		for seed in range(3):
			with self.subTest(seed=seed):
				random = Random(seed)
				state = list(SOLVED)

				for _ in range(20):
					state = apply_move(state, random.choice(moves))
				solution = solve_cross(state)
				for move in solution:
					state = apply_move(state, move)
				self.assertTrue(is_cross_solved(state))
