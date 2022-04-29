# Features of Evaluation Function

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

    my_cells.sort()
    op_cells.sort()
    return my_cells, op_cells


# Current max length of continuous pieces
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
