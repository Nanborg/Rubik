# TODO(Neon): résoudre les quatre paires coin/arête sans casser la croix.

from common.cube import Positions, apply_move
from common.moves import SOLVED, inverse_move
from solving.cross import is_cross_solved
from solving.search import bidirectional_search
from itertools import permutations
from common.moves import simplify_move
from functools import cache

F2L_PAIRS = (
    (Positions.URF, Positions.FR),
    (Positions.UFL, Positions.FL),
    (Positions.ULB, Positions.BL),
    (Positions.UBR, Positions.BR),
)

# inverse une sequence en inversant l'ordre et chaque mouvement
def inverse_action(action):
    result = []
    for move in reversed(action):
        result.append(inverse_move(move))
    return tuple(result)

# Retrouve une piece et l'orientationde sa premiere couleur
def locate_piece(state, target):
    colors = SOLVED[target]

    for position, piece in enumerate(state):
        if set(piece) == set(colors):
            color_index = piece.index(colors[0])
            return position, color_index
    raise ValueError("Piece introuvable")

# retient la position et l'orientation des piece a suivre
def f2l_key(state, pairs):
    key = []
    for corner, edge in pairs:
        key.append(locate_piece(state, corner))
        key.append(locate_piece(state, edge))
    return tuple(key)

# Prepare les sequences qui preservent la croix
def f2l_actions():
    actions = [("D",), ("D'",), ("D2",)]

    for face in "RFLB":
        for opening in (face, face + "'"):
            closing = inverse_move(opening)
            for bottom in ("D", "D'", "D2"):
                actions.append((opening, bottom, closing))
    return tuple(actions)

@cache
# Calcul le trajet et l'orientation des pieces pour une sequence
def f2l_transitions(action):
    moved = list(SOLVED)
    for move in action:
        moved = apply_move(moved, move)
    transitions = {}

    for source, piece in enumerate(SOLVED):
        destination, _ = locate_piece(moved, source)

        for color_index, color in enumerate(piece):
            new_index = moved[destination].index(color)
            transitions[source, color_index] = (
                destination,
                new_index,
            )
    return transitions


# Verifie si un coin et son arete sont bien en place/orientées
def is_pair_solved(state, corner, edge):
    return (
        state[corner] == SOLVED[corner]
        and state[edge] == SOLVED[edge]
    )


#verifie la croix et les 4 paires de coins(arretes)
def is_f2l_solved(state):
    if not is_cross_solved(state):
        return False

    for corner, edge in F2L_PAIRS:
        if not is_pair_solved(state, corner, edge):
            return False
    return True

# Resout une paire en conservant la croix
# restaure aussi les paires indiques dans protected
def solve_pair(state, pair, protected=()):
    if not is_cross_solved(state):
        raise ValueError("Ls croix doit etre resolue")
    pairs = tuple(protected) + (pair,)
    start = f2l_key(state, pairs)
    goal = f2l_key(SOLVED, pairs)
    if start == goal:
        return []
    transitions = { action: f2l_transitions(action) for action in f2l_actions()}
    actions = bidirectional_search(start, goal, transitions, inverse_action)
    solution = []
    for action in actions:
        solution.extend(action)
    return solution

# Resout les 4 paires sans perdres les déjà faites
# Renvoie les mouvement sans modifier le cube de depart
def solve_f2l_order(state, order):
    current = list(state)
    solution = []
    protected = []

    for pair in order:
        moves = solve_pair(current, pair, protected)
        for move in moves:
            current = apply_move(current, move)
        solution.extend(moves)
        protected.append(pair)
    if not is_f2l_solved(current):
        raise ValueError("F2L non resolu")
    return solution

def solve_f2l(state):
    best = None

    for order in permutations(F2L_PAIRS):
        moves = solve_f2l_order(state, order)
        candidate = simplify_move(moves)

        if best is None or len(candidate) < len(best):
            best = candidate
    return best
