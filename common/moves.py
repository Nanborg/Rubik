# TODO(shared): parser et valider les 18 mouvements autorisés.

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
