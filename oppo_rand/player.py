import random
from oppo_rand.board import *
from oppo_rand.utils import *


class Player:

    def __init__(self, player, n):
        self.side = player
        self.size = n
        self.board = Board(n, player)

    def action(self):
        cell = random.choice(self.board.empty_cells)
        # The first move cannot be the center of the board
        while (self.board.turn == 1) and (not self.board.legal_first_move(cell)):
            cell = random.choice(self.board.empty_cells)
        return place_action(cell)

    def turn(self, player, action):
        cell = (action[1], action[2])
        self.board.make_move(cell, player)
