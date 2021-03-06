
# Global variables
place = "PLACE"
steal = "STEAL"
red = "red"
blue = "blue"
my_flag = "m"
op_flag = "o"


# Format the action to valid command line inputs
def place_action(cell):
    return tuple([place, cell[0], cell[1]])


# Return the color of opponent
def opponent(player):
    oppo = red
    if player == red:
        oppo = blue
    return oppo


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


# Remove redundant captures
def unique_captures(captures):
    res = []
    for c in captures:
        res.append(c[0])
        res.append(c[1])
    return list(set(res))


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
    captures = board.can_capture(move, player)
    for c in unique_captures(captures):
        op_cells.remove(c)
    return my_cells, op_cells


# Compute max length of consecutive pieces
def max_path_length(my_cells, board):
    max_length = 0
    res = []
    clone = my_cells.copy()
    while len(clone) > 0:
        # Select a head to start
        queue = [clone.pop(0)]
        length = 0
        temp_list = []
        # Breath first search
        while len(queue) > 0:
            temp = queue.pop(0)
            length += 1
            temp_list.append(temp)
            neighbour_list = board.neighbours(temp)
            for n in neighbour_list:
                if n in clone:
                    clone.remove(n)
                    queue.append(n)

        if length > max_length:
            res = temp_list
            max_length = length
    return res


# Initialise cells left and right to the queue
def init_r_neighbours(mid, queue, board, bottom):
    # Decide the order to offer the queue
    if bottom:
        right = (mid[0], mid[1] + 1)
        if board.in_bounds(right):
            queue.append((right, 0))
        left = (mid[0], mid[1] - 1)
        if board.in_bounds(left):
            queue.append((left, 1))
    else:
        left = (mid[0], mid[1] - 1)
        if board.in_bounds(left):
            queue.append((left, 1))
        right = (mid[0], mid[1] + 1)
        if board.in_bounds(right):
            queue.append((right, 0))


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
    # Decide the order to offer the queue
    if left:
        top = (mid[0] + 1, mid[1])
        if board.in_bounds(top):
            queue.append((top, 0))
        bottom = (mid[0] - 1, mid[1])
        if board.in_bounds(bottom):
            queue.append((bottom, 1))
    else:
        bottom = (mid[0] - 1, mid[1])
        if board.in_bounds(bottom):
            queue.append((bottom, 1))
        top = (mid[0] + 1, mid[1])
        if board.in_bounds(top):
            queue.append((top, 0))


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


# Return the number of cells which is in the same line of the given cell
def num_one_line(player, cell, my_cells):
    i = 0
    if player == red:
        i = 1
    cnt = 0
    k = cell[i]
    for c in my_cells:
        if c[i] == k:
            cnt += 1
    return cnt


# Find optimal cells for start and goal to win
def start_goal(player, my_cells, op_cells, board):
    # Find cells which is nearest to the (red/blue) border
    if player == red:
        my_cells.sort()
    else:
        my_cells.sort(key=lambda l: l[1])

    x = board.size - 1
    heads = []
    tails = []
    # If the player hasn't occupied any cells, head and tail will be assumed as the center
    if len(my_cells) == 0:
        c = (x + 1) >> 1
        heads.append((c, c))
        tails.append((c, c))
    else:
        i = 1
        if player == "red":
            i = 0
        min_v = my_cells[0][i]
        max_v = my_cells[-1][i]
        for c in my_cells:
            if c[i] == min_v:
                heads.append(c)
            if c[i] == max_v:
                tails.append(c)

    start = heads[0]
    min_dis = 100
    max_line = 0
    for head in heads:
        # Red player, check bottom border
        if player == red:
            curr_line = num_one_line(player, head, my_cells)
            if curr_line < max_line:
                continue
            max_line = curr_line
            if head[0] == 0:
                start = head
            else:
                # Nearest start from head
                temp_start = (0, head[1])
                # Check if the start is occupied by opponent
                if temp_start in op_cells:
                    temp_start = find_r_border(temp_start, board, op_cells, bottom=True)
                if temp_start is None:
                    continue
                temp_dis = manhattan(head, temp_start)
                if temp_dis <= min_dis:
                    start = temp_start
                    min_dis = temp_dis

        # Blue player, check left border
        else:
            curr_line = num_one_line(player, head, my_cells)
            if curr_line < max_line:
                continue
            max_line = curr_line
            if head[1] == 0:
                start = head
            else:
                temp_start = (head[0], 0)
                if temp_start in op_cells:
                    temp_start = find_q_border(temp_start, board, op_cells, left=True)
                if temp_start is None:
                    continue
                temp_dis = manhattan(head, temp_start)
                if temp_dis <= min_dis:
                    start = temp_start
                    min_dis = temp_dis

    goal = tails[0]
    min_dis = 100
    max_line = 0
    for tail in tails:
        # Red player, check top border
        if player == red:
            curr_line = num_one_line(player, tail, my_cells)
            if curr_line < max_line:
                continue
            max_line = curr_line
            if tail[0] == x:
                goal = tail
            else:
                temp_goal = (x, tail[1])
                if temp_goal in op_cells:
                    temp_goal = find_r_border(temp_goal, board, op_cells, bottom=False)
                if temp_goal is None:
                    continue
                temp_dis = manhattan(tail, temp_goal)
                if temp_dis <= min_dis:
                    goal = temp_goal
                    min_dis = temp_dis

        # Blue player, check right border
        else:
            curr_line = num_one_line(player, tail, my_cells)
            if curr_line < max_line:
                continue
            max_line = curr_line
            if tail[1] == x:
                goal = tail
            else:
                temp_goal = (tail[0], x)
                if temp_goal in op_cells:
                    temp_goal = find_q_border(temp_goal, board, op_cells, left=False)
                if temp_goal is None:
                    continue
                temp_dis = manhattan(tail, temp_goal)
                if temp_dis <= min_dis:
                    goal = temp_goal
                    min_dis = temp_dis

    return start, goal


