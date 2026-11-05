# TODO(Neon): orienter la dernière couche sans casser F2L.

from common.colors import Colors
from common.cube import Positions, apply_move
from common.moves import SOLVED, inverse_move, simplify_move
from solving.f2l import is_f2l_solved

OLL_POSITIONS = (
    Positions.DF, Positions.DR,
    Positions.DB, Positions.DL,
    Positions.DFR, Positions.DLF,
    Positions.DBL, Positions.DRB,
)

#verifie F2l et les huit stickers jaunes
def is_oll_solved(state):
    if not is_f2l_solved(state):
        return False
    for position in OLL_POSITIONS:
        if state[position][0] != Colors.YELLOW:
            return False
    return True

def oll_key(state):
    key = []
    for position in OLL_POSITIONS:
        key.append(state[position].index(Colors.YELLOW))
    return tuple(key)

#construit le cas resolu par un algo
# verifie que la sequence preserve fF2L
def oll_case(algorithm):
    state = list(SOLVED)
    for move in reversed(algorithm):
        state = apply_move(state, inverse_move(move))
    if not is_f2l_solved(state):
        raise ValueError("F2L est cassé")
    return oll_key(state)


# Associe chaque cas OLL a sa sequence
# Garde la plus courte si plusieurs fonctionnent
def build_oll_table(algorithms):
    table = {oll_key(SOLVED): ()}

    for algorithm in algorithms:
        key = oll_case(algorithm)
        if key not in table or len(algorithm) < len(table[key]):
            table[key] = tuple(algorithm)
    return table

#Cherche le cas en essayant 4 orientations de D
# Renvoie la sequence la plus courte (preserve cube)
def solve_oll(state, table):
    if not is_f2l_solved(state):
        raise ValueError("F2L doit etre resolu")
    best = None
    for setup in ((), ("D",), ("D2",), ("D'",)):
        current = list(state)
        for move in setup:
            current = apply_move(current, move)
        algorithm = table.get(oll_key(current))
        if algorithm is None:
            continue
        moves = simplify_move(list(setup) + list(algorithm))
        if best is None or len(moves) < len(best):
            best = moves
    if best is None:
        raise ValueError("Cas OLL absent de la table")
    return best
