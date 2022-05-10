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
        if len(cmd) == 1:
            return steal
        else:
            cell = (int(cmd[0]), int(cmd[1]))
            # The first move cannot be the center of the board
            if (self.board.turn == 1) and (not self.board.legal_first_move(cell)):
                cmd = input()
                cmd = cmd.split(",")
                cell = (int(cmd[0]), int(cmd[1]))
            return place_action(cell)

    def turn(self, player, action):
        # print(f"# {player}: {action}")
        if action[0] == steal:
            self.board.steal_move(player)
        else:
            cell = (action[1], action[2])
            self.board.make_move(cell, player)
