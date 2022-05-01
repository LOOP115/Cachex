from math import inf, tanh
from copy import deepcopy
from ELDEN_KING.utils import *


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
    res = len(my_max_path) - len(op_max_path) - my_win_cost + op_win_cost + len(my_cells) - len(op_cells)
    return res


# Mini Max with alpha-beta pruning
def minimax(player, board):
    # Filter out promising actions at current state
    actions = get_actions(board)
    if len(actions) == 1:
        return actions[0], inf
    good_actions = []
    for action in actions:
        score = evaluation(player, action, board)
        # print(f"# eval: {action}: {score}")
        if score == inf:
            return action, inf
        good_actions.append((action, score))
    # print()
    # Sort the promising actions based on their evaluation result
    # Choose the greatest half to perform mini-max search to reduce time complexity
    good_actions.sort(key=lambda x: x[1], reverse=True)
    good_actions = good_actions[:len(good_actions)//2]

    # Find the action with max utility value after looking several steps ahead
    value = -inf
    res = good_actions[0][0]
    for action in good_actions:
        move = action[0]
        temp = min_value(player, move, board, 0, -inf, inf)
        # print(f"# min value: {move}: {temp}")
        if temp > value:
            value = temp
            res = move
    return res, value


# Return the max value assuming opponent selected actions with min values
def max_value(player, action, board, depth, alpha, beta):
    # Max search depth reached, terminate
    if depth == MAX_DEPTH:
        return utility_value(player, opponent(player), action, board)

    # Opponent will win after this move, terminate
    value = utility_value(player, opponent(player), action, board)
    if value == -inf:
        return value

    # Clone the board after opponent's move and get available actions for me
    board_clone = deepcopy(board)
    board_clone.make_move(action, opponent(player))
    actions = get_actions(board_clone)

    # Search the max value for me
    for action in actions:
        alpha = max(alpha, min_value(player, action, board_clone, depth+1, alpha, beta))
        if alpha >= beta:
            return beta
    return alpha


# Return the min value assuming I selected actions with max values
def min_value(player, action, board, depth, alpha, beta):
    # Max search depth reached, terminate
    if depth == MAX_DEPTH:
        return utility_value(player, player, action, board)

    # I will win after this move, terminate
    value = utility_value(player, player, action, board)
    if value == inf:
        return value

    # Clone the board after my move and get available actions for opponent
    board_clone = deepcopy(board)
    board_clone.make_move(action, player)
    actions = get_actions(board_clone)

    # Search the min value for opponent
    for action in actions:
        beta = min(beta, max_value(player, action, board_clone, depth+1, alpha, beta))
        if beta <= alpha:
            return alpha
    return beta
