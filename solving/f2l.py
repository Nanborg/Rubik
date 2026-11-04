# TODO(Neon): résoudre les quatre paires coin/arête sans casser la croix.

from common.cube import Positions
from common.moves import SOLVED, inverse_move
from solving.cross import is_cross_solved


F2L_PAIRS = (
    (Positions.URF, Positions.FR),
    (Positions.UFL, Positions.FL),
    (Positions.ULB, Positions.BL),
    (Positions.UBR, Positions.BR),
)

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
