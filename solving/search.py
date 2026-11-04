
# Explore un lvl de recherche
# renvoie la prochaine frontiere et un point de rencontre
def expand_layer(frontier, paths, other_paths, transitions):
    next_frontier = []

    for current in frontier:
        for move, table in transitions.items():
            key = tuple(table[edge] for edge in current)
            if key in paths:
                continue
            paths[key] = paths[current] + [move]

            if key in other_paths:
                return next_frontier, key
            next_frontier.append(key)
    return next_frontier, None

# Cherche un chemin depuis le depart et depuis le debut
def bidirectional_search(start, goal, transitions, inverse_action):
    if start == goal:
        return []
    forward = [start]
    backward = [goal]

    forward_paths = {start: []}
    backward_paths = {goal: []}

    while forward and backward:
        if len(forward) <= len (backward):
            forward, meeting = expand_layer(
                forward, forward_paths, backward_paths, transitions
            )
        else:
            backward, meeting = expand_layer(
                backward, backward_paths, forward_paths, transitions
            )
        if meeting is not None:
            end_path = [
                inverse_action(move)
                for move in reversed(backward_paths[meeting])
            ]
            return forward_paths[meeting] + end_path
    raise ValueError("Aucun chemin trouve")
