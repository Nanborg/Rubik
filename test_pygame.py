import pygame
from math import cos, sin

WIDTH, HEIGHT = 1280, 720

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

angle_h = 0.
angle_v = 0.

polygons = [
	("#FFFFFF", [(1.,1.,1.),(-1.,1.,1.),(-1.,-1.,1.),(1.,-1.,1.)]),
	("#F0CC00", [(1.,1.,-1.),(-1.,1.,-1.),(-1.,-1.,-1.),(1.,-1.,-1.)]),
	("#48B328", [(1.,1.,1.),(1.,-1.,1.),(1.,-1.,-1.),(1.,1.,-1.)]),
	("#3E3CB8", [(-1.,1.,1.),(-1.,-1.,1.),(-1.,-1.,-1.),(-1.,1.,-1.)]),
	("#C41616", [(1.,1.,1.),(-1.,1.,1.),(-1.,1.,-1.),(1.,1.,-1.)]),
	("#D86800", [(1.,-1.,1.),(-1.,-1.,1.),(-1.,-1.,-1.),(1.,-1.,-1.)]),
]

scale = 100.
rotation_speed = 10.

def transform_to_screen(point: tuple) -> tuple:
	return (-point[0] * scale + WIDTH/2., -point[1] * scale + HEIGHT/2.)

def projection(point: tuple) -> tuple:
	pointv = pygame.Vector3(*point)
	h = pointv.dot(camera_h)
	v = pointv.dot(camera_v)
	return transform_to_screen((h,v))

def avg_dist(polygon: tuple) -> float:
	ret = 0.
	for point in polygon[1]:
		ret += pygame.Vector3(*point) * camera
	return ret / len(polygon[1])

def draw_polygon(polygon: tuple):
		pygame.draw.polygon(screen, polygon[0], list(map(projection, polygon[1])))

was_pressed = False

while (running):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	screen.fill("black")

	if (pygame.mouse.get_pressed()[0]):
		if (not was_pressed):
			pygame.mouse.get_rel()
		mov_x, mov_y = pygame.mouse.get_rel()
		mov_x /= min(WIDTH, HEIGHT)
		mov_y /= min(WIDTH, HEIGHT)
		angle_h -= mov_x * rotation_speed
		angle_v += mov_y * rotation_speed

	camera_h = pygame.Vector3(sin(angle_h), -cos(angle_h), .0)
	camera_v = pygame.Vector3(-camera_h[1] * -sin(angle_v), camera_h[0] * -sin(angle_v), cos(angle_v))
	camera = pygame.Vector3(-camera_h[1] * cos(angle_v), camera_h[0] * cos(angle_v), sin(angle_v))

	polygons.sort(key=avg_dist, reverse=False)
	for p in polygons:
		draw_polygon(p)

	was_pressed = pygame.mouse.get_pressed()[0]
	pygame.display.flip()
	clock.tick(60)

pygame.quit()
