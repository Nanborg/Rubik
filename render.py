#!/opt/pyenv/shims/python3

from os import environ # hide pygame community message
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame
from common.colors import FACES
from common.cube import Positions as pos, apply_move, SOLVED
from rendering.mapping import *
from math import cos, sin
import sys
from copy import deepcopy

width, height = 1280, 720

angle_h = 0.
angle_v = 0.

SCALE = 30.
ROTATION_SPEED = 5.
FOC_LENGTH = 20.

ANIMATION_SPEED = 30
ANIMATION_DELAY = 10

cur_animation = None

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

def rotate_all(polygons: list, face, angle: float):
	for i in range(len(polygons)):
		polygons[i] = rotated_polygon(POLYGONS[i], DIRECTIONS[cur_animation[0]], cur_animation[1])
	return polygons

def loop(cube: list, algo: list):
	global width, height, screen, clock, cur_animation

	polygons = deepcopy(POLYGONS)

	running = True
	was_pressed = False
	frame_counter = -60
	while (running):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.VIDEORESIZE:
				width, height = screen.get_width(), screen.get_height()

		screen.fill("gray")

		animation_time = frame_counter % (ANIMATION_SPEED + ANIMATION_DELAY)
		if (len(algo) > 0 and frame_counter >= 0):
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

def print_help():
	print(
		f"{sys.argv[0]}, a utility to display a 3x3x3 rubik's cube and algorithms\n" \
		f"usage: {sys.argv[0]} [options -(n|s|d|h)] <scramble>\n" \
		"options:\n" \
		"	-n	no input, doesn't try to read an algorithm on stdin\n" \
		"	-s=N	speed, sets animation speed to specified amount of frames\n" \
		"	-d=N	delay, sets the delay between moves to specified amount of frames\n" \
		"	-h	help, displays this message\n"
	)
	exit(1)

def options(option: str):
	global no_input, ANIMATION_SPEED, ANIMATION_DELAY
	match (option[1]):
		case 'n':
			no_input = True
		case 's':
			ANIMATION_SPEED = float(option[3:])
		case 'd':
			ANIMATION_DELAY = float(option[3:])
		case 'h':
			print_help()

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

	pygame.init()
	screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
	clock = pygame.time.Clock()

	loop(cube, moves.split())
