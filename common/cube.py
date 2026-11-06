# TODO(shared): appliquer les mouvements et vérifier si le cube est résolu.
from enum import IntEnum
from common.colors import Colors, COLOR_TEXT
from common.moves import quarter_turns

class Positions(IntEnum):
	# edges
	FU = UF = 0
	FR = RF = 1
	FD = DF = 2
	RU = UR = 3
	RB = BR = 4
	RD = DR = 5
	BU = UB = 6
	BL = LB = 7
	BD = DB = 8
	LU = UL = 9
	LF = FL = 10
	LD = DL = 11

	# corners
	UFR = FRU = RUF = RFU = FUR = URF = 12
	UFL = FLU = LUF = LFU = FUL = ULF = 13
	UBR = BRU = RUB = RBU = BUR = URB = 14
	UBL = BLU = LUB = LBU = BUL = ULB = 15
	DFR = FRD = RDF = RFD = FDR = DRF = 16
	DFL = FLD = LDF = LFD = FDL = DLF = 17
	DBR = BRD = RDB = RBD = BDR = DRB = 18
	DBL = BLD = LDB = LBD = BDL = DLB = 19

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

def print_sticker(col: Colors) -> None:
	print(COLOR_TEXT[col] + "■ ", end="")

def print_pieces(cube: list[tuple], pieces: list[tuple]) -> None:
	for p, i in pieces:
		if (p < 0):
			print_sticker(i)
		else:
			print_sticker(cube[p][i])
	print("\033[0m")

def print_cube(cube: list[tuple]) -> None:
	"""
	prints colored cube faces on stdout
	"""

	pos = Positions # shorthand

	print("UP")
	print_pieces(cube, [(pos.UBL, 0), (pos.UB, 0), (pos.UBR, 0)])
	print_pieces(cube, [(pos.UL, 0), (-1, Colors.WHITE), (pos.UR, 0)])
	print_pieces(cube, [(pos.UFL, 0), (pos.UF, 0), (pos.UFR, 0)])

	print("DOWN")
	print_pieces(cube, [(pos.DFL, 0), (pos.DF, 0), (pos.DFR, 0)])
	print_pieces(cube, [(pos.DL, 0), (-1, Colors.YELLOW), (pos.DR, 0)])
	print_pieces(cube, [(pos.DBL, 0), (pos.DB, 0), (pos.DBR, 0)])

	print("FRONT")
	print_pieces(cube, [(pos.UFL, 1), (pos.UF, 1), (pos.UFR, 2)])
	print_pieces(cube, [(pos.FL, 0), (-1, Colors.GREEN), (pos.FR, 1)])
	print_pieces(cube, [(pos.DFL, 2), (pos.DF, 1), (pos.DFR, 1)])

	print("BACK")
	print_pieces(cube, [(pos.UBL, 2), (pos.UB, 1), (pos.UBR, 1)])
	print_pieces(cube, [(pos.BL, 1), (-1, Colors.BLUE), (pos.BR, 0)])
	print_pieces(cube, [(pos.DBL, 1), (pos.DB, 1), (pos.DBR, 2)])

	print("RIGHT")
	print_pieces(cube, [(pos.URF, 1), (pos.UR, 1), (pos.URB, 2)])
	print_pieces(cube, [(pos.RF, 0), (-1, Colors.RED), (pos.RB, 1)])
	print_pieces(cube, [(pos.DRF, 2), (pos.DR, 1), (pos.DRB, 1)])

	print("LEFT")
	print_pieces(cube, [(pos.ULB, 1), (pos.UL, 1), (pos.ULF, 2)])
	print_pieces(cube, [(pos.LB, 0), (-1, Colors.ORANGE), (pos.LF, 1)])
	print_pieces(cube, [(pos.DLB, 2), (pos.DL, 1), (pos.DLF, 1)])

FACE_CYCLES = {
	"U": (
	 (Positions.UF, Positions.UR, Positions.UB, Positions.UL),
	 (Positions.URF, Positions.UBR, Positions.ULB, Positions.UFL)
	),
	"D": (
	 (Positions.DF, Positions.DL, Positions.DB, Positions.DR),
	 (Positions.DFR, Positions.DLF, Positions.DBL, Positions.DRB)
	),
    "L": (
        (Positions.UL, Positions.BL, Positions.DL, Positions.FL),
        (Positions.UFL, Positions.ULB, Positions.DBL, Positions.DLF),
    ),
    "R": (
        (Positions.UR, Positions.FR, Positions.DR, Positions.BR),
        (Positions.URF, Positions.DFR, Positions.DRB, Positions.UBR),
    ),
    "F": (
        (Positions.UF, Positions.FL, Positions.DF, Positions.FR),
        (Positions.URF, Positions.UFL, Positions.DLF, Positions.DFR),
    ),
    "B": (
        (Positions.UB, Positions.BR, Positions.DB, Positions.BL),
        (Positions.UBR, Positions.DRB, Positions.DBL, Positions.ULB),
    ),
}

POSITION_FACE = (
	"UF", "RF", "DF",
	"UR", "BR", "DR",
	"UB", "LB", "DB",
	"UL", "FL", "DL",
	"URF", "UFL", "UBR", "ULB",
	"DFR", "DLF", "DRB", "DBL",
)

FACE_NEIGHBORS = {
	"U": "FLBR",
	"D": "FRBL",
	"L": "UFDB",
	"R": "UBDF",
	"F": "URDL",
	"B": "ULDR",
}

# Recoit une piece, sa position de depart et sa position d'arrivee
# Calcule ou regardent ses couleurs apres un quart de tour
# Renvoie les couleurs dans l'ordre de la position d'arrivee
# Ne modifie pas la piece de depart
def rotate_piece(piece, source, destination, face):
	neighbors = FACE_NEIGHBORS[face]
	face_map = dict(zip(neighbors, neighbors[1:] + neighbors[:1]))
	face_map[face] = face
	color_by_face = {}

	for direction, color in zip(POSITION_FACE[source], piece):
		new_direction = face_map[direction]
		color_by_face[new_direction] = color

	return tuple(
		color_by_face[direction]
		for direction in POSITION_FACE[destination]
	)

# Recoit le cube et un mouvment valide
# Deplace les pieces et reoriente leurs couleurs
# Renvoie un nouveau cube
# Ne modifi pas le cube de depart
def apply_move(state, move):
	face = move[0]
	turns = quarter_turns(move)

	if face not in FACE_CYCLES:
		raise NotImplementedError(f"Rotation pas implémentée : {face}")
	result = list(state)

	for _ in range(turns):
		previous = list(result)

		for positions in FACE_CYCLES[face]:
			for index, destination in enumerate(positions):
				source = positions[(index + 1) % len(positions)]

				result[destination] = rotate_piece(
					previous[source],
					source,
					destination,
					face,
				)
	return result

def apply_moves(state, moves):
	result = list(state)
	for move in moves:
		result = apply_move(result, move)
	return result
