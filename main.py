from maze_solver.map_loader import Map
from maze_solver.path_finding import solve_maze,breadth_first,depth_first,a_star

def main():
    maze = Map.load_map_from_file('mazes/test_maze.txt')

    start = maze.checkpoints[0].coordinates
    end = maze.checkpoints[1].coordinates

    path = solve_maze(maze,breadth_first)
    print("BFS")
    print(path)

    path = solve_maze(maze,depth_first)
    print("DFS")
    print(path)

    path = solve_maze(maze,a_star)
    print("A*")
    print(path)

if __name__ == '__main__':
    main()
