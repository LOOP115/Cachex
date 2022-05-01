from math import inf, tanh
from copy import deepcopy
from ELDEN_KING.utils import *

MAX_DEPTH = 4

# Decide if this is a good move to search deeper
def evaluation(player, action, board):
    # My benefit if I make this action
    my_benefit = utility_value(player, player, action, board)
    # # I can win by taking this action
    # if my_benefit == inf:
    #     return inf

    # My benefit if opponent take this action
    op_benefit = utility_value(player, opponent(player), action, board)
    # # Opponent wins by taking action
    # if op_benefit == -inf:
    #     return inf

    return my_benefit - op_benefit


# Evaluation function
def utility_value(player, curr_player, action, board):
    n = board.size
    # If I take this step
    my_cells, op_cells = split_board(curr_player, action, board)
    if player != curr_player:
        temp = my_cells
        my_cells = op_cells
        op_cells = temp

    my_max_path = max_path_length(my_cells, board)
    op_max_path = max_path_length(op_cells, board)

    if is_win(player, n, my_max_path):
        return inf

    if is_win(opponent(player), n, op_max_path):
        return -inf

    my_win, my_path = min_win_cost(player, my_cells, op_cells, board)
    my_win_cost = best_goal(my_win, my_path)[1]

    op_win, op_path = min_win_cost(opponent(player), op_cells, my_cells, board)
    op_win_cost = best_goal(op_win, op_path)[1]

    # Max utility value if the action can lead to win
    # if my_win_cost == 0:
    #     my_win_cost = 0.1

    if my_win_cost is None:
        my_win_cost = 2 * n

    if op_win_cost is None:
        op_win_cost = 2 * n

    # if op_win_cost == 0:
    #     op_win_cost = 0.1

    # res = my_max_path - op_max_path + 2 * (n / my_win_cost) - 2 * (n / op_win_cost) + len(my_cells) - len(op_cells)
    # res = 0 - my_win_cost
    res = 2 * len(my_max_path) - 2 * len(op_max_path) - my_win_cost + op_win_cost + len(my_cells) - len(op_cells)
    return res


# Mini Max with alpha-beta pruning
def minimax(player, board):
    # Filter out important actions at current state
    actions = get_actions(board)
    if len(actions) == 1:
        return actions[0], inf
    good_actions = []
    for action in actions:
        score = evaluation(player, action, board)
        print(f"# eval: {action}: {score}")
        if score == inf:
            return action, inf
        good_actions.append((action, score))
    print()
    good_actions.sort(key=lambda x: x[1], reverse=True)
    good_actions = good_actions[:len(good_actions)//2]
    # Find the action with the max value
    value = -inf
    res = good_actions[0]
    for action in good_actions:
        move = action[0]
        temp = max_value(player, move, board, 0, -inf, inf)
        print(f"# max: {move}: {temp}")
        if temp > value:
            value = temp
            res = move
    return res, value


def max_value(player, action, board, depth, alpha, beta):
    # Termination test
    if depth == MAX_DEPTH:
        return utility_value(player, player, action, board)

    value = utility_value(player, player, action, board)
    if value == -inf or value == inf:
        return value

    # I make this move
    board_clone = deepcopy(board)
    board_clone.make_move(action, player)
    actions = get_actions(board_clone)

    # Good next actions for opponent
    # good_actions = []
    # for action in actions:
    #     score = evaluation(player, action, board)
    #     if score == inf:
    #         return inf
    #     good_actions.append((action, score))
    #
    # good_actions.sort(key=lambda x: x[1])
    # good_actions = good_actions[:len(good_actions) // 2]

    for action in actions:
        alpha = max(alpha, min_value(player, action, board_clone, depth+1, alpha, beta))
        if alpha >= beta:
            return beta
    return alpha


def min_value(player, action, board, depth, alpha, beta):
    # Termination test
    if depth == MAX_DEPTH:
        return utility_value(player, opponent(player), action, board)

    value = utility_value(player, opponent(player), action, board)
    if value == -inf or value == inf:
        return value

    # Opponent make this move
    board_clone = deepcopy(board)
    board_clone.make_move(action, opponent(player))
    actions = get_actions(board_clone)

    # Good next actions for me
    good_actions = []
    # for action in actions:
    #     score = evaluation(player, action, board)
    #     if score == inf:
    #         return inf
    #     good_actions.append((action, score))
    #
    # good_actions.sort(key=lambda x: x[1], reverse=True)
    # good_actions = good_actions[:len(good_actions) // 2]

    for action in actions:
        beta = min(beta, max_value(player, action, board_clone, depth+1, alpha, beta))
        if beta <= alpha:
            return alpha
    return beta
