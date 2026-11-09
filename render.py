#!/usr/bin/python3

# TODO(nicolsan): lire l’état initial, les mouvements sur stdin et les options du rendu bonus.
import pygame
from common.colors import Colors, FACES
from common.cube import Positions as pos, apply_move, SOLVED
from math import cos, sin, pi
import sys
from copy import deepcopy

width, height = 1280, 720

pygame.init()
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
clock = pygame.time.Clock()

angle_h = 0.
angle_v = 0.


COLOR_VALUES = {
	Colors.WHITE: "#FFFFFF",
	Colors.YELLOW: "#F0CC00",
	Colors.GREEN: "#48B328",
	Colors.BLUE: "#3E3CB8",
	Colors.RED: "#C41616",
	Colors.ORANGE: "#D86800"
}

SCALE = 30.
ROTATION_SPEED = 5.
FOC_LENGTH = 20.

ANIMATION_SPEED = 30
ANIMATION_DELAY = 10

cur_animation = None

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

# still need to make the layering work properly before those
#	("black",		[(3.,3.,1.),	(3.,-3.,1.),	(-3.,-3.,1.),	(-3.,3.,1.)],	Colors.WHITE),
#	("black",		[(3.,3.,-1.),	(3.,-3.,-1.),	(-3.,-3.,-1.),	(-3.,3.,-1.)],	Colors.YELLOW),
#	("black",		[(1.,3.,3.),	(1.,-3.,3.),	(1.,-3.,-3.),	(1.,3.,3.)],	Colors.GREEN),
#	("black",		[(-1.,3.,3.),	(-1.,-3.,3.),	(-1.,-3.,-3.),	(-1.,3.,3.)],	Colors.BLUE),
#	("black",		[(3.,1.,3.),	(-3.,1.,3.),	(-3.,1.,-3.),	(-3.,1.,3.)],	Colors.RED),
#	("black",		[(3.,1.,3.),	(-3.,1.,3.),	(-3.,1.,-3.),	(-3.,1.,3.)],	Colors.ORANGE),
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

def transform_to_screen(point: tuple) -> tuple:
	return (-point[0] * SCALE + width/2., -point[1] * SCALE + height/2.)

def projection(point: tuple) -> tuple:
	pointv = pygame.Vector3(*point)
	perspective = FOC_LENGTH / (FOC_LENGTH - pointv * camera)
	h = (pointv * camera_h) * perspective
	v = (pointv * camera_v) * perspective
	return transform_to_screen((h,v))

def avg_dist(polygon: tuple) -> float:
	ret = 0.
	for point in polygon[1]:
		ret += (pygame.Vector3(*point) / FOC_LENGTH).distance_squared_to(camera)
	return ret / len(polygon[1])

def rotated_polygon(polygon: tuple, normal: tuple, angle: float):
	if (polygon[2] & cur_animation[0] == 0):
		return polygon

	new = deepcopy(polygon)
	for i in range(len(polygon[1])):
		new[1][i] = tuple(pygame.Vector3(*polygon[1][i]).rotate(angle, normal))
	return new

def draw_polygon(polygon: tuple, cube: list):
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

def draw_all_polygons(polygons: list, cube: list):
	polygons.sort(key=avg_dist, reverse=True)
	for p in polygons:
		draw_polygon(p, cube)

# TODO: move this somewhere esle
def is_valid_move(move: str) -> bool:
	mod = True if len(move) == 1 else move[1] in "'2"
	return move[0] in "UDFBRL" and mod

def rotate_all(polygons: list, face, angle: float):
	for i in range(len(polygons)):
		polygons[i] = rotated_polygon(POLYGONS[i], DIRECTIONS[cur_animation[0]], cur_animation[1])
	return polygons

def loop(cube: list, algo: list):
	global width, height, screen, clock, cur_animation

	polygons = deepcopy(POLYGONS)

	running = True
	was_pressed = False
	frame_counter = 0
	while (running):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.VIDEORESIZE:
				width, height = screen.get_width(), screen.get_height()

		screen.fill("gray")

		animation_time = frame_counter % (ANIMATION_SPEED + ANIMATION_DELAY)
		if (len(algo) > 0):
			if (animation_time == 0):
				cube = apply_move(cube, algo[0])
				cur_animation = [FACES[algo[0][0]], 0.]
			if (animation_time < ANIMATION_SPEED):
				cur_animation[1] = (1. - animation_time / ANIMATION_SPEED) * ROTATIONS[algo[0][1:]]
				rotate_all(polygons, *cur_animation)
			elif (animation_time == ANIMATION_SPEED):
				cur_animation = None
				algo.pop(0)
				polygons = deepcopy(POLYGONS)

		if (pygame.mouse.get_pressed()[0]):
			if (not was_pressed):
				pygame.mouse.get_rel()
			update_camera_angles()

		update_camera()

		draw_all_polygons(polygons, cube)

		was_pressed = pygame.mouse.get_pressed()[0]
		pygame.display.flip()
		clock.tick(60)
		frame_counter += 1

	pygame.quit()

no_input = False

def options(option: str):
	global no_input, ANIMATION_SPEED, ANIMATION_DELAY
	match (option[1]):
		case 'n':
			no_input = True
		case 's':
			ANIMATION_SPEED = float(option[3:])
		case 'd':
			ANIMATION_DELAY = float(option[3:])

if __name__=="__main__":
	algo = ""
	for i in range(1, len(sys.argv)):
		if (sys.argv[i][0] == '-'):
			options(sys.argv[i])
		else:
			algo = sys.argv[i]
	cube = SOLVED
	for move in algo.split():
		cube = apply_move(cube, move)
	moves = "" if (no_input) else sys.stdin.read()
	loop(cube, moves.split())
