from common.moves import quarter_turns

DIRECTIONS = {
    "R": (1, 0, 0),
    "L": (-1, 0, 0),
    "U": (0, 1, 0),
    "D": (0, -1, 0),
    "F": (0, 0, 1),
    "B": (0, 0, -1),
}

def rotate_vector(vector, axis):
    x, y, z = vector
    a, b, c = axis

    projection = a * x + b * y + c * z

    return (
        a * projection - (b * z - c * y),
        b * projection - (c * x - a * z),
        c * projection - (a * y - b * x),
    )

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

def rotate_layer(stickers, face):
    axis = DIRECTIONS[face]
    result = {}

    for (position, direction), color in stickers.items():
        layer = sum(p * a for p, a in zip(position, axis))

        if layer == 1:
            position = rotate_vector(position, axis)
            direction = rotate_vector(direction, axis)

        result[position, direction] = color

    return result


def reference_move(stickers, move):
    result = stickers.copy()

    for _ in range(quarter_turns(move)):
        result = rotate_layer(result, move[0])

    return result

