from math import inf
from copy import deepcopy
from agent.utils import *

MAX_DEPTH = 2

# Evaluation function
def utility_value(players, action, board):
    n = board.size
    my_cells, op_cells = split_board(players[0], action, board)
    my_max_path = max_path_length(my_cells, board)
    op_max_path = max_path_length(op_cells, board)

    my_win, my_path = min_win_cost(players[0], my_cells, op_cells, board)
    my_win_cost = best_goal(my_win, my_path)[1]

    op_win, op_path = min_win_cost(players[1], op_cells, my_cells, board)
    op_win_cost = best_goal(op_win, op_path)[1]

    # Max utility value if the action can lead to win
    if my_win_cost == 0 or my_win_cost == 1:
        return inf

    if my_win_cost is None:
        my_win_cost = n

    if op_win_cost is None:
        op_win_cost = n

    if op_win_cost == 0 or op_win_cost == 1:
        op_win_cost = 0.1

    res = my_max_path - op_max_path + (n / my_win_cost) - (n / op_win_cost)
    return res


# Mini Max with alpha-beta pruning
def minimax(player, board):
    players = []
    if player == "red":
        players.append("red")
        players.append("blue")
    else:
        players.append("blue")
        players.append("red")

    actions = get_actions(board)
    value = -inf
    res = actions[0]
    for action in actions:
        temp = max_value(players, action, board, 0, -inf, inf)
        if temp > value:
            value = temp
            res = action
    return res


def max_value(players, action, board, depth, alpha, beta):
    # Termination test
    if depth == MAX_DEPTH:
        return utility_value(players, action, board)

    value = utility_value(players, action, board)
    if value == inf:
        return value

    # Dive deeper
    value = -inf
    board_clone = deepcopy(board)
    board_clone.make_move(action, players[0])
    actions = get_actions(board_clone)

    for action in actions:
        # Ignore bad actions
        value = max(value, min_value(players, action, board_clone, depth+1, alpha, beta))
        if value >= beta:
            return value
        alpha = max(alpha, value)
    return value


def min_value(players, action, board, depth, alpha, beta):
    # Change side
    temp_players = [players[1], players[0]]

    # Termination test
    if depth == MAX_DEPTH:
        return utility_value(temp_players, action, board)

    value = utility_value(temp_players, action, board)
    if value == inf:
        return value

    # Dive deeper
    value = inf
    board_clone = deepcopy(board)
    board_clone.make_move(action, players[1])
    actions = get_actions(board_clone)

    for action in actions:
        value = min(value, max_value(players, action, board_clone, depth+1, alpha, beta))
        if value <= alpha:
            return value
        beta = min(beta, value)
    return value
