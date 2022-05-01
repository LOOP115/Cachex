from human.utils import *


class Board:

    # Vectors help to find neighbours
    dx = [1, 1, 0, 0, -1, -1]
    dy = [-1, 0, -1, 1, 0, 1]

    # Vectors help to find captures
    cx = [1, -1, 1, -1, 2, -2]
    cy = [1, -1, -2, 2, -1, 1]

    # Initialise the board
    def __init__(self, size, player):
        self.size = size
        self.turn = 1
        self.board_dict = {}
        self.player_dict = {}
        # Specify side color
        if player == red:
            self.player_dict[red] = my_flag
            self.player_dict[blue] = op_flag
        else:
            self.player_dict[red] = op_flag
            self.player_dict[blue] = my_flag
        # Record empty cells to get available actions faster
        self.empty_cells = []
        for i in range(size):
            for j in range(size):
                self.empty_cells.append((i, j))

    # Check if the cell is in bounds
    def in_bounds(self, cell):
        return 0 <= cell[0] < self.size and 0 <= cell[1] < self.size

    # Record each player's move after each turn and update the board
    def make_move(self, cell, player):
        self.board_dict[cell] = self.player_dict[player]
        self.turn += 1
        self.empty_cells.remove(cell)
        # Check captures
        cap = self.can_capture(cell, player)
        for c in unique_captures(cap):
            self.capture_remove(c)

    # Print board dict
    def print_board_dict(self):
        for k, v in self.board_dict.items():
            print(f"{k}: {v}")

    # Check if the first move is in the center of the board
    def legal_first_move(self, move):
        if (self.size % 2 != 0) and (move[0] == move[1]) and (self.size >> 1 == move[0]):
            return False
        return True

    # Find cells 1 unit from the current cell
    def neighbours(self, cell):
        x = cell[0]
        y = cell[1]
        neighbour_list = []
        for i in range(6):
            cell = (x + self.dx[i], y + self.dy[i])
            if self.in_bounds(cell):
                neighbour_list.append(cell)
        return neighbour_list

    # Find cells 2 unit from the current cell diagonally
    def neighbours_diagonal(self, cell):
        x = cell[0]
        y = cell[1]
        res = []
        for i in range(6):
            cell = (x + self.cx[i], y + self.cy[i])
            if self.in_bounds(cell):
                res.append(cell)
        return res

    # Remove pieces that have been captured
    def capture_remove(self, cell):
        self.board_dict.pop(cell)
        self.empty_cells.append(cell)

    # Check if the move can perform a capture
    # Return the cell for the capture to be performed, otherwise return null
    def can_capture(self, cell, player):
        # Specify the player
        my = my_flag
        op = op_flag
        if self.player_dict[player] == op_flag:
            my = op_flag
            op = my_flag

        # Search the neighbours and record the input player's opponent cells
        neighbour_cells = self.neighbours(cell)
        op_cells = []
        for c in neighbour_cells:
            if c in self.board_dict.keys() and self.board_dict[c][0] == op:
                op_cells.append(c)

        # Impossible to capture if number of neighbours is less than 2
        capture_list = []
        if len(op_cells) < 2:
            return capture_list

        # Type 1: 1 unit distance
        my_cells1 = []
        for c in neighbour_cells:
            if c in self.board_dict.keys() and self.board_dict[c][0] == my:
                my_cells1.append(c)

        # Type 2: 2 unit distance in diagonal directions
        my_cells2 = []
        diagonal_cells = self.neighbours_diagonal(cell)
        for c in diagonal_cells:
            if c in self.board_dict.keys() and self.board_dict[c][0] == my:
                my_cells2.append(c)

        # Check if there exists a capture
        for m in my_cells1:
            temp_capture = []
            for o in op_cells:
                if (manhattan(cell, o) == 1) and (manhattan(m, o) == 1):
                    temp_capture.append(o)
                # Success capture
                if len(temp_capture) == 2:
                    capture_list.append(temp_capture)
                    break

        for m in my_cells2:
            temp_capture = []
            for o in op_cells:
                if (manhattan(cell, o) == 1) and (manhattan(m, o) == 1):
                    temp_capture.append(o)
                # Success capture
                if len(temp_capture) == 2:
                    capture_list.append(temp_capture)
                    break

        return capture_list
