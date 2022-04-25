from search.util import print_board


class Board:

    def __init__(self, size, start, goal, occupied, board_dict):
        self.size = size
        self.start = start
        self.goal = goal
        self.occupied = occupied
        self.board_dict = board_dict

    # Visualise the chess board
    def visualise(self):
        clone = dict(self.board_dict)
        print_board(self.size, clone)

    # Check if the cell is in bounds
    def in_bounds(self, cell):
        return 0 <= cell[0] < self.size and 0 <= cell[1] < self.size

    # Check if the cell is occupied
    def is_occupied(self, cell):
        for b in self.occupied:
            if b[0] == cell[0] and b[1] == cell[1]:
                return False
        return True
