from greedy.board import *
from greedy.utils import *
from greedy.strategy import *


class Player:

    def __init__(self, player, n):
        self.player = player
        self.size = n
        self.board = Board(n, player)

    def action(self):
        cell = minimax(self.player, self.board)
        return place_action(cell)

    def turn(self, player, action):
        cell = (action[1], action[2])
        self.board.make_move(cell, player)
