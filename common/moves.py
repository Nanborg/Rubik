# TODO(shared): parser et valider les 18 mouvements autorisés.

from random import choice


# Genere un melange sans repeter la meme face de suite
def random_scramble(length=20):
    moves = []
    faces = "UDLRFB"
    for _ in range(length):
        face = choice(faces)
        moves.append(face + choice(("", "'", "2")))
        faces = "UDLRFB".replace(face, "")
    return moves


# Recoit un mouvement valide
# Renvoie le nombre de quarts de tour : 1, 2 ou 3
def quarter_turns(move: str) -> int:
    return {"": 1, "2": 2, "'": 3}[move[1:]]

# Recoit le texte des mouvements
# Separe les mouvements et verifie leurs notation
# Renvoie les mouvements dans leur ordre de lecture
# Leve ValueError si un mouvement est invalide
def parse_moves(text: str) -> tuple[str, ...]:
    moves = tuple(text.split())
    allowed = {
    face + suffix
    for face in "UDLRFB"
    for suffix in ("", "'", "2")
    }
    for move in moves:
        if move not in allowed:
            raise ValueError(f"mouv invalide : {move}")
    return moves

# Lit les sequences et une section optionnelle du fichier
def load_table_algorithms(path, section=None):
    algorithms = []
    current = None
    with open(path, encoding="utf-8") as file:
        for line in file:
            text = line.strip()
            if text.startswith("# [") and text.endswith("]"):
                current = text[3:-1]
            elif text and not text.startswith("#"):
                if section is None or current == section:
                    algorithms.append(parse_moves(text))
    return algorithms

# Change le point de vue autour de U et D sans ajouter de mouvement
def rotate_algorithm(algorithm, turns):
    faces = "RFLB"
    rotation = str.maketrans(faces, faces[turns:] + faces[:turns])
    return tuple(move.translate(rotation) for move in algorithm)

def cycle(cube: list[tuple], commutator:list[int], n:int) -> list[tuple]:
	"""
	applies specified commutator to cube<br>
	**/!\\ WARNING: does not rotate pieces, you have to take care of that yourself**
	"""
	for i in range(len(commutator) - n):
		cube[commutator[i]], cube[commutator[i + n]] = cube[commutator[i + n]], cube[commutator[i]]
	return cube

#renvoie le mouvement qui annule celui recu
def inverse_move(move):
	if move.endswith("2"):
		return move
	if move.endswith("'"):
		return move[0]
	return move + "'"






if __name__ == "__main__":
	from common.cube import Positions as pos, print_cube, SOLVED

	print("hello")
	#print(SOLVED)
	print_cube(SOLVED)
	print_cube(cycle(SOLVED, [pos.FU, pos.FR, pos.FD, pos.FL], 1))

#Fusionne les moves consecutifs d'une meme face
#supprime ceux qui s'annulent
def simplify_move(moves):
	result = []
	for move in moves:
		face = move[0]
		turns = quarter_turns(move)
		if result and result[-1][0] == face:
			previous = result.pop()
			turns = (quarter_turns(previous) + turns) % 4
		if turns != 0:
			suffix = {1: "", 2: "2", 3: "'"}[turns]
			result.append(face + suffix)

	return result
