# TODO(shared): parser et valider les 18 mouvements autorisés.
from common.colors import Colors

SOLVED = [
	# edges												# affected by:
	(Colors.WHITE,	Colors.GREEN	),					# F, U
	(Colors.RED,	Colors.GREEN	),					# F, R
	(Colors.YELLOW,	Colors.GREEN	),					# F, D
	(Colors.WHITE,	Colors.RED		),					# R, U
	(Colors.BLUE,	Colors.RED		),					# R, B
	(Colors.YELLOW,	Colors.RED		),					# R, D
	(Colors.WHITE,	Colors.BLUE		),					# B, U
	(Colors.ORANGE,	Colors.BLUE		),					# B, L
	(Colors.YELLOW,	Colors.BLUE		),					# B, D
	(Colors.WHITE,	Colors.ORANGE	),					# L, U
	(Colors.GREEN,	Colors.ORANGE	),					# L, F
	(Colors.YELLOW,	Colors.ORANGE	),					# L, D

	# corners											# affected by:
	(Colors.WHITE,	Colors.RED,		Colors.GREEN	),	# U, F, R
	(Colors.WHITE,	Colors.GREEN,	Colors.ORANGE	),	# U, F, L
	(Colors.WHITE,	Colors.BLUE,	Colors.RED		),	# U, B, R
	(Colors.WHITE,	Colors.ORANGE,	Colors.BLUE		),	# U, B, L
	(Colors.YELLOW,	Colors.GREEN,	Colors.RED		),	# D, F, R
	(Colors.YELLOW,	Colors.ORANGE,	Colors.GREEN	),	# D, F, L
	(Colors.YELLOW,	Colors.RED,		Colors.BLUE		),	# D, B, R
	(Colors.YELLOW,	Colors.BLUE,	Colors.ORANGE	)	# D, B, L
	]

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
