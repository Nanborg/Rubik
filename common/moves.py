# TODO(shared): parser et valider les 18 mouvements autorisés.
from common.colors import Colors, COLOR_TEXT
from common.cube import Positions as pos, print_cube, SOLVED

def cycle(cube: list[tuple], commutator:list[pos], n:int) -> list[tuple]:
	"""
	applies specified commutator to cube<br>
	**/!\\ WARNING: does not rotate pieces, you have to take care of that yourself**
	"""
	for i in range(len(commutator) - n):
		cube[commutator[i]], cube[commutator[i + n]] = cube[commutator[i + n]], cube[commutator[i]]
	return cube

if __name__ == "__main__":
	print("hello")
	#print(SOLVED)
	print_cube(SOLVED)
	print_cube(cycle(SOLVED, [pos.FU, pos.FR, pos.FD, pos.FL], 1))
