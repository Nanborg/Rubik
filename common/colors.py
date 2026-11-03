# TODO(shared): définir les six couleurs avec une classe Enum.
from enum import Enum

class Colors(Enum):
	WHITE = 1	# UP
	YELLOW = 2	# DOWN
	GREEN = 4	# FRONT
	BLUE = 8	# BACK
	ORANGE = 16	# LEFT
	RED = 32	# RIGHT
