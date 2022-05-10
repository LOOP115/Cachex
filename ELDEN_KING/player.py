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
        self.danger_time = n * n * 0.35
        self.ext_time = n * n * 0.02
        self.time_left = n * n
        self.turn_limit = 5

    def action(self):
        """
        Called at the beginning of your turn. Based on the current state
        of the game, select an action to play.
        """
        # Decide next move and update timer
        start_time = time.time()
        decision = minimax(self.player, self.board, self.danger_time, self.time_left, self.turn_limit, self.ext_time)
        end_time = time.time()
        time_elapse = end_time - start_time
        self.time_left -= time_elapse
        if decision == steal:
            return decision
        return place_action(decision)

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
        if action[0] == steal:
            self.board.steal_move(player)
        else:
            cell = (action[1], action[2])
            self.board.make_move(cell, player)
