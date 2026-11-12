from enum import IntEnum

class Colors(IntEnum):
	WHITE = 1	# UP
	YELLOW = 2	# DOWN
	GREEN = 4	# FRONT
	BLUE = 8	# BACK
	RED = 16	# RIGHT
	ORANGE = 32	# LEFT

COLOR_TEXT = {
	Colors.WHITE: "\033[38;5;255m",
	Colors.YELLOW: "\033[38;5;226m",
	Colors.GREEN: "\033[38;5;46m",
	Colors.BLUE: "\033[38;5;21m",
	Colors.RED: "\033[38;5;196m",
	Colors.ORANGE: "\033[38;5;208m"
	}

FACES = {
	"U": Colors.WHITE,
	"D": Colors.YELLOW,
	"F": Colors.GREEN,
	"B": Colors.BLUE,
	"R": Colors.RED,
	"L": Colors.ORANGE,
}
