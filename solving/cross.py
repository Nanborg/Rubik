# TODO(nicolsan): résoudre la croix dans le repère convenu.

from common.cube import Positions, apply_move, SOLVED
from common.moves import inverse_move
from common.colors import Colors
from solving.search import bidirectional_search

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

# Calcule le trajet des aretes pour un movement
def edge_transitions(move):
    moved = apply_move(SOLVED, move)
    transitions = {}

    for source, piece in enumerate(SOLVED[:12]):
        destination = find_edge(moved, piece)

        for color_index, color in enumerate(piece):
            new_index = moved[destination].index(color)

            transitions[source, color_index] = (
                destination,
                new_index,
            )
    return transitions



# Prepare ke recherche des mouv pour resoudre la croix
def solve_cross(state):
    if is_cross_solved(state):
        return []

    moves = tuple(
        face + suffix
        for face in "UDLRFB"
        for suffix in ("", "'", "2")
    )

    transitions = {move: edge_transitions(move) for move in moves}
    start = cross_key(state)
    goal = cross_key(SOLVED)
    return bidirectional_search(start, goal, transitions, inverse_move)
