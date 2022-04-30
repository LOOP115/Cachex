from math import inf
from copy import deepcopy
from ELDEN_KING.utils import *

MAX_DEPTH = 4

# Evaluation function
def utility_value(player, action, board):
    n = board.size
    my_cells, op_cells = split_board(player, action, board)
    my_max_path = max_path_length(my_cells, board)
    op_max_path = max_path_length(op_cells, board)

    if is_win(player, n, my_max_path, my_cells):
        return inf

    if is_win(opponent(player), n, op_max_path, op_cells):
        return -inf

    my_win, my_path = min_win_cost(player, my_cells, op_cells, board)
    my_win_cost = best_goal(my_win, my_path)[1]

    op_win, op_path = min_win_cost(player, op_cells, my_cells, board)
    op_win_cost = best_goal(op_win, op_path)[1]

    # Max utility value if the action can lead to win
    if my_win_cost == 0:
        my_win_cost = 0.1

    if my_win_cost is None:
        my_win_cost = n

    if op_win_cost is None:
        op_win_cost = n

    if op_win_cost == 0:
        op_win_cost = 0.1

    res = my_max_path - op_max_path + 2 * (n / my_win_cost) - 2 * (n / op_win_cost) + len(my_cells) - len(op_cells)
    return res


# Mini Max with alpha-beta pruning
def minimax(player, board):
    # Find the action with the max value
    actions = get_actions(board)
    value = -inf
    res = actions[0]
    for action in actions:
        temp = max_value(player, action, board, 0, -inf, inf)
        if temp == inf:
            return action, inf
        if temp > value:
            value = temp
            res = action
    return res, value


def max_value(player, action, board, depth, alpha, beta):
    # Termination test
    if depth == MAX_DEPTH:
        return utility_value(player, action, board)

    value = utility_value(player, action, board)
    if value == inf:
        return inf

    # Dive deeper
    value = -inf
    board_clone = deepcopy(board)
    board_clone.make_move(action, player)
    actions = get_actions(board_clone)

    for action in actions:
        alpha = max(alpha, min_value(player, action, board_clone, depth+1, alpha, beta))
        if alpha >= beta:
            return beta
    return alpha


def min_value(player, action, board, depth, alpha, beta):
    # Termination test
    if depth == MAX_DEPTH:
        return utility_value(player, action, board)

    value = utility_value(player, action, board)
    if value == -inf:
        return value

    # Dive deeper
    value = inf
    board_clone = deepcopy(board)
    board_clone.make_move(action, opponent(player))
    actions = get_actions(board_clone)

    for action in actions:
        beta = min(beta, max_value(player, action, board_clone, depth+1, alpha, beta))
        if beta <= alpha:
            return alpha
    return beta
