import random
from oppo_rand.board import *
from oppo_rand.utils import *


class Player:

    def __init__(self, player, n):
        """
        Called once at the beginning of a game to initialise this player.
        Set up an internal representation of the game state.

        The parameter player is the string "red" if your player will
        play as Red, or the string "blue" if your player will play
        as Blue.
        """
        self.side = player
        self.size = n
        self.board = Board(n)

    def action(self):
        """
        Called at the beginning of your turn. Based on the current state
        of the game, select an action to play.
        """
        # cmd = input()
        # cmd = cmd.split(",")
        # action = (cmd[0], int(cmd[1]), int(cmd[2]))
        cell = random.choice(self.board.empty_cells)
        return place_action(cell)

    def turn(self, player, action):
        """
        Called at the end of each player's turn to inform this player of
        their chosen action. Update your internal representation of the
        game state based on this. The parameter action is the chosen
        action itself.

        Note: At the end of your player's turn, the action parameter is
        the same as what your player returned from the action method
        above. However, the referee has validated it at this point.
        """
        if self.side == player:
            self.board.my_action((action[1], action[2]))
            self.board.place_cell((action[1], action[2]))
        else:
            self.board.op_action((action[1], action[2]))
            self.board.place_cell((action[1], action[2]))
        print("\n")
