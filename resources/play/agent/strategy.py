from math import inf, tanh
from copy import deepcopy
from agent.utils import *
import time
import random

# Decide if this is a good move to search deeper
def evaluation(player, action, board):
    lose = False

    # My benefit if I make this action
    my_benefit = utility_value(player, player, action, board)

    # My benefit if opponent take this action
    op_benefit = utility_value(player, opponent(player), action, board)
    if op_benefit == -inf:
        lose = True

    return my_benefit - op_benefit, lose


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
    my_win_cost = None
    if my_win is not None:
        my_win_cost = best_goal(my_win, my_path)[1]
    op_win, op_path = min_win_cost(opponent(player), op_cells, my_cells, board)
    op_win_cost = None
    if op_win is not None:
        op_win_cost = best_goal(op_win, op_path)[1]

    # If the cost to win is none, set it to 2n as a huge contribution utility value
    if my_win_cost is None:
        my_win_cost = 2 * n
    if op_win_cost is None:
        op_win_cost = 2 * n

    # Compute utility value based on the following features
    res = 1 * len(my_max_path) - 2 * len(op_max_path) - 2 * my_win_cost + 3 * op_win_cost + 1 * len(my_cells) - 2 * len(op_cells)
    return res


# Mini Max with alpha-beta pruning
def minimax(player, board, danger, time_left, turn_limit, ext):
    # Set a timer
    # print(f"# Danger time: {danger}")
    # print(f"# Ext time: {ext}")
    # print(f"# Time limit: {time_left}")
    # print(f"# Turn limit: {turn_limit}")
    start_time = time.time()
    cut_depth = set_depth(board)
    # print(f"# max depth: {cut_depth}")

    # First move
    if board.turn == 1:
        action = (0, board.size >> 1)
        return [action]
    # Get all available actions currently
    actions = get_actions(board)

    # Time nearly exhausted, do not make more calculations
    if time_left < ext:
        # print("# random!")
        return [random.choice(actions)]

    # Filter out promising actions at current state
    good_actions = []
    capture_actions = []
    lose_actions = []
    may_lose = False
    for action in actions:
        score, lose = evaluation(player, action, board)
        # print(f"# eval: {action}: {score}")
        if score == inf:
            if not lose:
                return [action, inf]
            else:
                may_lose = True
                lose_actions.append(action)
        good_actions.append((action, score))
        if len(board.can_capture(action, player)) > 0:
            capture_actions.append((action, score))

    # May lose, try to perform a capture
    if may_lose:
        if len(capture_actions) > 0:
            good_actions = capture_actions
        else:
            # No available capture, try to block
            return [lose_actions[0]]

    # If opponent's min cost to win is too small, try to capture
    my_cells, op_cells = split_curr_board(player, board)
    op_win, op_path = min_win_cost(opponent(player), op_cells, my_cells, board)
    op_win_cost = None
    if op_win is not None:
        op_win_cost = best_goal(op_win, op_path)[1]
    # print(f"# op win cost: {op_win_cost}")
    if op_win_cost is not None and op_win_cost <= 0.4 * board.size:
        if len(capture_actions) > 0:
            good_actions = capture_actions

    # Sort the promising actions based on their evaluation result
    # Choose the greatest half to perform mini-max search to reduce time complexity
    good_actions.sort(key=lambda x: x[1], reverse=True)
    good_actions = good_actions[:len(good_actions) // 2 + 1]
    # print(f"# eval time: {time.time() - start_time}")

    # Limited time left
    if time_left < danger or cut_depth == 0:
        return [good_actions[0][0]]

    # Find the action with max utility value after looking several steps ahead
    value = -inf
    res = good_actions[0][0]
    for action in good_actions:
        # Check time limit
        curr_time = time.time()
        if curr_time - start_time > turn_limit:
            break
        move = action[0]
        temp = min_value(player, move, board, 0, -inf, inf, cut_depth)
        # print(f"# min value: {move}: {temp}")
        if temp >= value:
            value = temp
            res = move

    # Consider if steal in second turn
    # if board.turn == 2:
    #     # first_move = list(board.board_dict.keys())[0]
    #     # print(f"# Decide if to steal {first_move}")
    #     curr_time = time.time()
    #     if curr_time - start_time > turn_limit:
    #         return [steal]
    #     board_clone = deepcopy(board)
    #     steal_move = board_clone.fake_steal()
    #     first_move_utility = min_value(player, steal_move, board_clone, 0, -inf, inf, cut_depth)
    #     # print(f"# Utility of steal: {first_move_utility}")
    #     # print(f"# Utility of not steal: {value}")
    #     if first_move_utility >= value:
    #         return [steal]

    return res, value


# Return the max value assuming opponent selected actions with min values
def max_value(player, action, board, depth, alpha, beta, max_depth):
    # Max search depth reached, terminate
    if depth == max_depth:
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
        alpha = max(alpha, min_value(player, action, board_clone, depth + 1, alpha, beta, max_depth))
        if alpha >= beta:
            return beta
    return alpha


# Return the min value assuming I selected actions with max values
def min_value(player, action, board, depth, alpha, beta, max_depth):
    # Max search depth reached, terminate
    if depth == max_depth:
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
        beta = min(beta, max_value(player, action, board_clone, depth + 1, alpha, beta, max_depth))
        if beta <= alpha:
            return alpha
    return beta
