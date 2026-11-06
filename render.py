# TODO(nicolsan): lire l’état initial, les mouvements sur stdin et les options du rendu bonus.
import pygame
from common.colors import Colors
from common.cube import Positions as pos, SOLVED
from math import cos, sin

COLOR_VALUES = {
	Colors.WHITE: "#FFFFFF",
	Colors.YELLOW: "#F0CC00",
	Colors.GREEN: "#48B328",
	Colors.BLUE: "#3E3CB8",
	Colors.RED: "#C41616",
	Colors.ORANGE: "#D86800"
}

width, height = 1280, 720

pygame.init()
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True

angle_h = 0.
angle_v = 0.

SCALE = 30.
ROTATION_SPEED = 5.

was_pressed = False

cube = SOLVED

polygons = [
	("#FFFFFF",	[(1.,1.,3.),	(-1.,1.,3.),	(-1.,-1.,3.),	(1.,-1.,3.)]),
	("#F0CC00",	[(1.,1.,-3.),	(-1.,1.,-3.),	(-1.,-1.,-3.),	(1.,-1.,-3.)]),
	("#48B328",	[(3.,1.,1.),	(3.,-1.,1.),	(3.,-1.,-1.),	(3.,1.,-1.)]),
	("#3E3CB8",	[(-3.,1.,1.),	(-3.,-1.,1.),	(-3.,-1.,-1.),	(-3.,1.,-1.)]),
	("#C41616",	[(1.,3.,1.),	(-1.,3.,1.),	(-1.,3.,-1.),	(1.,3.,-1.)]),
	("#D86800",	[(1.,-3.,1.),	(-1.,-3.,1.),	(-1.,-3.,-1.),	(1.,-3.,-1.)]),

	((pos.UFR, 0),	[(3.,3.,3.),	(1.,3.,3.),		(1.,1.,3.),		(3.,1.,3.)]),
	((pos.UF, 0),	[(3.,1.,3.),	(1.,1.,3.),		(1.,-1.,3.),	(3.,-1.,3.)]),
	((pos.UFL, 0),	[(1.,-1.,3.),	(3.,-1.,3.),	(3.,-3.,3.),	(1.,-3.,3.)]),
	((pos.UR, 0),	[(1.,3.,3.),	(-1.,3.,3.),	(-1.,1.,3.),	(1.,1.,3.)]),
	((pos.UBR, 0),	[(-1.,3.,3.),	(-3.,3.,3.),	(-3.,1.,3.),	(-1.,1.,3.)]),
	((pos.UL, 0),	[(1.,-1.,3.),	(-1.,-1.,3.),	(-1.,-3.,3.),	(1.,-3.,3.)]),
	((pos.UBL, 0),	[(-1.,-1.,3.),	(-3.,-1.,3.),	(-3.,-3.,3.),	(-1.,-3.,3.)]),
	((pos.UB, 0),	[(-1.,1.,3.),	(-3.,1.,3.),	(-3.,-1.,3.),	(-1.,-1.,3.)]),

	((pos.DFR, 0),	[(3.,3.,-3.),	(1.,3.,-3.),	(1.,1.,-3.),	(3.,1.,-3.)]),
	((pos.DF, 0),	[(3.,1.,-3.),	(1.,1.,-3.),	(1.,-1.,-3.),	(3.,-1.,-3.)]),
	((pos.DFL, 0),	[(1.,-1.,-3.),	(3.,-1.,-3.),	(3.,-3.,-3.),	(1.,-3.,-3.)]),
	((pos.DR, 0),	[(1.,3.,-3.),	(-1.,3.,-3.),	(-1.,1.,-3.),	(1.,1.,-3.)]),
	((pos.DBR, 0),	[(-1.,3.,-3.),	(-3.,3.,-3.),	(-3.,1.,-3.),	(-1.,1.,-3.)]),
	((pos.DL, 0),	[(1.,-1.,-3.),	(-1.,-1.,-3.),	(-1.,-3.,-3.),	(1.,-3.,-3.)]),
	((pos.DBL, 0),	[(-1.,-1.,-3.),	(-3.,-1.,-3.),	(-3.,-3.,-3.),	(-1.,-3.,-3.)]),
	((pos.DB, 0),	[(-1.,1.,-3.),	(-3.,1.,-3.),	(-3.,-1.,-3.),	(-1.,-1.,-3.)]),

	((pos.FUR, 2),	[(3.,3.,3.),	(3.,1.,3.),		(3.,1.,1.),		(3.,3.,1.)]),
	((pos.FU, 1),	[(3.,1.,3.),	(3.,-1.,3.),	(3.,-1.,1.),	(3.,1.,1.)]),
	((pos.FUL, 1),	[(3.,-1.,3.),	(3.,-3.,3.),	(3.,-3.,1.),	(3.,-1.,1.)]),
	((pos.FL, 0),	[(3.,-1.,1.),	(3.,-3.,1.),	(3.,-3.,-1.),	(3.,-1.,-1.)]),
	((pos.FDL, 2),	[(3.,-1.,-1.),	(3.,-3.,-1.),	(3.,-3.,-3.),	(3.,-1.,-3.)]),
	((pos.FD, 1),	[(3.,1.,-1.),	(3.,-1.,-1.),	(3.,-1.,-3.),	(3.,1.,-3.)]),
	((pos.FDR, 1),	[(3.,3.,-1.),	(3.,1.,-1.),	(3.,1.,-3.),	(3.,3.,-3.)]),
	((pos.FR, 1),	[(3.,3.,1.),	(3.,1.,1.),		(3.,1.,-1.),	(3.,3.,-1.)]),

	((pos.RUB, 2),	[(-3.,3.,3.),	(-1.,3.,3.),	(-1.,3.,1.),	(-3.,3.,1.)]),
	((pos.RU, 1),	[(-1.,3.,3.),	(1.,3.,3.),		(1.,3.,1.),		(-1.,3.,1.)]),
	((pos.RUF, 1),	[(1.,3.,3.),	(3.,3.,3.),		(3.,3.,1.),		(1.,3.,1.)]),
	((pos.RF, 0),	[(1.,3.,1.),	(3.,3.,1.),		(3.,3.,-1.),	(1.,3.,-1.)]),
	((pos.RDF, 2),	[(1.,3.,-1.),	(3.,3.,-1.),	(3.,3.,-3.),	(1.,3.,-3.)]),
	((pos.RD, 1),	[(-1.,3.,-1.),	(1.,3.,-1.),	(1.,3.,-3.),	(-1.,3.,-3.)]),
	((pos.RDB, 1),	[(-3.,3.,-1.),	(-1.,3.,-1.),	(-1.,3.,-3.),	(-3.,3.,-3.)]),
	((pos.RB, 1),	[(-3.,3.,1.),	(-1.,3.,1.),	(-1.,3.,-1.),	(-3.,3.,-1.)]),

	((pos.BUL, 2),	[(-3.,-3.,3.),	(-3.,-1.,3.),	(-3.,-1.,1.),	(-3.,-3.,1.)]),
	((pos.BU, 1),	[(-3.,-1.,3.),	(-3.,1.,3.),	(-3.,1.,1.),	(-3.,-1.,1.)]),
	((pos.BUR, 1),	[(-3.,1.,3.),	(-3.,3.,3.),	(-3.,3.,1.),	(-3.,1.,1.)]),
	((pos.BR, 0),	[(-3.,1.,1.),	(-3.,3.,1.),	(-3.,3.,-1.),	(-3.,1.,-1.)]),
	((pos.BDR, 2),	[(-3.,1.,-1.),	(-3.,3.,-1.),	(-3.,3.,-3.),	(-3.,1.,-3.)]),
	((pos.BD, 1),	[(-3.,-1.,-1.),	(-3.,1.,-1.),	(-3.,1.,-3.),	(-3.,-1.,-3.)]),
	((pos.BDL, 1),	[(-3.,-3.,-1.),	(-3.,-1.,-1.),	(-3.,-1.,-3.),	(-3.,-3.,-3.)]),
	((pos.BL, 1),	[(-3.,-3.,1.),	(-3.,-1.,1.),	(-3.,-1.,-1.),	(-3.,-3.,-1.)]),

	((pos.LUF, 2),	[(3.,-3.,3.),	(1.,-3.,3.),	(1.,-3.,1.),	(3.,-3.,1.)]),
	((pos.LU, 1),	[(1.,-3.,3.),	(-1.,-3.,3.),	(-1.,-3.,1.),	(1.,-3.,1.)]),
	((pos.LUB, 1),	[(-1.,-3.,3.),	(-3.,-3.,3.),	(-3.,-3.,1.),	(-1.,-3.,1.)]),
	((pos.LB, 0),	[(-1.,-3.,1.),	(-3.,-3.,1.),	(-3.,-3.,-1.),	(-1.,-3.,-1.)]),
	((pos.LDB, 2),	[(-1.,-3.,-1.),	(-3.,-3.,-1.),	(-3.,-3.,-3.),	(-1.,-3.,-3.)]),
	((pos.LD, 1),	[(1.,-3.,-1.),	(-1.,-3.,-1.),	(-1.,-3.,-3.),	(1.,-3.,-3.)]),
	((pos.LDF, 1),	[(3.,-3.,-1.),	(1.,-3.,-1.),	(1.,-3.,-3.),	(3.,-3.,-3.)]),
	((pos.LF, 1),	[(3.,-3.,1.),	(1.,-3.,1.),	(1.,-3.,-1.),	(3.,-3.,-1.)]),
]

