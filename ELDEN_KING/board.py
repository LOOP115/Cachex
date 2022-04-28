class Board:

    def __init__(self, size):
        self.size = size
        self.turn = 1
        self.board_dict = {}

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

    # Print board dict
    def print_dict(self):
        for k, v in self.board_dict.items():
            print(f"{k}: {v}")
