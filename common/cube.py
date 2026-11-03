# TODO(shared): appliquer les mouvements et vérifier si le cube est résolu.
from enum import IntEnum

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
