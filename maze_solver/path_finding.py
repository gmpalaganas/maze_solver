from maze_solver.map_loader import Map
from maze_solver.distance import manhattan

from queue import PriorityQueue,Queue,LifoQueue
from enum import Enum

class Direction(Enum):
    UP    = (-1,0)
    DOWN  = (1,0)
    LEFT  = (0,-1)
    RIGHT = (0,1)

class PathNode:
    
    def __init__(self,location,direction=None,parent=None,heuristic=manhattan,target=None):
        self.location = location
        self.direction = direction
        self.target = target
        self.parent = parent
        self.heuristic = heuristic

    def __str__(self):
        return "Value: {}".format(self.location)

    def get_nodes_from_root(self):
        nodes = []
        
        cur_node = self

        while(cur_node.parent != None):
            nodes.append(cur_node)
            cur_node = cur_node.parent

        nodes.reverse()

        return nodes

    def get_path_from_root(self):
        path = []
        nodes = self.get_nodes_from_root()

        for node in nodes:
            path.append(node.direction.name)

        return path
    
    def get_path_cost(self):
        return len(self.get_nodes_from_root())

    def __lt__(self,other):
        self_cost = self.get_path_cost() + self.heuristic(self.location,self.target)
        other_cost = other.get_path_cost() + self.heuristic(other.location,other.target)

        return self_cost < other_cost

def get_passable(node,maze):
    passable = []

    x,y = node.location

    for direction in Direction:
        x_new = x + direction.value[0]
        y_new = y + direction.value[1]

        i,j = direction.value

        if x_new < 0 or y_new < 0:
            continue

        if not maze.walls[x_new][y_new]:
            passable_node = PathNode((x_new,y_new),direction,node,node.heuristic,node.target)
            passable.append(passable_node)

    return passable


def search(maze,start,end,frontiers):
    explored = []
    
    # Search tree
    while(not frontiers.empty()):
        cur_node = frontiers.get()

        if cur_node.location not in explored:
            explored.append(cur_node.location)

            if cur_node.location == end:
                return cur_node.get_path_from_root()
            
            for passable in get_passable(cur_node,maze):
                frontiers.put(passable)

    # No path found
    return None
    
def breadth_first(maze,start,end):
    start_node = PathNode(start)

    frontiers = Queue()
    frontiers.put(start_node)

    return search(maze,start,end,frontiers)

def depth_first(maze,start,end):
    start_node = PathNode(start)

    frontiers = LifoQueue()
    frontiers.put(start_node)

    return search(maze,start,end,frontiers)

def a_star(maze,start,end):
    start_node = PathNode(start,target=end)

    frontiers = PriorityQueue()
    frontiers.put(start_node)

    return search(maze,start,end,frontiers)

def find_path(maze,start,end,path_finder):
    return path_finder(maze,start,end)

def solve_maze(maze,path_finder):
    path = []
    start = maze.checkpoints[0].coordinates
    
    for i in range(1,len(maze.checkpoints)):
        end = maze.checkpoints[i].coordinates
        path.append(find_path(maze,start,end,path_finder))
        start = maze.checkpoints[i].coordinates

    return path
