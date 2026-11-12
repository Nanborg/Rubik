from common.cube import SOLVED, apply_move
from solving.oll import OLL_POSITIONS, is_oll_solved
from common.moves import inverse_move, simplify_move, load_table_algorithms, rotate_algorithm
from pathlib import Path
from functools import cache

#Verifie tout les position et orientation du cube
def is_cube_solved(state):
	return state == SOLVED

# Identifie les pieces de la derniere couche
# Necessite une couche deja orientee par OLL
def pll_key(state):
	key = []
	for position in OLL_POSITIONS:
		key.append(SOLVED.index(state[position]))
	return tuple(key)

# constuit la permutation resolu par un algo
# verifie que F2L est conserves
def pll_case(algorithm):
	state = list(SOLVED)
	for move in reversed(algorithm):
		state = apply_move(state, inverse_move(move))
	if not is_oll_solved(state):
		raise ValueError("cet algo casse OLL")
	return pll_key(state)

#Associe chaque perm a sa solution
# Essaie les 4 alignements finaux
def build_pll_table(algorithms):
	table = {pll_key(SOLVED): ()}
	for algorithm in algorithms:
		for finish in ((), ("D",), ("D2",), ("D'",)):
			moves = simplify_move(list(algorithm) + list(finish))
			key = pll_case(moves)
			if key not in table or len(moves) < len(table[key]):
				table[key] = tuple(moves)
	return table

# Cherche la perme avec les 4 alignements
# renvoie la solution la plus courte (cube protegee)
def solve_pll(state, table=None ):
	if not is_oll_solved(state):
		raise ValueError("OLL doit etre resolu")
	if table is None:
		table = load_pll_table()
	best = None
	for setup in ((), ("D",), ("D2",), ("D'",)):
		current = list(state)
		for move in setup:
			current = apply_move(current, move)
		algorithm = table.get(pll_key(current))
		if algorithm is None:
			continue
		moves = simplify_move(list(setup) + list(algorithm))
		if best is None or len(moves) < len(best):
			best = moves
	if best is None:
		raise ValueError("Cas hors table")
	return best

#lit les sequence di fichier pll
def load_pll_algorithms(path):
	return load_table_algorithms(path)

@cache
def load_pll_table():
	path = Path(__file__).resolve().parents[1] / "data/cfop/pll.txt"
	algorithms = [
		rotate_algorithm(algorithm, turns)
		for algorithm in load_table_algorithms(path)
		for turns in range(4)
	]
	return build_pll_table(algorithms)
