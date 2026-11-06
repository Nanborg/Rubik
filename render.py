# TODO(nicolsan): lire l’état initial, les mouvements sur stdin et les options du rendu bonus.
import pygame
from common.colors import Colors
from common.cube import Positions as pos, SOLVED

COLOR_VALUES = {
	Colors.WHITE: "#FFFFFF",
	Colors.YELLOW: "#F0CC00",
	Colors.GREEN: "#48B328",
	Colors.BLUE: "#3E3CB8",
	Colors.RED: "#C41616",
	Colors.ORANGE: "#D86800"
}

WIDTH = 1280
HEIGHT = 720
SCALE = 30.

def draw_sticker(surface: pygame.Surface, color: str, pos: list[tuple]):
	"""
	pos assumes a 6.0*6.0 cube centered at 0., 0., 0.
	"""
	pygame.draw.polygon(surface, pygame.Color(color), [(x*SCALE + WIDTH/2.,y*SCALE + HEIGHT/2.) for x,y,_ in pos])


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT), )
clock = pygame.time.Clock()
running = True
cube = SOLVED

DIRECTIONS = {
	"R": (1, 0, 0),
	"L": (-1, 0, 0),
	"U": (0, 1, 0),
	"D": (0, -1, 0),
	"F": (0, 0, 1),
	"B": (0, 0, -1),
}

PIECE_FACES = (
	"UF RF DF UR BR DR UB LB DB UL FL DL "
	"URF UFL UBR ULB DFR DLF DRB DBL"
).split()

def to_stickers(state):
	stickers = {}

	for faces, piece in zip(PIECE_FACES, state):
		position = tuple(
			sum(DIRECTIONS[face][axis] for face in faces)
			for axis in range(3)
		)

		for face, color in zip(faces, piece):
			direction = DIRECTIONS[face]
			stickers[position, direction] = color
	return stickers

print(to_stickers(SOLVED))


while running:
	# poll for events
	# pygame.QUIT event means the user clicked X to close your window
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	# fill the screen with a color to wipe away anything from last frame
	screen.fill("black")

	stickers = to_stickers(cube)

	for i in range(3*3*3):
		x,y,z = i%3, i//3%9, i//9
		if (x*y | y*z | z*x != 0):
			for i in range(3):
				print(stickers[(x,y,z), (x,y,z)])

	polygons = [
		(cube[pos.UFR][0],	[(3., 3., 3.),(3., 1., 3.),(1., 1., 3.),(1., 3., 3.)]),
		(cube[pos.UF][0],	[(3., 1., 3.),(1., 1., 3.),(1., -1., 3.),(3., -1., 3.)]),
		(cube[pos.UFL][0],	[(3., -1., 3.),(3., -3., 3.),(1., -3., 3.),(1., -1., 3.)]),
		]
	for c, p in polygons:
		draw_sticker(screen, COLOR_VALUES[c], p)

	# RENDER YOUR GAME HERE

	# flip() the display to put your work on screen
	pygame.display.flip()

	clock.tick(60)  # limits FPS to 60

pygame.quit()
