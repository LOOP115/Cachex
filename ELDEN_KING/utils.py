# Format the action to valid command line inputs
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


# Split pieces into two lists after the player's move, one for player and the other for opponent
def split_board(player, move, board):
    my_cells = []
    op_cells = []
    for k, v in board.board_dict.items():
        if v == board.player_dict[player]:
            my_cells.append(k)
        else:
            op_cells.append(k)
    my_cells.append(move)

    # Check if my move will perform a capture
    capture = board.can_capture(move, player)
    if capture is not None:
        op_cells.remove(capture[0])
        op_cells.remove(capture[1])

    # my_cells.sort()
    # op_cells.sort()
    return my_cells, op_cells


# Compute max length of consecutive pieces
def max_path_length(my_cells, board):
    max_length = 0
    # Breath first search
    while len(my_cells) > 0:
        queue = [my_cells.pop(0)]
        length = 0
        while len(queue) > 0:
            temp = queue.pop(0)
            length += 1
            neighbours = board.neighbours(temp)
            for n in neighbours:
                if n in my_cells:
                    my_cells.remove(n)
                    queue.append(n)
        max_length = max(max_length, length)
    return max_length


# Initialise cells left and right to the queue
def init_r_neighbours(mid, queue, board, bottom):
    temp = []
    right = (mid[0], mid[1] + 1)
    if board.in_bounds(right):
        temp.append((right, 0))
    left = (mid[0], mid[1] - 1)
    if board.in_bounds(left):
        temp.append((left, 1))

    # Decide the order to offer the queue
    if bottom:
        queue.append(temp[0])
        queue.append(temp[1])
    else:
        queue.append(temp[1])
        queue.append(temp[0])


# Add cells left or right to the queue
def add_r_neighbours(src, queue, board):
    # 0 - right
    temp = src[0]
    if src[1] == 0:
        temp = (temp[0], temp[1] + 1)
    # 1 - left
    else:
        temp = (temp[0], temp[1] - 1)
    if board.in_bounds(temp):
        queue.append((temp, src[1]))


# Find the second-nearest start or goal position if opponent has occupied some cells on the border
def find_r_border(cell, board, op_cells, bottom):
    queue = []
    init_r_neighbours(cell, queue, board, bottom)
    while len(queue) > 0:
        temp = queue.pop(0)
        if temp[0] not in op_cells:
            return temp[0]
        else:
            add_r_neighbours(temp, queue, board)


# Initialise cells top and bottom to the queue
def init_q_neighbours(mid, queue, board, left):
    temp = []
    top = (mid[0] + 1, mid[1])
    if board.in_bounds(top):
        temp.append((top, 0))
    bottom = (mid[0] - 1, mid[1])
    if board.in_bounds(bottom):
        temp.append((bottom, 1))

    # Decide the order to offer the queue
    if left:
        queue.append(temp[0])
        queue.append(temp[1])
    else:
        queue.append(temp[1])
        queue.append(temp[0])


# Add cells top or bottom to the queue
def add_q_neighbours(src, queue, board):
    # 0 - top
    temp = src[0]
    if src[1] == 0:
        temp = (temp[0] + 1, temp[1])
    # 1 - bottom
    else:
        temp = (temp[0] - 1, temp[1])
    if board.in_bounds(temp):
        queue.append((temp, src[1]))


# Find the second-nearest start or goal position if opponent has occupied some cells on the border
def find_q_border(cell, board, op_cells, left):
    queue = []
    init_q_neighbours(cell, queue, board, left)
    while len(queue) > 0:
        temp = queue.pop(0)
        if temp[0] not in op_cells:
            return temp[0]
        else:
            add_q_neighbours(temp, queue, board)


# Find optimal cells for start and goal to win
def start_goal(player, my_cells, op_cells, board):
    # Find cells which is nearest to the (red/blue) border
    if player == "red":
        my_cells.sort()
    else:
        my_cells.sort(key=lambda l: l[1])

    # If the player hasn't occupied any cells, head and tail will be assumed as the center
    x = board.size - 1
    if len(my_cells) == 0:
        c = (x + 1) >> 1
        head = (c, c)
        tail = (c, c)
    else:
        head = my_cells[0]
        tail = my_cells[-1]

    start = head
    goal = tail
    # Red player, check top and bottom border
    if player == "red":
        # Confirm start position
        # Head is not on the border
        if head[0] != 0:
            # Nearest start from head
            start = (0, head[1])
            # Check if the start is occupied by opponent
            if start in op_cells:
                start = find_r_border(start, board, op_cells, bottom=True)

        # Find the nearest goal, same logic as finding the nearest start
        if tail[0] != x:
            goal = (x, tail[1])
            if goal in op_cells:
                goal = find_r_border(goal, board, op_cells, bottom=False)

    # Blue player, check left and right border
    # Same logic as red
    else:
        if head[1] != 0:
            start = (head[0], 0)
            if start in op_cells:
                start = find_q_border(start, board, op_cells, left=True)
        if tail[1] != x:
            goal = (tail[0], x)
            if goal in op_cells:
                goal = find_q_border(goal, board, op_cells, left=False)

    return start, goal

# Compute the lowest cost for the player to win at current state
# def min_win_cost(player, my_cells, op_cells, board):
#     # Decide optimal positions for start and goal
#
#     # Use A* search to find the minimum cost from start to goal
