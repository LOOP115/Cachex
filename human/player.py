from human.board import *
from human.utils import *


class Player:

    def __init__(self, player, n):
        self.side = player
        self.size = n
        self.board = Board(n, player)

    def action(self):
        cmd = input()
        cmd = cmd.split(",")
        cell = (int(cmd[1]), int(cmd[2]))
        # The first move cannot be the center of the board
        if (self.board.turn == 1) and (not self.board.legal_first_move(cell)):
            cmd = input()
            cmd = cmd.split(",")
            cell = (int(cmd[1]), int(cmd[2]))
        return place_action(cell)

    def turn(self, player, action):
        cell = (action[1], action[2])
        result = self.board.can_capture(cell, player)
        if result is not None:
            self.board.capture_remove(result[1])
        self.board.make_move(cell, player)
