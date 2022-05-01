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
        # Decide next move
        decision = minimax(self.player, self.board)
        cell = decision[0]

        # Debug specific turn
        # cell = (0, 0)
        # if self.board.turn == 8:
        #     decision = minimax(self.player, self.board)
        #     cell = decision[0]
        # else:
        #     decision = minimax(self.player, self.board)
        #     cell = decision[0]

        manual = False
        if manual:
            cmd = input()
            cmd = cmd.split(",")
            cell = (int(cmd[0]), int(cmd[1]))
            # First move cannot be the center of the board
            if (self.board.turn == 1) and (not self.board.legal_first_move(cell)):
                cmd = input()
                cmd = cmd.split(",")
                cell = (int(cmd[0]), int(cmd[1]))

        debug = False
        if debug:
            my = self.player
            op = opponent(my)
            print(f"\n# Side: {my}")
            print(f"# Take {cell} with utility of {decision[1]}")
            sides = split_board(my, cell, self.board)
            print(f"# {my} cells: {sides[0]}")
            print(f"# {op} cells: {sides[1]}")

            # Check max path
            max_len0 = len(max_path_length(sides[0], self.board))
            max_len1 = len(max_path_length(sides[1], self.board))
            print(f"# {my} max path: {max_len0}")
            print(f"# {op} max path: {max_len1}")

            # Check start and goal
            start1, goal1 = start_goal(my, sides[0], sides[1], self.board)
            start2, goal2 = start_goal(op, sides[1], sides[0], self.board)
            print(f"# {my} find  start: {start1}  goal: {goal1}")
            print(f"# {op} find  start: {start2}  goal: {goal2}")

            # Check A*
            goals1, exp1 = min_win_cost(my, sides[0], sides[1], self.board)
            goals2, exp2 = min_win_cost(op, sides[1], sides[0], self.board)
            goal1, cost1 = best_goal(goals1, exp1)
            goal2, cost2 = best_goal(goals2, exp2)
            print(f"# {my} A*  goal: {goal1}  cost: {cost1}")
            print(f"# {op} A*  goal: {goal2}  cost: {cost2}")
            print_path(my, start1, goal1, exp1)
            # print(exp1)
            print_path(op, start2, goal2, exp2)
            # print(exp2)
            print()

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
        cell = (action[1], action[2])
        self.board.make_move(cell, player)
