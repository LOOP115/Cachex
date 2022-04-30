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
        cell = (int(cmd[0]), int(cmd[1]))
        # The first move cannot be the center of the board
        if (self.board.turn == 1) and (not self.board.legal_first_move(cell)):
            cmd = input()
            cmd = cmd.split(",")
            cell = (int(cmd[0]), int(cmd[1]))
        return place_action(cell)

    def turn(self, player, action):
        cell = (action[1], action[2])
        result = self.board.can_capture(cell, player)
        for r in unique_captures(result):
            self.board.capture_remove(r)
        self.board.make_move(cell, player)
