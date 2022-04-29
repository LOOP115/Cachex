from ELDEN_KING.board import *
from ELDEN_KING.utils import *
from ELDEN_KING.strategy import *

class Player:

    def __init__(self, player, n):
        """
        Called once at the beginning of a game to initialise this player.
        Set up an internal representation of the game state.

        The parameter player is the string "red" if your player will
        play as Red, or the string "blue" if your player will play
        as Blue.
        """
        self.player = player
        self.size = n
        self.board = Board(n, player)

    def action(self):
        """
        Called at the beginning of your turn. Based on the current state
        of the game, select an action to play.
        """
        # self.board.print_board_dict()
        cmd = input()
        cmd = cmd.split(",")
        cell = (int(cmd[1]), int(cmd[2]))
        # The first move cannot be the center of the board
        if (self.board.turn == 1) and (not self.board.legal_first_move(cell)):
            cmd = input()
            cmd = cmd.split(",")
            cell = (int(cmd[1]), int(cmd[2]))

        # Check max path
        # sides = split_board(self.player, cell, self.board)
        # print(sides[0])
        # print(sides[1])
        # max_len0 = max_path_length(sides[0], self.board)
        # max_len1 = max_path_length(sides[1], self.board)
        # print(max_len0)
        # print(max_len1)

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
        # print(f"Turn: {self.side}")
        # print(player)
        # print(action)
        cell = (action[1], action[2])
        result = self.board.can_capture(cell, player)
        # print(result)
        if result is not None:
            self.board.capture_remove(result)
        self.board.make_move(cell, player)