# Check if the cell can be the start state
def is_start(player, cell):
    if player == red:
        return cell[0] == 0
    return cell[1] == 0


# Check if the cell can be the goal state
def is_goal(player, cell, board):
    x = board.size - 1
    if player == red:
        return cell[0] == x
    return cell[1] == x


# Compute the lowest cost for the player to win at current state
def min_win_cost(player, my_cells, op_cells, board):
    # Find optimal positions for start and goal
    start, goal = start_goal(player, my_cells, op_cells, board)

    # Specify player color
    i = 1
    if player == red:
        i = 0

    # Use A* search to find the minimum cost from start to goal
    # Similar to Part A
    queue = [(start, 0)]
    # Keep records of explored cells
    # Format: {current cell: (last cell, f(x))}
    explored = {start: (None, 1)}
    if start in my_cells:
        explored = {start: (None, 0)}

    goals = []
    while len(queue) > 0:
        # Pop and expand the cell with lowest f(x)
        curr_cell = queue.pop(0)[0]
        neighbour_list = board.neighbours(curr_cell)
        for next_cell in neighbour_list:
            if next_cell in op_cells:
                continue

            start_flag = False
            # Update the cost to new cell, the cost is 0 if the cell is occupied by us
            new_cost = explored[curr_cell][1] + 1
            if next_cell in my_cells:
                # Find a piece on border, make it a new start state with cost = 0
                if next_cell != start and is_start(player, next_cell):
                    new_cost = 0
                    start_flag = True
                else:
                    new_cost -= 1
            else:
                # Find a cell on border, make it a new start state with cost = 1
                if is_start(player, next_cell):
                    start_flag = True
                    new_cost = 1

            # Goal test upon expansion
            if next_cell == goal:
                explored[next_cell] = (curr_cell, new_cost)
                goals.append(next_cell)
                return goals, explored

            # Check if the cell is worth to be expanded
            if next_cell not in explored.keys() or new_cost < explored[next_cell][1]:
                # If the cell can be a start state, record its predecessor as None
                if start_flag:
                    explored[next_cell] = (None, new_cost)
                else:
                    explored[next_cell] = (curr_cell, new_cost)

                # If the border is reached, record it to find the goal state with the least cost
                if is_goal(player, next_cell, board):
                    goals.append(next_cell)

                # Calculate f(x) of new cell and offer it to the queue
                queue.append((next_cell, new_cost + manhattan(next_cell, goal) - len(my_cells) + next_cell[i]))

        # Sort the queue based on f(x) after the cell is fully expanded
        queue.sort(key=lambda x: (x[1], x[0][i]))

    return goals, explored


# Find the goal state with the least cost
def best_goal(goals, explored):
    min_cost = 100
    # No available path
    if goals is None or len(goals) == 0:
        return None, None
    res = goals[0]
    for goal in goals:
        cost = explored[goal][1]
        if cost < min_cost:
            res = goal
            min_cost = cost
    return res, min_cost


# Print the path
def print_path(player, start, goal, explored):
    # No path found
    if start is None or goal is None:
        print("# No path found!")
        return

    # Backtrack the path
    result = []
    while True:
        result.append(goal)
        goal = explored[goal][0]
        if is_start(player, goal):
            break

    # Format the output
    result.append(goal)
    print(f"# {player} path:")
    for cell in result:
        print(f"# {cell}")


# Get all possible actions in current turn
def get_actions(board):
    n = board.size
    t = board.turn
    actions = []
    # In first turn, we can consider only half of the board due to symmetry
    if t == 1:
        # for i in range(n):
        #     for j in range(n - i):
        #         actions.append((i, j))
        # # Check center
        # c = n >> 1
        # cell = (c, c)
        # if not board.legal_first_move(cell):
        #     actions.remove(cell)
        # actions.append((0, n - 1))
        actions.append((0, n - 1))
        return actions
    # In second turn, decide if to steal

    # Normally, just extract the empty cells from board
    return board.empty_cells


# Check if the player can win
def is_win(player, size, max_path):
    if len(max_path) < size:
        return False
    if player == red:
        max_path.sort()
        return max_path[0][0] == 0 and max_path[-1][0] == size - 1
    else:
        max_path.sort(key=lambda l: l[1])
        return max_path[0][1] == 0 and max_path[-1][1] == size - 1
