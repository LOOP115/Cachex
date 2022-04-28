class Board:

    def __init__(self, size):
        self.size = size
        self.turn = 1
        self.board_dict = {}
        self.empty_cells = []
        for i in range(size):
            for j in range(size):
                self.empty_cells.append((i, j))

    # Check if the cell is in bounds
    def in_bounds(self, cell):
        return 0 <= cell[0] < self.size and 0 <= cell[1] < self.size

    # Record my move
    def my_action(self, cell):
        self.board_dict[cell] = ("m", self.turn)
        self.turn += 1

    # Record opponent's move
    def op_action(self, cell):
        self.board_dict[cell] = ("o", self.turn)
        self.turn += 1

    # Update empty_cells after actions
    def place_cell(self, cell):
        self.empty_cells.remove(cell)

    # Check if the first move is in the center of the board
    def legal_first_move(self, move):
        if (self.size % 2 != 0) and (move[0] == move[1]) and (self.size >> 1 == move[0]):
            return False
        return True

    # Print board dict
    def print_dict(self):
        for k, v in self.board_dict.items():
            print(f"{k}: {v}")
