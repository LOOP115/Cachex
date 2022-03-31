import heapq


# https://www.redblobgames.com/pathfinding/a-star/implementation.html
class PriorityQueue:

    def __init__(self):
        self.elements = []

    def empty(self) -> bool:
        return not self.elements

    # Pop the cell with lowest f(x)
    def pop(self):
        return heapq.heappop(self.elements)[1]

    # Add the new cell and do up heap
    def push(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
