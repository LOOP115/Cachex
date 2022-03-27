import heapq


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self) -> bool:
        return not self.elements

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


def heuristic(start, goal):
    dx = goal[0] - start[0]
    dy = goal[1] - start[1]

    if (dx >= 0 and dy >= 0) or (dx < 0 and dy < 0):
        return abs(dx + dy)
    else:
        return max(abs(dx), abs(dy))


# object oriented programming?
# a*: total cost = exact step have been executed + estimated heuristic2

# procedure
# 1 calculate heuristic as the initial costs and put the results in to priority queue(sort by the cost)
# 2 expand the node with the lowest cost, then update the queue
# 3 detect the goal state




# 1 board from input. 2 point (r,q)
# return false if is blocked, return true if is not blocked
def b_detect(board, point):
    for b in board:
        if b[1] == point[0] and b[2] == point[1]:
            return False
    return True

# inputs: n -> int, board -> 2d array with the coordinate have already get occupied, current node -> (x,y)
# outputs: 2d list with the neighboring
def neighbors(n, board, current):
    x = current[0]
    y = current[1]
    neighborList = []
    if 0 <= x + 1 < n and 0 <= y - 1 < n and b_detect(board, (x + 1, y - 1)):
        neighborList.append((x + 1,y - 1))
    if 0 <= x + 1 < n and 0 <= y < n and b_detect(board, (x + 1, y)):
        neighborList.append((x + 1, y))
    if 0 <= x < n and 0 <= y - 1 < n and b_detect(board, (x, y - 1)):
        neighborList.append((x, y - 1))
    if 0 <= x < n and 0 <= y + 1 < n and b_detect(board, (x, y + 1)):
        neighborList.append((x, y + 1))
    if 0 <= x - 1 < n and 0 <= y < n and b_detect(board, (x - 1, y)):
        neighborList.append((x - 1, y))
    if 0 <= x - 1 < n and 0 <= y + 1 < n and b_detect(board, (x - 1, y + 1)):
        neighborList.append((x - 1, y + 1))
    return neighborList



def a_star_search(n, board, start, goal):
    reach_goal = False
    pq = PriorityQueue()
    pq.put((start[0], start[1]), 0)

    # current node : (last node, cost so far)
    explored = {(start[0], start[1]): (None, 0)}

    while not pq.empty():
        current = pq.get()

        if current == goal:
            reach_goal = True
            break

        for next in neighbors(n, board, current):
            newCost = explored[current][1] + 1
            if next not in explored.keys() or newCost < explored[next][1]:
                explored[next] = (current, newCost)
                pq.put(next, newCost + heuristic(next, goal))
    return explored
