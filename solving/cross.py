# TODO(Neon): résoudre la croix dans le repère convenu.

from common.cube import Positions, apply_move
from common.moves import SOLVED, inverse_move
from common.colors import Colors


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

# Explore un lvl de recherche
# renvoie la prochaine frontiere et un point de rencontre
def expand_cross_layer(frontier, paths, other_paths, transitions):
    next_frontier = []

    for current in frontier:
        for move, table in transitions.items():
            key = tuple(table[edge] for edge in current)
            if key in paths:
                continue
            paths[key] = paths[current] + [move]

            if key in other_paths:
                return next_frontier, key
            next_frontier.append(key)
    return next_frontier, None


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
    forward = [start]
    backward = [goal]

    forward_paths = {start: []}
    backward_paths = {goal: []}

    while forward and backward:
        if len(forward) <= len (backward):
            forward, meeting = expand_cross_layer(
                forward, forward_paths, backward_paths, transitions
            )
        else:
            backward, meeting = expand_cross_layer(
                backward, backward_paths, forward_paths, transitions
            )
        if meeting is not None:
            end_path = [
                inverse_move(move)
                for move in reversed(backward_paths[meeting])
            ]
            return forward_paths[meeting] + end_path
    raise ValueError("Aucune solution pour la croix")
