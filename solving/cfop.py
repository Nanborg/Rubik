from itertools import permutations

from common.cube import SOLVED, apply_moves
from common.moves import simplify_move
from solving.cross import solve_cross
from solving.f2l import F2L_PAIRS, solve_f2l_order
from solving.oll import solve_oll
from solving.pll import solve_pll


# Compare les solutions completes pour les 24 ordres F2L
# Departage les egalites avec les mouvements F2L simplifies
def solve(moves, with_steps=False):
    state = apply_moves(SOLVED, moves)
    if state == SOLVED:
        if with_steps:
            return [], (("Croix", []), ("F2L", []), ("OLL", []), ("PLL", []))
        return []
    cross = solve_cross(state)
    after_cross = apply_moves(state, cross)
    best = None
    best_steps = None
    best_score = None
    for order in permutations(F2L_PAIRS):
        f2l = simplify_move(solve_f2l_order(after_cross, order))
        current = apply_moves(after_cross, f2l)
        oll = solve_oll(current)
        current = apply_moves(current, oll)
        pll = solve_pll(current)
        solution = simplify_move(cross + f2l + oll + pll)
        score = (len(solution), len(f2l))
        if best_score is None or score < best_score:
            best = solution
            best_score = score
            best_steps = (("Croix", cross), ("F2L", simplify_move(f2l)), ("OLL", oll), ("PLL", pll))
    if with_steps:
        return best, best_steps
    return best
