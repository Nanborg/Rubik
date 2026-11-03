# TODO(shared): appliquer les mouvements et vérifier si le cube est résolu.
from enum import IntEnum
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
