# Format the action
def place_action(cell):
    return tuple(["PLACE", cell[0], cell[1]])

# Compute manhattan distance of hexagonal grids
# Same as Part A
# https://stackoverflow.com/questions/5084801/manhattan-distance-between-tiles-in-a-hexagonal-grid
def manhattan(src, target):
    dx = target[0] - src[0]
    dy = target[1] - src[1]
    if (dx >= 0 and dy >= 0) or (dx < 0 and dy < 0):
        return abs(dx + dy)
    else:
        return max(abs(dx), abs(dy))
