# TODO(Neon): résoudre la croix dans le repère convenu.

from common.cube import Positions, apply_move
from common.moves import SOLVED
from common.colors import Colors
from collections import deque



# Verifie les 4 arretes de la croix blance
# Compare leur position et orientation au cube resolu
def is_cross_solved(state):
    positions = (
        Positions.UF,
        Positions.UR,
        Positions.UB,
        Positions.UL,
    )

    return all(state[position] == SOLVED[position] for position in positions)


# Cherche une arete par ses 2 couleurs
# Renvoie sa position meme si elle est retournee
def find_edge(state, colors):
    for position, piece in enumerate(state[:12]):
        if set(piece) == set(colors):
            return position
    raise ValueError("Arete introuvable")

#retiens la position et l'orientation des 4 arretes blanches
def cross_key(state):
    key = []

    for target in (Positions.UF, Positions.UR, Positions.UB, Positions.UL):
        position = find_edge(state, SOLVED[target])
        white_index = state[position].index(Colors.WHITE)

        key.append((position, white_index))

    return tuple(key)

# Prepare ke recherche des mouv pour resoudre la croix
def solve_cross(state):
    if is_cross_solved(state):
        return []

    moves = tuple(
        face + suffix
        for face in "UDLRFB"
        for suffix in ("", "'", "2")
    )

    queue = deque([(list(state), [])])
    visited = {cross_key(state)}

    while queue:
        current, path = queue.popleft()

        for move in moves:
            next_state = apply_move(current, move)
            key = cross_key(next_state)

            if key in visited:
                continue

            next_path = path + [move]
            if is_cross_solved(next_state):
                return next_path

            visited.add(key)
            queue.append((next_state, next_path))
    raise ValueError("Aucune solution pour la croix")
