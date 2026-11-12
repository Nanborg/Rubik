from common.colors import Colors
from common.cube import Positions as pos

COLOR_VALUES = {
	Colors.WHITE: "#FFFFFF",
	Colors.YELLOW: "#F0CC00",
	Colors.GREEN: "#48B328",
	Colors.BLUE: "#3E3CB8",
	Colors.RED: "#C41616",
	Colors.ORANGE: "#D86800"
}

POLYGONS = [
	("#FFFFFF",	[(1.,1.,3.),	(-1.,1.,3.),	(-1.,-1.,3.),	(1.,-1.,3.)],	Colors.WHITE),
	("#F0CC00",	[(1.,1.,-3.),	(-1.,1.,-3.),	(-1.,-1.,-3.),	(1.,-1.,-3.)],	Colors.YELLOW),
	("#48B328",	[(3.,1.,1.),	(3.,-1.,1.),	(3.,-1.,-1.),	(3.,1.,-1.)],	Colors.GREEN),
	("#3E3CB8",	[(-3.,1.,1.),	(-3.,-1.,1.),	(-3.,-1.,-1.),	(-3.,1.,-1.)],	Colors.BLUE),
	("#C41616",	[(1.,3.,1.),	(-1.,3.,1.),	(-1.,3.,-1.),	(1.,3.,-1.)],	Colors.RED),
	("#D86800",	[(1.,-3.,1.),	(-1.,-3.,1.),	(-1.,-3.,-1.),	(1.,-3.,-1.)],	Colors.ORANGE),

	((pos.UFR, 0),	[(3.,3.,3.),	(1.,3.,3.),		(1.,1.,3.),		(3.,1.,3.)],	Colors.WHITE | Colors.GREEN | Colors.RED),
	((pos.UFL, 0),	[(1.,-1.,3.),	(3.,-1.,3.),	(3.,-3.,3.),	(1.,-3.,3.)],	Colors.WHITE | Colors.GREEN | Colors.ORANGE),
	((pos.UBR, 0),	[(-1.,3.,3.),	(-3.,3.,3.),	(-3.,1.,3.),	(-1.,1.,3.)],	Colors.WHITE | Colors.BLUE | Colors.RED),
	((pos.UBL, 0),	[(-1.,-1.,3.),	(-3.,-1.,3.),	(-3.,-3.,3.),	(-1.,-3.,3.)],	Colors.WHITE | Colors.BLUE | Colors.ORANGE),
	((pos.UF, 0),	[(3.,1.,3.),	(1.,1.,3.),		(1.,-1.,3.),	(3.,-1.,3.)],	Colors.WHITE | Colors.GREEN),
	((pos.UB, 0),	[(-1.,1.,3.),	(-3.,1.,3.),	(-3.,-1.,3.),	(-1.,-1.,3.)],	Colors.WHITE | Colors.BLUE),
	((pos.UR, 0),	[(1.,3.,3.),	(-1.,3.,3.),	(-1.,1.,3.),	(1.,1.,3.)],	Colors.WHITE | Colors.RED),
	((pos.UL, 0),	[(1.,-1.,3.),	(-1.,-1.,3.),	(-1.,-3.,3.),	(1.,-3.,3.)],	Colors.WHITE | Colors.ORANGE),

	((pos.DFR, 0),	[(3.,3.,-3.),	(1.,3.,-3.),	(1.,1.,-3.),	(3.,1.,-3.)],	Colors.YELLOW | Colors.GREEN | Colors.RED),
	((pos.DFL, 0),	[(1.,-1.,-3.),	(3.,-1.,-3.),	(3.,-3.,-3.),	(1.,-3.,-3.)],	Colors.YELLOW | Colors.GREEN | Colors.ORANGE),
	((pos.DBR, 0),	[(-1.,3.,-3.),	(-3.,3.,-3.),	(-3.,1.,-3.),	(-1.,1.,-3.)],	Colors.YELLOW | Colors.BLUE | Colors.RED),
	((pos.DBL, 0),	[(-1.,-1.,-3.),	(-3.,-1.,-3.),	(-3.,-3.,-3.),	(-1.,-3.,-3.)],	Colors.YELLOW | Colors.BLUE | Colors.ORANGE),
	((pos.DF, 0),	[(3.,1.,-3.),	(1.,1.,-3.),	(1.,-1.,-3.),	(3.,-1.,-3.)],	Colors.YELLOW | Colors.GREEN),
	((pos.DB, 0),	[(-1.,1.,-3.),	(-3.,1.,-3.),	(-3.,-1.,-3.),	(-1.,-1.,-3.)],	Colors.YELLOW | Colors.BLUE),
	((pos.DR, 0),	[(1.,3.,-3.),	(-1.,3.,-3.),	(-1.,1.,-3.),	(1.,1.,-3.)],	Colors.YELLOW | Colors.RED),
	((pos.DL, 0),	[(1.,-1.,-3.),	(-1.,-1.,-3.),	(-1.,-3.,-3.),	(1.,-3.,-3.)],	Colors.YELLOW | Colors.ORANGE),

	((pos.FUR, 2),	[(3.,3.,3.),	(3.,1.,3.),		(3.,1.,1.),		(3.,3.,1.)],	Colors.GREEN | Colors.WHITE | Colors.RED),
	((pos.FUL, 1),	[(3.,-1.,3.),	(3.,-3.,3.),	(3.,-3.,1.),	(3.,-1.,1.)],	Colors.GREEN | Colors.WHITE | Colors.ORANGE),
	((pos.FDL, 2),	[(3.,-1.,-1.),	(3.,-3.,-1.),	(3.,-3.,-3.),	(3.,-1.,-3.)],	Colors.GREEN | Colors.YELLOW | Colors.ORANGE),
	((pos.FDR, 1),	[(3.,3.,-1.),	(3.,1.,-1.),	(3.,1.,-3.),	(3.,3.,-3.)],	Colors.GREEN | Colors.YELLOW | Colors.RED),
	((pos.FU, 1),	[(3.,1.,3.),	(3.,-1.,3.),	(3.,-1.,1.),	(3.,1.,1.)],	Colors.GREEN | Colors.WHITE),
	((pos.FL, 0),	[(3.,-1.,1.),	(3.,-3.,1.),	(3.,-3.,-1.),	(3.,-1.,-1.)],	Colors.GREEN | Colors.ORANGE),
	((pos.FD, 1),	[(3.,1.,-1.),	(3.,-1.,-1.),	(3.,-1.,-3.),	(3.,1.,-3.)],	Colors.GREEN | Colors.YELLOW),
	((pos.FR, 1),	[(3.,3.,1.),	(3.,1.,1.),		(3.,1.,-1.),	(3.,3.,-1.)],	Colors.GREEN | Colors.RED),

	((pos.RUB, 2),	[(-3.,3.,3.),	(-1.,3.,3.),	(-1.,3.,1.),	(-3.,3.,1.)],	Colors.RED | Colors.WHITE | Colors.BLUE),
	((pos.RUF, 1),	[(1.,3.,3.),	(3.,3.,3.),		(3.,3.,1.),		(1.,3.,1.)],	Colors.RED | Colors.WHITE | Colors.GREEN),
	((pos.RDF, 2),	[(1.,3.,-1.),	(3.,3.,-1.),	(3.,3.,-3.),	(1.,3.,-3.)],	Colors.RED | Colors.YELLOW | Colors.GREEN),
	((pos.RDB, 1),	[(-3.,3.,-1.),	(-1.,3.,-1.),	(-1.,3.,-3.),	(-3.,3.,-3.)],	Colors.RED | Colors.YELLOW | Colors.BLUE),
	((pos.RU, 1),	[(-1.,3.,3.),	(1.,3.,3.),		(1.,3.,1.),		(-1.,3.,1.)],	Colors.RED | Colors.WHITE),
	((pos.RF, 0),	[(1.,3.,1.),	(3.,3.,1.),		(3.,3.,-1.),	(1.,3.,-1.)],	Colors.RED | Colors.GREEN),
	((pos.RD, 1),	[(-1.,3.,-1.),	(1.,3.,-1.),	(1.,3.,-3.),	(-1.,3.,-3.)],	Colors.RED | Colors.YELLOW),
	((pos.RB, 1),	[(-3.,3.,1.),	(-1.,3.,1.),	(-1.,3.,-1.),	(-3.,3.,-1.)],	Colors.RED | Colors.BLUE),

	((pos.BUL, 2),	[(-3.,-3.,3.),	(-3.,-1.,3.),	(-3.,-1.,1.),	(-3.,-3.,1.)],	Colors.BLUE | Colors.WHITE | Colors.ORANGE),
	((pos.BUR, 1),	[(-3.,1.,3.),	(-3.,3.,3.),	(-3.,3.,1.),	(-3.,1.,1.)],	Colors.BLUE | Colors.WHITE | Colors.RED),
	((pos.BDR, 2),	[(-3.,1.,-1.),	(-3.,3.,-1.),	(-3.,3.,-3.),	(-3.,1.,-3.)],	Colors.BLUE | Colors.YELLOW | Colors.RED),
	((pos.BDL, 1),	[(-3.,-3.,-1.),	(-3.,-1.,-1.),	(-3.,-1.,-3.),	(-3.,-3.,-3.)],	Colors.BLUE | Colors.YELLOW | Colors.ORANGE),
	((pos.BU, 1),	[(-3.,-1.,3.),	(-3.,1.,3.),	(-3.,1.,1.),	(-3.,-1.,1.)],	Colors.BLUE | Colors.WHITE),
	((pos.BR, 0),	[(-3.,1.,1.),	(-3.,3.,1.),	(-3.,3.,-1.),	(-3.,1.,-1.)],	Colors.BLUE | Colors.RED),
	((pos.BD, 1),	[(-3.,-1.,-1.),	(-3.,1.,-1.),	(-3.,1.,-3.),	(-3.,-1.,-3.)],	Colors.BLUE | Colors.YELLOW),
	((pos.BL, 1),	[(-3.,-3.,1.),	(-3.,-1.,1.),	(-3.,-1.,-1.),	(-3.,-3.,-1.)],	Colors.BLUE | Colors.ORANGE),

	((pos.LUF, 2),	[(3.,-3.,3.),	(1.,-3.,3.),	(1.,-3.,1.),	(3.,-3.,1.)],	Colors.ORANGE | Colors.WHITE | Colors.GREEN),
	((pos.LUB, 1),	[(-1.,-3.,3.),	(-3.,-3.,3.),	(-3.,-3.,1.),	(-1.,-3.,1.)],	Colors.ORANGE | Colors.WHITE | Colors.BLUE),
	((pos.LDB, 2),	[(-1.,-3.,-1.),	(-3.,-3.,-1.),	(-3.,-3.,-3.),	(-1.,-3.,-3.)],	Colors.ORANGE | Colors.YELLOW | Colors.BLUE),
	((pos.LDF, 1),	[(3.,-3.,-1.),	(1.,-3.,-1.),	(1.,-3.,-3.),	(3.,-3.,-3.)],	Colors.ORANGE | Colors.YELLOW | Colors.GREEN),
	((pos.LU, 1),	[(1.,-3.,3.),	(-1.,-3.,3.),	(-1.,-3.,1.),	(1.,-3.,1.)],	Colors.ORANGE | Colors.WHITE),
	((pos.LF, 1),	[(3.,-3.,1.),	(1.,-3.,1.),	(1.,-3.,-1.),	(3.,-3.,-1.)],	Colors.ORANGE | Colors.GREEN),
	((pos.LD, 1),	[(1.,-3.,-1.),	(-1.,-3.,-1.),	(-1.,-3.,-3.),	(1.,-3.,-3.)],	Colors.ORANGE | Colors.YELLOW),
	((pos.LB, 0),	[(-1.,-3.,1.),	(-3.,-3.,1.),	(-3.,-3.,-1.),	(-1.,-3.,-1.)],	Colors.ORANGE | Colors.BLUE),
]

DIRECTIONS = {
	Colors.WHITE:	(0., 0., 1.),
	Colors.YELLOW:	(0., 0., -1.),
	Colors.GREEN:	(1., 0., 0.),
	Colors.BLUE:	(-1., 0., 0.),
	Colors.RED:		(0., 1., 0.),
	Colors.ORANGE:	(0., -1., 0.),
}

ROTATIONS = {
	"": 90.,
	"2": 180.,
	"'": -90.,
}