def transform_to_screen(point: tuple) -> tuple:
	return (-point[0] * SCALE + width/2., -point[1] * SCALE + height/2.)

def projection(point: tuple) -> tuple:
	pointv = pygame.Vector3(*point)
	h = (pointv * camera_h) / (10. - pointv * camera) * 10.
	v = (pointv * camera_v) / (10. - pointv * camera) * 10.
	return transform_to_screen((h,v))

def avg_dist(polygon: tuple) -> float:
	ret = 0.
	for point in polygon[1]:
		ret += pygame.Vector3(*point) * camera
	return ret / len(polygon[1])

def draw_polygon(polygon: tuple):
	if (isinstance(polygon[0], tuple)):
		piece, i = polygon[0]
		color = COLOR_VALUES[cube[piece][i]]
	else:
		color = polygon[0]
	pygame.draw.polygon(screen, color, list(map(projection, polygon[1])))
	pygame.draw.polygon(screen, "black", list(map(projection, polygon[1])), 5)

def update_camera_angles():
	global angle_h, angle_v

	mov_x, mov_y = pygame.mouse.get_rel()
	mov_x *= ROTATION_SPEED / min(width, height)
	mov_y *= ROTATION_SPEED / min(width, height)
	angle_h -= mov_x
	angle_v += mov_y

def update_camera():
	global camera_h, camera_v, camera

	sv, cv = sin(angle_v), cos(angle_v)
	camera_h = pygame.Vector3(sin(angle_h), -cos(angle_h), .0)
	camera_v = pygame.Vector3(camera_h[1] * sv, camera_h[0] * -sv, cv)
	camera = pygame.Vector3(-camera_h[1] * cv, camera_h[0] * cv, sv)

def draw_all_polygons(polygons: list):
	polygons.sort(key=avg_dist, reverse=False)
	for p in polygons:
		draw_polygon(p)

while (running):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.VIDEORESIZE:
			width, height = screen.get_width(), screen.get_height()

	screen.fill("gray")

	if (pygame.mouse.get_pressed()[0]):
		if (not was_pressed):
			pygame.mouse.get_rel()
		update_camera_angles()
		# update camera angles

	# update camera
	update_camera()

	# draw all polygons
	draw_all_polygons(polygons)

	was_pressed = pygame.mouse.get_pressed()[0]
	pygame.display.flip()
	clock.tick(60)

pygame.quit()
