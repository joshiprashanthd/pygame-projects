from typing import Union, AnyStr, List, Tuple, Any

from grid import Grid
from point import Point
from priority_queue import PriorityQueue

import math


def copy(point):
        return Point(point.x, point.y)

class AStarAlgorithm:
    def __init__(self, grid: Grid, start: tuple, end: tuple):
        self.grid = grid
        self.rows = self.grid.rows
        self.cols = self.grid.cols
        self.obstacle = 1
        self.free = 0
        self.close = -1

        self.found = False  # found is set to true if the point reaches the end point
        self.resign = False

        self.f = 0
        self.g = 0
        self.cost = 1  # cost for taking each step

        self.gScore = Grid[int](self.rows, self.cols, math.inf)  # cost map of each cell
        self.fScore = Grid[int](self.rows, self.cols, math.inf)
        self.cameFrom = Grid[Point](self.rows, self.cols, None)
        self.action = Grid[int](self.rows, self.cols, 0)
        self.closed = Grid[int](self.rows, self.cols, 0)  # to prevent path going backwards

        self.start = Point(*start)
        self.end = Point(*end)

        self.up = Point(-1, 0)
        self.left = Point(0, -1)
        self.down = Point(1, 0)
        self.right = Point(0, 1)
        self.topLeft = Point(-1, -1)
        self.topRight = Point(-1, 1)
        self.bottomLeft = Point(1, -1)
        self.bottomRight = Point(1, 1)
        
        self.deltas = [self.up, self.left, self.down, self.right, self.topLeft, self.topRight, self.bottomLeft, self.bottomRight]

        self.cells = PriorityQueue(maxsize=1000, max_queue=False, sort_index=0)

    def __init_gscore(self):
        self.gScore[self.start.x][self.start.y] = 0
        self.fScore[self.start.x][self.start.y] = self.start.absolute_distance_from(self.end)

    def __reconstruct_path(self, new_point):
        invpath = []
        point = copy(new_point)
        invpath.append(point)
        while point is not None:
            point = self.cameFrom[point.x][point.y]
            invpath.insert(0, point)
        return invpath
    
    def run(self):
        self.__init_gscore()

        self.cells.insert((self.fScore[self.start.x][self.start.y], self.start))

        while not self.found and not self.resign:
            if self.cells.is_empty():
                return "PATH NOT FOUND"

            _, current = self.cells.pop()

            if current == self.end:
                self.found = True
            else:
                for index, delta in enumerate(self.deltas):
                    neighbour = current + delta
                    x = neighbour.x
                    y = neighbour.y
                    if Point(0, 0) <= neighbour <= Point(self.rows - 1, self.cols - 1):
                        if self.closed[x][y] == self.free and self.grid[x][y] == self.free:
                            tentativeGScore = self.gScore[current.x][current.y] + self.cost
                            if tentativeGScore < self.gScore[x][y]:
                                self.cameFrom[x][y] = copy(current)
                                self.gScore[x][y] = tentativeGScore
                                self.fScore[x][y] = self.gScore[x][y] + neighbour.absolute_distance_from(self.end)
                                self.cells.insert((self.fScore[x][y], copy(neighbour)))
                                self.closed[x][y] = self.close
            yield self.__reconstruct_path(current)
