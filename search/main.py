"""
COMP30024 Artificial Intelligence, Semester 1, 2022
Project Part A: Searching

This script contains the entry point to the program (the code in
`__main__.py` calls `main()`). Your solution starts here!
"""

import sys
import json

# If you want to separate your code into separate files, put them
# inside the `search` directory (like this one and `util.py`) and
# then import from them like this:
from search.util import print_board, print_coordinate
from search.astar import a_star_search, neighbors


def main():
    try:
        with open(sys.argv[1]) as file:
            data = json.load(file)
    except IndexError:
        print("usage: python3 -m search path/to/input.json", file=sys.stderr)
        sys.exit(1)

    # TODO:
    # Find and print a solution to the board configuration described
    # by `data`.
    # Why not start by trying to print this configuration out using the
    # `print_board` helper function? (See the `util.py` source code for
    # usage information).

    start = (data["start"][0], data["start"][1])
    goal = (data["goal"][0], data["goal"][1])
    boardDict = {start: "start",
                 goal: "goal"}
    for block in data["board"]:
        boardDict[(block[1], block[2])] = block[0]
    print_board(data["n"], boardDict)

    # print(neighbors(data["n"], data["board"], (2,1)))

    explored = a_star_search(data["n"], data["board"], data["start"], data["goal"])
    print(explored.keys())

    for key in explored.keys():
        print(f'current: {key}: last node: {explored[key][0]}  cost so far: {explored[key][1]}')

    node = goal
    result = []
    while node != start:
        result.append(node)
        node = explored[node][0]

        boardDict[node] = "p"
        print_board(data["n"], boardDict)

    result.append(start)
    result.reverse()
    print(result)
