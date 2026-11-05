# TODO(shared): appliquer les mouvements et vérifier si le cube est résolu.
from enum import IntEnum
from common.colors import Colors, COLOR_TEXT

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
