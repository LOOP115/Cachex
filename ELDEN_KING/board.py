from ELDEN_KING.utils import *


class Board:

    # Vectors help to find neighbours
    dx = [1, 1, 0, 0, -1, -1]
    dy = [-1, 0, -1, 1, 0, 1]

    # Vectors help to find captures
    cx = [1, -1, 1, -1, 2, -2]
    cy = [1, -1, -2, 2, -1, 1]

    def __init__(self, size, player):
        self.size = size
        self.turn = 1
        self.board_dict = {}
        self.player_dict = {}
        if player == "red":
            self.player_dict["red"] = "m"
            self.player_dict["blue"] = "o"
        else:
            self.player_dict["red"] = "o"
            self.player_dict["blue"] = "m"
        self.empty_cells = []
        for i in range(size):
            for j in range(size):
                self.empty_cells.append((i, j))

    # Check if the cell is in bounds
    def in_bounds(self, cell):
        return 0 <= cell[0] < self.size and 0 <= cell[1] < self.size

    # Record each player's move after each turn
    def make_move(self, cell, player):
        self.board_dict[cell] = self.player_dict[player]
        self.turn += 1
        self.empty_cells.remove(cell)

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
        # Check if neighbour cells are in bounds
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
        # Check if neighbour cells are in bounds
        for i in range(6):
            cell = (x + self.cx[i], y + self.cy[i])
            if self.in_bounds(cell):
                res.append(cell)
        return res

    # Check if the move can perform a capture
    # Return the cell for the capture to be performed, otherwise return null
    def can_capture(self, cell, player):
        # Specify the player
        my = "m"
        op = "o"
        if self.player_dict[player] == "o":
            my = "o"
            op = "m"

        # Search the neighbours and record the input player's opponent cells
        neighbour_cells = self.neighbours(cell)
        op_cells = []
        for c in neighbour_cells:
            if c in self.board_dict.keys() and self.board_dict[c][0] == op:
                op_cells.append(c)

        capture_list = []

        # Impossible to capture if number of neighbours is less than 2
        if len(op_cells) < 2:
            return capture_list

        # Type 1: 1 unit distance
        my_cells1 = []
        for c in neighbour_cells:
            if c in self.board_dict.keys() and self.board_dict[c][0] == my:
                my_cells1.append(c)

        my_cells2 = []
        # Type 2: 2 unit distance in diagonal directions
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
                    # print("capture!")
                    capture_list.append(temp_capture)
                    break

        for m in my_cells2:
            temp_capture = []
            for o in op_cells:
                if (manhattan(cell, o) == 1) and (manhattan(m, o) == 1):
                    temp_capture.append(o)
                # Success capture
                if len(temp_capture) == 2:
                    # print("capture!")
                    capture_list.append(temp_capture)
                    break

        return capture_list

    # Remove pieces that have been captured
    def capture_remove(self, cell):
        self.board_dict.pop(cell)
        self.empty_cells.append(cell)
