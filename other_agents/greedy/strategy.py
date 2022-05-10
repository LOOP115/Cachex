from math import inf, tanh
from copy import deepcopy
from greedy.utils import *


MAX_DEPTH = 3


# Decide if this is a good move to search deeper
def evaluation(player, action, board):
    # My benefit if I make this action
    my_benefit = utility_value(player, player, action, board)

    # My benefit if opponent take this action
    op_benefit = utility_value(player, opponent(player), action, board)

    return my_benefit - op_benefit


# Evaluation function
def utility_value(player, curr_player, action, board):
    # Specify the color side
    my_cells, op_cells = split_board(curr_player, action, board)
    if player != curr_player:
        temp = my_cells
        my_cells = op_cells
        op_cells = temp

    # Extract max consecutive pieces for both sides
    my_max_path = max_path_length(my_cells, board)
    op_max_path = max_path_length(op_cells, board)

    # Check if one of the players can win
    n = board.size
    if is_win(player, n, my_max_path):
        return inf
    if is_win(opponent(player), n, op_max_path):
        return -inf

    # Search the optimal wining path for both sides
    my_win, my_path = min_win_cost(player, my_cells, op_cells, board)
    my_win_cost = best_goal(my_win, my_path)[1]
    op_win, op_path = min_win_cost(opponent(player), op_cells, my_cells, board)
    op_win_cost = best_goal(op_win, op_path)[1]

    # If the cost to win is none, set it to 2n as a huge contribution utility value
    if my_win_cost is None:
        my_win_cost = 2 * n
    if op_win_cost is None:
        op_win_cost = 2 * n

    # Compute utility value based on the following features
    res = len(my_max_path) - 2 * len(op_max_path) - my_win_cost + 2 * op_win_cost + len(my_cells) - 2 * len(op_cells)
    return res


# Greedy: Select most immediately promising action
def minimax(player, board):
    # Filter out promising actions at current state
    actions = get_actions(board)
    if len(actions) == 1:
        return actions[0]
    good_actions = []
    for action in actions:
        score = evaluation(player, action, board)
        # print(f"# eval: {action}: {score}")
        if score == inf:
            return action
        good_actions.append((action, score))
    # Sort the promising actions based on their evaluation result
    # Choose the greatest half to perform mini-max search to reduce time complexity
    good_actions.sort(key=lambda x: x[1], reverse=True)
    return good_actions[0][0]
