from common.moves import quarter_turns

DIRECTIONS = {
    "R": (1, 0, 0),
    "L": (-1, 0, 0),
    "U": (0, 1, 0),
    "D": (0, -1, 0),
    "F": (0, 0, 1),
    "B": (0, 0, -1),
}

# Recoit des coordonnees et l'axe de rotation
# Tourne d'un quart de tour horaire vu depuis l'exterieur
# Renvoie les nouvelle coordonnees
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

# Recoit un cube sous forme d'aretes et de coins
# Associe chaque couleur a une position et une direction
# Renvoie les 48 stickers sans les centres fixes
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

# Recoit les stickers et la face a tourner
# Tourne les positions et directions des stickers de cette face
# Renvoie de nouveaux stickers sans modifier ceux de depart
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


# Recoit les stickers et un mouvement valide
# Applique le nombre de quarts de tour demande
# Renvoie les stickers apres le mouvemnt
def reference_move(stickers, move):
    result = stickers.copy()

    for _ in range(quarter_turns(move)):
        result = rotate_layer(result, move[0])

    return result

