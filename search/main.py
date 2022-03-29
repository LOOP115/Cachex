"""
COMP30024 Artificial Intelligence, Semester 1, 2022
Project Part A: Searching
Team: ELDEN_KING
Members: Jiahao Chen, Zhiquan Lai
"""

import sys
import json
from search.astar import *
from search.board import *


def main():
    try:
        with open(sys.argv[1]) as file:
            data = json.load(file)
    except IndexError:
        print("usage: python3 -m search path/to/input.json", file=sys.stderr)
        sys.exit(1)

    # Process the inputs and initialise the board
    start = (data["start"][0], data["start"][1])
    goal = (data["goal"][0], data["goal"][1])
    board_dict = {start: "start", goal: "goal"}
    occupied = []
    for piece in data["board"]:
        occupied.append((piece[1], piece[2]))
        board_dict[(piece[1], piece[2])] = piece[0]
    board = Board(data["n"], start, goal, occupied, board_dict)
    # board.visualise()

    # Find path
    explored = find_path(board)
    print_path(board, explored)
    # search_history(explored)
    # board.visualise()
