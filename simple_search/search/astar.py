from search.priority_queue import *


# Compute manhattan distance of hexagonal grids
# https://stackoverflow.com/questions/5084801/manhattan-distance-between-tiles-in-a-hexagonal-grid
def manhattan(start, goal):
    dx = goal[0] - start[0]
    dy = goal[1] - start[1]
    if (dx >= 0 and dy >= 0) or (dx < 0 and dy < 0):
        return abs(dx + dy)
    else:
        return max(abs(dx), abs(dy))


# Find cells 1 unit from the current cell
def neighbors(board, curr_cell):
    x = curr_cell[0]
    y = curr_cell[1]
    neighbor_list = []
    # Expansion matrix
    dx = [1, 1, 0, 0, -1, -1]
    dy = [-1, 0, -1, 1, 0, 1]
    # Check if neighbour cells are in bounds and not occupied
    for i in range(6):
        cell = (x + dx[i], y + dy[i])
        if board.in_bounds(cell) and board.is_occupied(cell):
            neighbor_list.append(cell)
    return neighbor_list


# Use A* to search the path
# https://www.redblobgames.com/pathfinding/a-star/implementation.html
def find_path(board):
    # Use priority queue to help get the cell with the lowest f(x) while expansion
    queue = PriorityQueue()
    queue.push((board.start[0], board.start[1]), 0)

    # Keep records of explored cells
    # Format: {current cell: (last cell, f(x))}
    explored = {(board.start[0], board.start[1]): (None, 0)}

    while not queue.empty():
        # Pop and expand the cell with lowest f(x)
        curr_cell = queue.pop()
        for next_cell in neighbors(board, curr_cell):
            new_cost = explored[curr_cell][1] + 1
            # Goal test upon expansion
            if next_cell == board.goal:
                explored[next_cell] = (curr_cell, new_cost)
                return explored
            # Calculate f(x) of new cell and push it to the priority queue
            if next_cell not in explored.keys() or new_cost < explored[next_cell][1]:
                explored[next_cell] = (curr_cell, new_cost)
                queue.push(next_cell, new_cost + manhattan(next_cell, board.goal))
    return explored


# Format and print the result
def print_path(board, explored):
    cell = board.goal
    # No path found
    if list(explored.keys())[-1] != cell:
        print(0)
        return

    result = []
    # Backtrack the path
    while True:
        result.append(cell)
        cell = explored[cell][0]
        if cell == board.start:
            break
        board.board_dict[cell] = "p"

    # Format the output
    result.append(board.start)
    result.reverse()
    print(len(result))
    for cell in result:
        print(f'({cell[0]},{cell[1]})')


# Print search history
def search_history(explored):
    print("\nSearch history: ")
    for key in explored.keys():
        print(f'Current cell: {key} | Last cell: {explored[key][0]} | f(x) = {explored[key][1]}')
